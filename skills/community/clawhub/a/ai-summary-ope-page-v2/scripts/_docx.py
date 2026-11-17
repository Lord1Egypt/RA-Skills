# -*- coding: utf-8 -*-
"""_docx.py — перевод DOCX в PDF перед обычной обработкой навыка.

Без внешних программ и библиотек: DOCX читается стандартным zipfile + ElementTree, превращается в HTML
и верстается в PDF движком PyMuPDF (Story), который навык и так использует. Ни Word, ни LibreOffice,
ни дочерних процессов, ни сети.

Что переносится: абзацы и заголовки (по стилям документа), жирный и курсив, маркированные и нумерованные
списки, таблицы (с объединением по горизонтали), рисунки PNG/JPEG/GIF/BMP/TIFF, текстовые поля, данные
диаграмм Word (ряды и значения из кэша диаграммы — таблицей), сноски и концевые сноски (в конце), правки
в режиме рецензирования (вставленное — да, удалённое — нет).
Что не переносится: колонтитулы, рисунки EMF/WMF (на их месте — пометка), точная вёрстка Word. Поэтому
номера страниц PDF не совпадают с Word: в резюме ссылки идут на страницы этого PDF.
"""
from __future__ import annotations

import html
import io
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "v": "urn:schemas-microsoft-com:vml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
W = "{%s}" % NS["w"]
R = "{%s}" % NS["r"]
MAX_UNZIPPED_MB = 600          # защита от «zip-бомбы»
MAX_MEMBERS = 20000
MAX_CHARTS = 200               # диаграмм на документ: остальные — заглушкой
MAX_CHART_SERIES = 40          # рядов в одной диаграмме
MAX_CHART_POINTS = 500         # точек в ряду: idx вне [0, MAX_CHART_POINTS) отбрасываются
MAX_HTML_CHARS = 40_000_000    # предел промежуточного HTML (защита памяти при вёрстке PDF)
IMAGE_OK = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff"}
CSS = """
body { font-family: sans-serif; font-size: 10.5pt; line-height: 1.3; }
h1 { font-size: 17pt; margin: 10pt 0 6pt 0; } h2 { font-size: 14pt; margin: 9pt 0 5pt 0; }
h3 { font-size: 12pt; margin: 8pt 0 4pt 0; } h4, h5, h6 { font-size: 11pt; margin: 6pt 0 3pt 0; }
p { margin: 0 0 5pt 0; } p.title { font-size: 19pt; font-weight: bold; margin-bottom: 8pt; }
p.li { margin: 0 0 3pt 0; } p.cap { font-style: italic; font-size: 9.5pt; }
table { border-collapse: collapse; margin: 4pt 0 8pt 0; width: 100%; }
td, th { border: 0.6pt solid #808080; padding: 2pt 3pt; font-size: 9pt; vertical-align: top; }
p.note { font-size: 9pt; color: #555555; } p.fn { font-size: 9pt; margin: 0 0 2pt 0; }
"""


class DocxError(Exception):
    pass


def _on(el) -> bool:
    """w:b, w:i: есть элемент и w:val не выключает его."""
    if el is None:
        return False
    v = el.get(W + "val")
    return v not in ("0", "false", "off", "none")


class _Converter:
    def __init__(self, z: zipfile.ZipFile):
        self.z = z
        self.images: list[tuple[bytes, str]] = []
        self.warnings: list[str] = []
        self.stats = {"paragraphs": 0, "tables": 0, "images": 0, "images_skipped": 0, "charts": 0, "footnotes": 0}
        self.rels = self._rels("word/_rels/document.xml.rels")
        self.styles, self.style_num = self._styles()
        self.numfmt = self._numbering()
        self.counters: dict[tuple, int] = {}
        self.notes: list[str] = []
        self.footnotes = self._notes("word/footnotes.xml", "footnote")
        self.endnotes = self._notes("word/endnotes.xml", "endnote")

    # ---------------------------------------------------------------- части пакета
    def _xml(self, name: str):
        try:
            return ET.fromstring(self.z.read(name))
        except KeyError:
            return None
        except ET.ParseError as e:
            raise DocxError("часть %s повреждена: %s" % (name, e)) from None

    def _rels(self, name: str) -> dict:
        root = self._xml(name)
        out = {}
        if root is None:
            return out
        base = name.split("/_rels/")[0]
        for r in root.findall("rel:Relationship", NS):
            tgt = r.get("Target", "")
            if r.get("TargetMode") == "External":
                continue
            path = tgt.lstrip("/") if tgt.startswith("/") else (base + "/" + tgt)
            parts = []
            for p in path.split("/"):                    # нормализовать ../
                if p == "..":
                    parts and parts.pop()
                elif p and p != ".":
                    parts.append(p)
            out[r.get("Id")] = "/".join(parts)
        return out

    def _styles(self) -> tuple[dict, dict]:
        """styleId → уровень заголовка (1–6), 0 — заголовок документа (Title); styleId → numPr стиля
        (списки, заданные стилем «Маркированный список» и т. п.)."""
        out, nums = {}, {}
        root = self._xml("word/styles.xml")
        if root is None:
            return out, nums
        based = {}
        for st in root.findall("w:style", NS):
            sid = st.get(W + "styleId", "")
            np_ = st.find("w:pPr/w:numPr", NS)
            if np_ is not None and np_.find("w:numId", NS) is not None:
                nums[sid] = np_
            b = st.find("w:basedOn", NS)
            if b is not None:
                based[sid] = b.get(W + "val", "")
        for sid in list(based):                          # список, унаследованный от базового стиля
            cur, hops = sid, 0
            while sid not in nums and cur in based and hops < 10:
                cur, hops = based[cur], hops + 1
                if cur in nums:
                    nums[sid] = nums[cur]
        for st in root.findall("w:style", NS):
            sid = st.get(W + "styleId", "")
            name = (st.find("w:name", NS).get(W + "val", "") if st.find("w:name", NS) is not None else "").lower()
            lvl = None
            m = re.search(r"(heading|заголовок)\s*(\d)", name)
            if m:
                lvl = min(6, int(m.group(2)))
            elif name in ("title", "название", "заголовок"):
                lvl = 0
            ol = st.find("w:pPr/w:outlineLvl", NS)
            if lvl is None and ol is not None and ol.get(W + "val", "9").isdigit() and int(ol.get(W + "val")) < 6:
                lvl = int(ol.get(W + "val")) + 1
            if lvl is not None:
                out[sid] = lvl
        return out, nums

    def _numbering(self) -> dict:
        """(numId, ilvl) → numFmt (decimal, bullet, …)."""
        root = self._xml("word/numbering.xml")
        out = {}
        if root is None:
            return out
        abstract = {}
        for an in root.findall("w:abstractNum", NS):
            fm = {}
            for lv in an.findall("w:lvl", NS):
                f = lv.find("w:numFmt", NS)
                fm[lv.get(W + "ilvl", "0")] = f.get(W + "val", "bullet") if f is not None else "bullet"
            abstract[an.get(W + "abstractNumId")] = fm
        for num in root.findall("w:num", NS):
            a = num.find("w:abstractNumId", NS)
            fm = abstract.get(a.get(W + "val") if a is not None else "", {})
            for ilvl, f in fm.items():
                out[(num.get(W + "numId"), ilvl)] = f
        return out

    def _notes(self, name: str, tag: str) -> dict:
        root = self._xml(name)
        out = {}
        if root is None:
            return out
        for n in root.findall("w:" + tag, NS):
            nid = n.get(W + "id")
            if n.get(W + "type") in ("separator", "continuationSeparator", "continuationNotice"):
                continue
            text = " ".join(self._plain(p) for p in n.iter(W + "p")).strip()
            if text:
                out[nid] = text
        return out

    # ---------------------------------------------------------------- текст
    def _plain(self, el) -> str:
        parts = []
        for x in el.iter():
            if x.tag == W + "t":
                parts.append(x.text or "")
            elif x.tag in (W + "tab",):
                parts.append(" ")
        return re.sub(r"\s+", " ", "".join(parts)).strip()

    def _runs(self, p) -> str:
        """HTML содержимого абзаца: текст, жирный/курсив, разрывы, рисунки, диаграммы, ссылки на сноски."""
        out = []
        for el in p:
            tag = el.tag
            if tag == W + "r":
                out.append(self._run(el))
            elif tag in (W + "hyperlink", W + "smartTag", W + "fldSimple", W + "ins", W + "customXml", W + "sdt",
                         W + "sdtContent", W + "bdo", W + "dir"):
                out.append(self._runs(el))
            elif tag == "{%s}AlternateContent" % NS["mc"]:
                ch = el.find("mc:Choice", NS)
                fb = el.find("mc:Fallback", NS)
                out.append(self._runs(ch if ch is not None else (fb if fb is not None else el)))
            # w:del, w:pPr, w:bookmark*, w:proofErr — пропускаются
        return "".join(out)

    def _run(self, r) -> str:
        rpr = r.find("w:rPr", NS)
        bold = italic = False
        if rpr is not None:
            bold, italic = _on(rpr.find("w:b", NS)), _on(rpr.find("w:i", NS))
            va = rpr.find("w:vertAlign", NS)
            sup = va is not None and va.get(W + "val") == "superscript"
        else:
            sup = False
        buf = []
        for x in r:
            t = x.tag
            if t == W + "t":
                buf.append(html.escape(x.text or ""))
            elif t == W + "tab":
                buf.append(" ")
            elif t in (W + "br", W + "cr"):
                buf.append("<br/>")
            elif t == W + "noBreakHyphen":
                buf.append("-")
            elif t == W + "sym":
                buf.append(" ")
            elif t == W + "footnoteReference":
                buf.append(self._noteref(x.get(W + "id"), self.footnotes, ""))
            elif t == W + "endnoteReference":
                buf.append(self._noteref(x.get(W + "id"), self.endnotes, "к"))
            elif t in (W + "drawing", W + "pict", W + "object"):
                buf.append(self._drawing(x))
            elif t == "{%s}AlternateContent" % NS["mc"]:
                ch = x.find("mc:Choice", NS)
                if ch is not None:
                    for y in ch:
                        if y.tag in (W + "drawing", W + "pict"):
                            buf.append(self._drawing(y))
        s = "".join(buf)
        if not s.strip("<br/> "):
            return s
        if sup and not s.startswith("["):
            s = "<sup>%s</sup>" % s
        if italic:
            s = "<i>%s</i>" % s
        if bold:
            s = "<b>%s</b>" % s
        return s

    def _noteref(self, nid, store: dict, prefix: str) -> str:
        text = store.get(nid)
        if not text:
            return ""
        self.notes.append("%s%d. %s" % (prefix, len(self.notes) + 1, text))
        self.stats["footnotes"] += 1
        return "<sup>[%s%d]</sup>" % (prefix, len(self.notes))

    # ---------------------------------------------------------------- рисунки, диаграммы, текстовые поля
    def _drawing(self, el) -> str:
        out = []
        for tb in el.iter(W + "txbxContent"):                 # текстовое поле: его абзацы
            out.append(self._blocks(tb))
        for blip in el.iter("{%s}blip" % NS["a"]):
            out.append(self._image(blip.get(R + "embed") or blip.get(R + "link")))
        for im in el.iter("{%s}imagedata" % NS["v"]):
            out.append(self._image(im.get(R + "id")))
        for ch in el.iter("{%s}chart" % NS["c"]):
            out.append(self._chart(ch.get(R + "id")))
        return "".join(out)

    def _image(self, rid) -> str:
        path = self.rels.get(rid or "")
        if not path:
            return ""
        ext = Path(path).suffix.lower()
        if ext not in IMAGE_OK:
            self.stats["images_skipped"] += 1
            return '<p class="note">[рисунок в формате %s не перенесён]</p>' % html.escape(ext.lstrip(".").upper() or "?")
        try:
            data = self.z.read(path)
        except KeyError:
            return ""
        name = "img%03d%s" % (len(self.images) + 1, ".jpg" if ext == ".jpeg" else ext)
        self.images.append((data, name))
        self.stats["images"] += 1
        return '<img src="%s" style="max-width:100%%"/>' % name

    def _chart(self, rid) -> str:
        path = self.rels.get(rid or "")
        root = self._xml(path) if path else None
        if root is None or self.stats["charts"] >= MAX_CHARTS:
            return '<p class="note">[диаграмма]</p>'
        self.stats["charts"] += 1
        title = " ".join(t.text or "" for t in root.findall(".//c:title//a:t", NS)).strip()
        series = []
        cats: list[str] = []
        for ser in root.iter("{%s}ser" % NS["c"]):
            if len(series) >= MAX_CHART_SERIES:
                break
            name = " ".join(v.text or "" for v in ser.findall("c:tx//c:v", NS)).strip() or "ряд %d" % (len(series) + 1)
            cat_pts = ser.findall("c:cat//c:pt", NS)
            val_pts = ser.findall("c:val//c:pt", NS) or ser.findall("c:yVal//c:pt", NS)
            c = _chart_points(cat_pts)
            v = _chart_points(val_pts)
            fmt = " ".join(f.text or "" for f in ser.findall("c:val//c:formatCode", NS))
            if "%" in fmt:                               # процентный формат: в кэше доли (0.37 → 37%)
                v = {k: _pct(x) for k, x in v.items()}
            if not cats and c:
                cats = [c[k] for k in sorted(c)]
            series.append((name, v))
        if not series:
            return '<p class="note">[диаграмма%s]</p>' % (": " + html.escape(title) if title else "")
        n = min(MAX_CHART_POINTS, max([len(cats)] + [max(v) + 1 if v else 0 for _, v in series]))
        cats = cats[:n]
        cats = cats + [""] * (n - len(cats))
        head = "<tr><th></th>%s</tr>" % "".join("<th>%s</th>" % html.escape(s) for s, _ in series)
        rows = "".join("<tr><td>%s</td>%s</tr>" % (html.escape(cats[i]), "".join(
            "<td>%s</td>" % html.escape(_num(v.get(i, ""))) for _, v in series)) for i in range(n))
        cap = '<p class="cap">Диаграмма%s (данные диаграммы)</p>' % (": " + html.escape(title) if title else "")
        return cap + "<table>%s%s</table>" % (head, rows)

    # ---------------------------------------------------------------- блоки
    def _paragraph(self, p) -> str:
        self.stats["paragraphs"] += 1
        ppr = p.find("w:pPr", NS)
        sid = ""
        lvl = None
        numpr = None
        if ppr is not None:
            ps = ppr.find("w:pStyle", NS)
            sid = ps.get(W + "val", "") if ps is not None else ""
            lvl = self.styles.get(sid)
            if lvl is None:
                m = re.fullmatch(r"(?i)(heading|заголовок)(\d)", sid)
                lvl = int(m.group(2)) if m else (0 if sid.lower() == "title" else None)
            ol = ppr.find("w:outlineLvl", NS)
            if lvl is None and ol is not None and ol.get(W + "val", "9").isdigit() and int(ol.get(W + "val")) < 6:
                lvl = int(ol.get(W + "val")) + 1
            numpr = ppr.find("w:numPr", NS)
            if numpr is None or numpr.find("w:numId", NS) is None:
                numpr = self.style_num.get(sid)
        body = self._runs(p)
        if not re.sub(r"<[^>]+>|\s", "", body) and "<img" not in body and "<table" not in body:
            return ""
        if lvl == 0:
            return '<p class="title">%s</p>' % body
        if lvl:
            return "<h%d>%s</h%d>" % (lvl, body, lvl)
        if numpr is not None and numpr.find("w:numId", NS) is not None:
            nid = numpr.find("w:numId", NS).get(W + "val", "0")
            il = numpr.find("w:ilvl", NS).get(W + "val", "0") if numpr.find("w:ilvl", NS) is not None else "0"
            fmt = self.numfmt.get((nid, il), "bullet")
            indent = 14 * (min(int(il), 8) + 1) if il.isdigit() else 14
            if nid != "0":
                if fmt in ("bullet", "none"):
                    mark = "•"
                else:
                    key = (nid, il)
                    self.counters[key] = self.counters.get(key, 0) + 1
                    for k in list(self.counters):         # вложенные уровни начинаются заново
                        if k[0] == nid and k[1].isdigit() and il.isdigit() and int(k[1]) > int(il):
                            self.counters.pop(k)
                    mark = "%d." % self.counters[key]
                return '<p class="li" style="margin-left:%dpt">%s %s</p>' % (indent, mark, body)
        if sid.lower().startswith("caption") or sid.lower().startswith("название"):
            return '<p class="cap">%s</p>' % body
        return "<p>%s</p>" % body

    def _table(self, tbl) -> str:
        self.stats["tables"] += 1
        rows = []
        for tr in tbl.findall("w:tr", NS):
            cells = []
            for tc in tr.findall("w:tc", NS):
                span = tc.find("w:tcPr/w:gridSpan", NS)
                cs = min(63, int(span.get(W + "val", "1"))) if span is not None and span.get(W + "val", "1").isdigit() else 1
                vm = tc.find("w:tcPr/w:vMerge", NS)
                inner = "" if (vm is not None and vm.get(W + "val") in (None, "continue")) else self._blocks(tc)
                inner = re.sub(r"^<p>(.*)</p>$", r"\1", inner, flags=re.S)
                cells.append("<td%s>%s</td>" % (' colspan="%d"' % cs if cs > 1 else "", inner))
            if cells:
                rows.append("<tr>%s</tr>" % "".join(cells))
        return "<table>%s</table>" % "".join(rows) if rows else ""

    def _blocks(self, parent) -> str:
        out = []
        for el in parent:
            if el.tag == W + "p":
                out.append(self._paragraph(el))
            elif el.tag == W + "tbl":
                out.append(self._table(el))
            elif el.tag in (W + "sdt", W + "sdtContent", W + "customXml"):
                out.append(self._blocks(el))
            elif el.tag == "{%s}AlternateContent" % NS["mc"]:
                ch = el.find("mc:Choice", NS)
                if ch is not None:
                    out.append(self._blocks(ch))
        return "".join(out)

    def convert(self) -> str:
        root = self._xml("word/document.xml")
        if root is None:
            raise DocxError("в файле нет word/document.xml — это не документ Word")
        body = root.find("w:body", NS)
        if body is None:
            raise DocxError("в документе нет тела (w:body)")
        out = self._blocks(body)
        if self.notes:
            out += "<h3>Сноски</h3>" + "".join('<p class="fn">%s</p>' % html.escape(n) for n in self.notes)
        return out


def _pct(v: str) -> str:
    try:
        f = float(v) * 100
    except (TypeError, ValueError):
        return v or ""
    return ("%d%%" % round(f)) if abs(f - round(f)) < 1e-9 else ("%.4g%%" % f)


def _num(v: str) -> str:
    if isinstance(v, str) and v.endswith("%"):
        return v
    try:
        f = float(v)
    except (TypeError, ValueError):
        return v or ""
    return ("%d" % f) if f == int(f) and abs(f) < 1e15 else ("%.4g" % f if abs(f) < 1e6 else "%.6g" % f)


def _chart_points(pts) -> dict:
    """Точки ряда диаграммы {idx: значение}. idx из файла не доверяем: нечисловой, отрицательный или
    за пределом MAX_CHART_POINTS отбрасывается — иначе таблица на idx="999999999" съест память."""
    out = {}
    for i, p in enumerate(pts[:MAX_CHART_POINTS * 2]):
        try:
            k = int(p.get("idx", i))
        except (TypeError, ValueError):
            continue
        if 0 <= k < MAX_CHART_POINTS:
            out[k] = p.findtext("c:v", "", NS)
    return out


def check_docx(path: Path) -> zipfile.ZipFile:
    with open(path, "rb") as fh:
        head = fh.read(8)
    if head.startswith(b"\xd0\xcf\x11\xe0"):
        raise DocxError("файл защищён паролем или это старый формат .doc (Word 97–2003): откройте его в Word и "
                        "сохраните как .docx без пароля")
    if not head.startswith(b"PK"):
        raise DocxError("это не DOCX (нет сигнатуры ZIP)")
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile as e:
        raise DocxError("DOCX повреждён: %s" % e) from None
    infos = z.infolist()
    if len(infos) > MAX_MEMBERS or sum(i.file_size for i in infos) > MAX_UNZIPPED_MB * 1e6:
        raise DocxError("DOCX подозрительно велик после распаковки — не обрабатывается")
    names = {i.filename for i in infos}
    if "word/document.xml" not in names:
        raise DocxError("в файле нет word/document.xml — это не документ Word (возможно, Excel или PowerPoint)")
    if any(i.flag_bits & 0x1 for i in infos):
        raise DocxError("части DOCX зашифрованы")
    return z


def _core_props(z: zipfile.ZipFile) -> dict:
    try:
        root = ET.fromstring(z.read("docProps/core.xml"))
    except (KeyError, ET.ParseError):
        return {}
    out = {}
    for el in root:
        tag = el.tag.split("}")[-1]
        if tag in ("title", "creator", "created") and (el.text or "").strip():
            out[{"creator": "author"}.get(tag, tag)] = el.text.strip()
    return out


def convert(pymupdf, src: Path, dst: Path) -> dict:
    """DOCX → PDF (A4). Возвращает сведения о переносе: страницы, таблицы, рисунки, предупреждения."""
    z = check_docx(src)
    with z:
        conv = _Converter(z)
        body = conv.convert()
        props = _core_props(z)
    if len(body) > MAX_HTML_CHARS:
        raise DocxError("DOCX после разбора слишком велик для перевода в PDF — пришлите PDF")
    if not re.sub(r"<[^>]+>|\s", "", body):
        raise DocxError("в документе нет текста")
    doc_html = "<body>%s</body>" % body
    arch = pymupdf.Archive()
    for data, name in conv.images:
        arch.add((data, name))
    story = pymupdf.Story(html=doc_html, user_css=CSS, archive=arch)
    mediabox = pymupdf.paper_rect("a4")
    where = mediabox + (54, 54, -54, -54)
    buf = io.BytesIO()
    writer = pymupdf.DocumentWriter(buf)
    more, pages = 1, 0
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
        pages += 1
        if pages > 3000:
            raise DocxError("документ слишком велик для перевода в PDF")
    writer.close()
    out = pymupdf.open("pdf", buf.getvalue())
    meta = {"title": props.get("title", ""), "author": props.get("author", ""), "creator": "ai-summary-one-page-ver-2: DOCX → PDF",
            "creationDate": "", "modDate": "", "subject": "", "keywords": "", "producer": "PyMuPDF Story"}
    out.set_metadata(meta)
    part = dst.with_suffix(".pdf.part")
    out.save(part, garbage=3, deflate=True)
    out.close()
    part.replace(dst)
    warnings = []
    if conv.stats["images_skipped"]:
        warnings.append("рисунков EMF/WMF не перенесено: %d" % conv.stats["images_skipped"])
    return {"pages": pages, **conv.stats, "doc_title": props.get("title", ""), "doc_author": props.get("author", ""),
            "doc_created": props.get("created", ""), "warnings": warnings}
