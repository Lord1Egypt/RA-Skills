from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import fitz

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_CSV = ROOT / "references" / "glossary.csv"

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN_RE = re.compile(r"[A-Za-z]")
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
DICE_RE = re.compile(r"\b\d*d\d+\b", re.I)
URL_RE = re.compile(r"^(?:https?://|www\.)\S+$", re.I)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
BULLET_RE = re.compile(r"^\s*(?:[•·▪▫◦‣⁃●○◆◇■□►▶\-–—*]|\(?\d{1,2}[.)])\s*")
PRIVATE_USE_RE = re.compile(r"[\ue000-\uf8ff]")

LIGATURES = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
    "\ufb05": "st",
    "\ufb06": "st",
}

WRONG_LEVEL = "error"
AVOID_LEVEL = "warning"


def setup_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


def sRGB_to_rgb(color: int) -> Tuple[float, float, float]:
    return (
        ((color >> 16) & 255) / 255.0,
        ((color >> 8) & 255) / 255.0,
        (color & 255) / 255.0,
    )


def rect_to_list(rect: fitz.Rect) -> List[float]:
    return [round(float(rect.x0), 2), round(float(rect.y0), 2),
            round(float(rect.x1), 2), round(float(rect.y1), 2)]


def list_to_rect(values: Sequence[float]) -> fitz.Rect:
    return fitz.Rect(float(values[0]), float(values[1]),
                     float(values[2]), float(values[3]))


def union_rects(rects: Sequence[fitz.Rect]) -> fitz.Rect:
    if not rects:
        return fitz.Rect()
    result = fitz.Rect(rects[0])
    for rect in rects[1:]:
        result |= rect
    return result


def rect_area(rect: fitz.Rect) -> float:
    return max(0.0, rect.width) * max(0.0, rect.height)


def overlap_area(a: fitz.Rect, b: fitz.Rect) -> float:
    inter = a & b
    if inter.is_empty:
        return 0.0
    return max(0.0, inter.width) * max(0.0, inter.height)


def safe_expand(rect: fitz.Rect, pad: float) -> fitz.Rect:
    return fitz.Rect(rect.x0 - pad, rect.y0 - pad, rect.x1 + pad, rect.y1 + pad)


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", "", (text or "").replace(chr(0x2060), "").replace(chr(0x200b), ""))


def clean_text(text: str) -> str:
    text = text or ""
    text = unicodedata.normalize("NFC", text)
    for src, dst in LIGATURES.items():
        text = text.replace(src, dst)
    text = text.replace("\u00ad", "")
    text = text.replace("\ufeff", "")
    text = text.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "")
    text = text.replace("\u00a0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def has_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text or ""))


def cjk_ratio(text: str) -> float:
    letters = [ch for ch in (text or "") if not ch.isspace()]
    if not letters:
        return 0.0
    return sum(1 for ch in letters if CJK_RE.match(ch)) / len(letters)


def latin_ratio(text: str) -> float:
    letters = [ch for ch in (text or "") if not ch.isspace()]
    if not letters:
        return 0.0
    return sum(1 for ch in letters if LATIN_RE.match(ch)) / len(letters)


def is_pure_number_or_symbol(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    if not re.search(r"\d", t):
        return False
    return bool(re.fullmatch(r"[\d\s.,:;%+\-–—/×xX()\[\]]+", t))


def is_probably_keep(text: str, repeated_header: bool = False) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    if URL_RE.match(t) or EMAIL_RE.match(t):
        return True
    if is_pure_number_or_symbol(t):
        return True
    if DICE_RE.fullmatch(t):
        return True
    if PRIVATE_USE_RE.search(t):
        return True
    if cjk_ratio(t) >= 0.4:
        return True
    if t.startswith(("©", "(c)", "Copyright", "All rights reserved")):
        return True
    if repeated_header and len(t) <= 80:
        return True
    return False


def join_line_texts(texts: Sequence[str]) -> str:
    if not texts:
        return ""
    result = clean_text(texts[0]).strip()
    for raw in texts[1:]:
        nxt = clean_text(raw).strip()
        if not nxt:
            continue
        if not result:
            result = nxt
            continue
        if result.endswith("-") and re.match(r"[a-z]", nxt):
            result = result[:-1] + nxt
            continue
        if has_cjk(result[-1:]) or has_cjk(nxt[:1]):
            result += nxt
        elif BULLET_RE.match(result) and len(result) <= 4:
            result = result + " " + nxt
        elif result.endswith(("（", "(", "《", "「", "『", "【", "“")):
            result += nxt
        else:
            result += " " + nxt
    result = re.sub(r"[ \t]+", " ", result).strip()
    result = re.sub(r"\s+([,.;:!?，。；：！？])", r"\1", result)
    return result


def read_tsv_map(path: Path) -> Tuple[Dict[str, str], List[str]]:
    """Read id<TAB>value. Returns (mapping, problems). Lines with a bare id map to ''."""
    mapping: Dict[str, str] = {}
    problems: List[str] = []
    if not path.exists():
        return mapping, problems
    with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        for lineno, line in enumerate(handle, 1):
            raw = line.rstrip("\n").rstrip("\r")
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if "\t" not in raw:
                if re.fullmatch(r"[A-Za-z0-9_\-]+", raw.strip()):
                    mapping[raw.strip()] = ""
                else:
                    problems.append(f"第{lineno}行缺少制表符（id<TAB>译文）：{raw[:60]}")
                continue
            sid, value = raw.split("\t", 1)
            sid = sid.strip()
            if not sid:
                problems.append(f"第{lineno}行 id 为空")
                continue
            if sid in mapping:
                problems.append(f"第{lineno}行 id 重复：{sid}")
            value = value.replace("\t", " ").strip()
            if "\n" in value:
                value = " ".join(value.splitlines()).strip()
            mapping[sid] = value
    return mapping, problems


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, default=str)
        handle.write("\n")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@dataclass
class GlossaryTerm:
    en: str
    zh: str
    avoid: str
    wrong: str
    category: str
    note: str
    regex: Optional[re.Pattern] = None

    def variants(self, value: str) -> List[str]:
        return [part.strip() for part in (value or "").split(";") if part.strip()]

    @property
    def zh_variants(self) -> List[str]:
        return [part.strip() for part in (self.zh or "").split("/") if part.strip()]


def _term_pattern(term: str) -> str:
    escaped = re.escape(term)
    escaped = escaped.replace(r"\ ", r"[\s\-]+")
    if re.search(r"[A-Za-z]$", term):
        escaped += r"(?:s|es|ed|ing)?"
    return escaped


def load_glossary(path: Path = GLOSSARY_CSV) -> List[GlossaryTerm]:
    terms: List[GlossaryTerm] = []
    if not path.exists():
        return terms
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not row or not (row.get("en") or "").strip():
                continue
            term = GlossaryTerm(
                en=row["en"].strip(),
                zh=(row.get("zh") or "").strip(),
                avoid=(row.get("avoid") or "").strip(),
                wrong=(row.get("wrong") or "").strip(),
                category=(row.get("category") or "").strip(),
                note=(row.get("note") or "").strip(),
            )
            term.regex = re.compile(
                r"(?<![A-Za-z0-9])" + _term_pattern(term.en) + r"(?![A-Za-z0-9])",
                re.IGNORECASE,
            )
            terms.append(term)
    return terms


class GlossaryIndex:
    def __init__(self, terms: Sequence[GlossaryTerm]):
        self.terms = list(terms)
        sorted_terms = sorted(
            enumerate(self.terms), key=lambda item: len(item[1].en), reverse=True
        )
        self._sorted_ids = [idx for idx, _ in sorted_terms]
        parts = []
        for name_idx, term in sorted_terms:
            parts.append(f"(?P<t{name_idx}>{_term_pattern(term.en)})")
        if parts:
            self._combined = re.compile(
                r"(?<![A-Za-z0-9])(?:" + "|".join(parts) + r")(?![A-Za-z0-9])",
                re.IGNORECASE,
            )
        else:
            self._combined = None

    def find(self, text: str) -> List[Tuple[GlossaryTerm, str, int, int]]:
        if not self._combined or not text:
            return []
        found: List[Tuple[GlossaryTerm, str, int, int]] = []
        seen = set()
        for match in self._combined.finditer(text):
            group = match.lastgroup
            if not group:
                continue
            idx = int(group[1:])
            term = self.terms[idx]
            key = (idx, match.group(0).lower())
            if key in seen:
                continue
            seen.add(key)
            found.append((term, match.group(0), match.start(), match.end()))
        found.sort(key=lambda item: item[2])
        return found


@dataclass
class FontChoice:
    regular: fitz.Font
    bold: fitz.Font
    regular_path: Optional[str]
    bold_path: Optional[str]
    label: str
    builtin: fitz.Font = field(default_factory=lambda: fitz.Font("cjk"))

    def font_for(self, bold: bool) -> fitz.Font:
        return self.bold if bold else self.regular

    def insert_spec(self, bold: bool) -> Tuple[str, Optional[str]]:
        if self.regular_path is None:
            return "china-s", None
        if bold and self.bold_path:
            return "zhbold", self.bold_path
        return "zhbody", self.regular_path

    def covers(self, font: fitz.Font, text: str) -> Tuple[bool, List[str]]:
        missing = []
        for ch in set(text or ""):
            if ch.isspace() or ch in "\u200b\u200c\u200d\ufeff":
                continue
            try:
                if not font.has_glyph(ord(ch)):
                    missing.append(ch)
            except Exception:
                missing.append(ch)
        return not missing, sorted(missing)


def _load_font(path: Optional[str]) -> Optional[fitz.Font]:
    if not path:
        return None
    try:
        return fitz.Font(fontfile=path)
    except Exception:
        return None


def _default_font_candidates() -> List[Tuple[str, str, Optional[str]]]:
    if sys.platform.startswith("win"):
        fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        return [
            ("Microsoft YaHei", str(fonts / "msyh.ttc"), str(fonts / "msyhbd.ttc")),
            ("SimHei", str(fonts / "simhei.ttf"), str(fonts / "simhei.ttf")),
            ("SimSun", str(fonts / "simsun.ttc"), str(fonts / "simsun.ttc")),
        ]
    if sys.platform == "darwin":
        return [
            ("PingFang SC", "/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/PingFang.ttc"),
            ("STHeiti", "/System/Library/Fonts/STHeiti Medium.ttc", "/System/Library/Fonts/STHeiti Medium.ttc"),
            ("Songti SC", "/System/Library/Fonts/Supplemental/Songti.ttc", "/System/Library/Fonts/Supplemental/Songti.ttc"),
        ]
    return [
        ("Noto Sans CJK SC", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
         "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        ("Noto Sans CJK SC", "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
         "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"),
        ("WenQuanYi Zen Hei", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
         "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
    ]


def choose_fonts(regular_path: Optional[str] = None,
                 bold_path: Optional[str] = None) -> FontChoice:
    if regular_path:
        regular = _load_font(regular_path)
        if regular is None:
            raise ValueError(f"无法加载字体：{regular_path}")
        bold = _load_font(bold_path) if bold_path else None
        if bold is None:
            bold = regular
        return FontChoice(
            regular=regular,
            bold=bold,
            regular_path=regular_path,
            bold_path=bold_path if bold is not regular else None,
            label=regular_path,
        )

    for label, reg_path, bold_path_try in _default_font_candidates():
        regular = _load_font(reg_path)
        if regular is None:
            continue
        bold = _load_font(bold_path_try) if bold_path_try else None
        return FontChoice(
            regular=regular,
            bold=bold or regular,
            regular_path=reg_path,
            bold_path=bold_path_try if bold is not None else None,
            label=label,
        )

    builtin = fitz.Font("cjk")
    return FontChoice(
        regular=builtin,
        bold=builtin,
        regular_path=None,
        bold_path=None,
        label="built-in CJK (Droid Sans Fallback)",
        builtin=builtin,
    )


def select_render_font(fonts: FontChoice, text: str, bold: bool
                       ) -> Tuple[fitz.Font, bool, List[str], bool]:
    """Pick a font that covers the text. Returns (font, is_bold, missing, used_builtin)."""
    font = fonts.font_for(bold)
    ok, missing = fonts.covers(font, text)
    if ok:
        return font, bold, [], False
    ok_builtin, missing_builtin = fonts.covers(fonts.builtin, text)
    if ok_builtin:
        return fonts.builtin, False, [], True
    return font, bold, missing, False


def page_image_infos(page: fitz.Page) -> List[Dict[str, Any]]:
    infos = []
    try:
        raw_infos = page.get_image_info(hashes=True)
    except Exception:
        raw_infos = []
    for info in raw_infos:
        digest = info.get("digest")
        digest_hex = ""
        if isinstance(digest, (bytes, bytearray)):
            digest_hex = bytes(digest).hex()
        elif digest:
            digest_hex = str(digest)
        infos.append({
            "bbox": [round(float(v), 2) for v in info.get("bbox", (0, 0, 0, 0))],
            "width": int(info.get("width", 0) or 0),
            "height": int(info.get("height", 0) or 0),
            "colorspace": info.get("cs-name") or info.get("colorspace"),
            "digest": digest_hex,
            "has_mask": bool(info.get("has-mask", False)),
        })
    infos.sort(key=lambda item: (item["digest"], tuple(item["bbox"])))
    return infos


def _canon(value: Any) -> Any:
    if isinstance(value, fitz.Rect):
        return [round(float(v), 2) for v in value]
    if isinstance(value, fitz.Point):
        return [round(float(value.x), 2), round(float(value.y), 2)]
    if isinstance(value, (list, tuple)):
        return [_canon(item) for item in value]
    if isinstance(value, float):
        return round(value, 3)
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return str(value)


def page_drawings(page: fitz.Page) -> Tuple[List[Dict[str, Any]], List[fitz.Rect]]:
    raw = []
    icon_rects: List[fitz.Rect] = []
    try:
        drawings = page.get_drawings()
    except Exception:
        drawings = []
    for drawing in drawings:
        rect = drawing.get("rect")
        if not isinstance(rect, fitz.Rect):
            continue
        fill = drawing.get("fill")
        dtype = drawing.get("type")
        if fill is not None and dtype in ("f", "fs"):
            if rect.width >= 1.5 and rect.height >= 1.5:
                icon_rects.append(fitz.Rect(rect))
        raw.append({
            "type": dtype,
            "rect": _canon(rect),
            "fill": _canon(fill),
            "color": _canon(drawing.get("color")),
            "width": _canon(drawing.get("width")),
            "closePath": drawing.get("closePath"),
            "items": _canon(drawing.get("items") or []),
        })
    payload = json.dumps(raw, sort_keys=True, ensure_ascii=True)
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()
    return raw, icon_rects


def drawings_summary(page: fitz.Page) -> Dict[str, Any]:
    raw, _ = page_drawings(page)
    payload = json.dumps(raw, sort_keys=True, ensure_ascii=True)
    return {
        "count": len(raw),
        "digest": hashlib.sha1(payload.encode("utf-8")).hexdigest(),
    }


def page_geometry(page: fitz.Page) -> Dict[str, Any]:
    return {
        "rect": [round(float(v), 2) for v in page.rect],
        "mediabox": [round(float(v), 2) for v in page.mediabox],
        "cropbox": [round(float(v), 2) for v in page.cropbox],
        "rotation": int(page.rotation),
    }


def media_coverage(page: fitz.Page, images: Sequence[Dict[str, Any]]) -> float:
    page_area = max(1.0, page.rect.width * page.rect.height)
    # Union approximation by sampling a coarse grid; avoids over-counting overlaps.
    grid = 24
    covered = 0
    cells = grid * grid
    for gy in range(grid):
        y = page.rect.y0 + (gy + 0.5) * page.rect.height / grid
        for gx in range(grid):
            x = page.rect.x0 + (gx + 0.5) * page.rect.width / grid
            point = fitz.Point(x, y)
            if any(fitz.Rect(img["bbox"]).contains(point) for img in images):
                covered += 1
    return covered / cells if cells else 0.0


def compute_body_size(segments: Sequence[Dict[str, Any]]) -> float:
    pairs: List[Tuple[float, int]] = []
    for seg in segments:
        if seg.get("table"):
            continue
        size = float(seg.get("font_size") or 0)
        if size < 5 or size > 60:
            continue
        text = seg.get("text") or ""
        weight = max(1, len(text))
        pairs.append((size, weight))
    if not pairs:
        return 10.0
    pairs.sort(key=lambda item: item[0])
    total = sum(weight for _, weight in pairs)
    halfway = total / 2.0
    run = 0
    for size, weight in pairs:
        run += weight
        if run >= halfway:
            return round(size, 2)
    return round(pairs[-1][0], 2)


def make_font_label(fonts: FontChoice) -> str:
    return fonts.label


# ---------- CJK text layout for segments that flow around inline art ----------

CLOSING_PUNCT = set("，。、；：！？）》」』】”’%…—,.;:!?)]}")
OPENING_PUNCT = set("（《「『【“‘([")


def _tokenize(text: str) -> List[str]:
    pattern = re.compile(
        r"[A-Za-z0-9]+(?:[.,:;/%+\-–—][A-Za-z0-9]+)*|\s+|.", re.S
    )
    return pattern.findall(text)


def wrap_text(font: fitz.Font, text: str, fontsize: float, width: float) -> List[str]:
    if width <= 0:
        return [text]
    tokens = _tokenize(text.replace("\n", " "))
    lines: List[str] = []
    current = ""
    current_w = 0.0
    for token in tokens:
        if not token:
            continue
        if token.isspace():
            if current and not current.endswith(" "):
                current += " "
                current_w += font.text_length(" ", fontsize)
            continue
        token_w = font.text_length(token, fontsize)
        if current and current_w + token_w > width + 0.01:
            if token in CLOSING_PUNCT and current_w + token_w <= width + fontsize * 0.4:
                current += token
                current_w += token_w
                continue
            stripped = current.rstrip()
            if stripped and stripped[-1] in OPENING_PUNCT and len(stripped) > 1:
                carry = stripped[-1]
                stripped = stripped[:-1].rstrip()
                if stripped:
                    lines.append(stripped)
                current = carry
                current_w = font.text_length(carry, fontsize)
            else:
                if stripped:
                    lines.append(stripped)
                current = ""
                current_w = 0.0
            if token_w > width:
                for ch in token:
                    ch_w = font.text_length(ch, fontsize)
                    if current and current_w + ch_w > width:
                        lines.append(current.rstrip())
                        current = ch
                        current_w = ch_w
                    else:
                        current += ch
                        current_w += ch_w
            else:
                current = token
                current_w = token_w
        else:
            current += token
            current_w += token_w
    if current.strip():
        lines.append(current.rstrip())
    return [line for line in lines if line.strip()]


def subtract_intervals(start: float, end: float,
                       blocked: Sequence[Tuple[float, float]]) -> List[Tuple[float, float]]:
    intervals = [(start, end)]
    for b0, b1 in sorted(blocked):
        next_intervals = []
        for a0, a1 in intervals:
            if b1 <= a0 or b0 >= a1:
                next_intervals.append((a0, a1))
                continue
            if b0 > a0:
                next_intervals.append((a0, b0))
            if b1 < a1:
                next_intervals.append((b1, a1))
        intervals = next_intervals
        if not intervals:
            break
    return [item for item in intervals if item[1] - item[0] > 0.5]


def layout_around_obstacles(page: fitz.Page, box: fitz.Rect, text: str,
                            font: fitz.Font, fontsize: float, lineheight: float,
                            align: int, color: Sequence[float],
                            obstacles: Sequence[fitz.Rect],
                            insert_name: str,
                            insert_path: Optional[str],
                            pad: float = 0.8) -> Optional[List[fitz.Rect]]:
    """Compute a line layout that avoids obstacles. Draws only if it fits."""
    lines = wrap_text(font, text, fontsize, box.width)
    if not lines:
        return []
    line_h = fontsize * lineheight
    placements: List[Tuple[str, fitz.Rect, float]] = []
    y = box.y0
    max_iterations = max(4, int((box.height + line_h) / max(line_h, 1)) * 3 + 10)
    for _ in range(max_iterations):
        if not lines:
            break
        if y + line_h > box.y1 + 0.01:
            return None
        line = lines[0]
        line_w = font.text_length(line, fontsize)
        band = fitz.Rect(box.x0, y - pad, box.x1, y + line_h + pad)
        blocked: List[Tuple[float, float]] = []
        for rect in obstacles:
            if rect.y1 <= band.y0 or rect.y0 >= band.y1:
                continue
            if rect.x1 <= box.x0 or rect.x0 >= box.x1:
                continue
            blocked.append((rect.x0 - pad, rect.x1 + pad))
        intervals = subtract_intervals(box.x0, box.x1, blocked)
        if not intervals:
            y += line_h
            continue
        fitting = [interval for interval in intervals if interval[1] - interval[0] >= line_w - 0.1]
        if not fitting:
            y += line_h
            continue
        # Prefer the widest interval, then the leftmost among near-equal widths.
        fitting.sort(key=lambda item: (-(item[1] - item[0]), item[0]))
        x0, x1 = fitting[0]
        if align == 1:
            x = x0 + max(0.0, ((x1 - x0) - line_w) / 2.0)
        elif align == 2:
            x = x1 - line_w
        else:
            x = x0
        placements.append((line, fitz.Rect(x, y, x + line_w, y + line_h), y))
        lines.pop(0)
        y += line_h
    if lines:
        return None
    for line, rect, top in placements:
        baseline = top + font.ascender * fontsize
        try:
            if insert_path:
                page.insert_text((rect.x0, baseline), line, fontname=insert_name,
                                 fontfile=insert_path, fontsize=fontsize,
                                 color=color, overlay=True)
            else:
                page.insert_text((rect.x0, baseline), line, fontname=insert_name,
                                 fontsize=fontsize, color=color, overlay=True)
        except Exception:
            return None
    return [rect for _, rect, _ in placements]
