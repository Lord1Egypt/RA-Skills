# -*- coding: utf-8 -*-
"""从 PDF 提取文本（纯标准库，无第三方依赖）。

适用：Word / WPS / LaTeX 导出的常规 PDF（含压缩对象流、CID 字体 + ToUnicode）。
不适用：扫描件（无文本层）、加密 PDF。

用法：
    python extract_pdf.py 文件.pdf             # 打印
    python extract_pdf.py 文件.pdf 输出.txt     # 写文件

实现要点：
1. 顺序扫描 "N 0 obj"，同时支持 /ObjStm 压缩对象流；
2. 走 /Root → /Pages → /Kids 得到页序；
3. 每页按 /Resources /Font 建立 "字体名 → ToUnicode CMap"，逐段解码；
4. Td/TD/T*/ET 作为换行信号，尽量保留原文分行（选题清单很依赖分行）。
"""
import re
import sys
import zlib


# ---------- 基础对象解析 ----------
class PDF:
    def __init__(self, data):
        self.data = data
        self.objs = {}          # num -> (dict_bytes, stream_bytes|None)
        self._scan()
        self._expand_objstm()

    def _scan(self):
        data, pos, n = self.data, 0, len(self.data)
        pat = re.compile(rb"(?<![0-9])(\d+)\s+(\d+)\s+obj\b")
        while True:
            m = pat.search(data, pos)
            if not m:
                break
            num = int(m.group(1))
            i = m.end()
            s = data.find(b"stream", i)
            e_obj = data.find(b"endobj", i)
            if s != -1 and (e_obj == -1 or s < e_obj):
                dict_part = data[i:s]
                start = s + 6
                if data[start:start + 2] == b"\r\n":
                    start += 2
                elif data[start:start + 1] in (b"\n", b"\r"):
                    start += 1
                e = data.find(b"endstream", start)
                if e == -1:
                    break
                stream = data[start:e]
                if stream.endswith(b"\r\n"):
                    stream = stream[:-2]
                elif stream.endswith((b"\n", b"\r")):
                    stream = stream[:-1]
                self.objs[num] = (dict_part, stream)
                pos = e + 9
            else:
                if e_obj == -1:
                    break
                self.objs[num] = (data[i:e_obj], None)
                pos = e_obj + 6

    def _expand_objstm(self):
        for num, (d, st) in list(self.objs.items()):
            if st is None or b"/ObjStm" not in d:
                continue
            body = self.decode(st, d)
            if body is None:
                continue
            first = re.search(rb"/First\s+(\d+)", d)
            cnt = re.search(rb"/N\s+(\d+)", d)
            if not (first and cnt):
                continue
            first, cnt = int(first.group(1)), int(cnt.group(1))
            header = [int(x) for x in body[:first].split()]
            for k in range(cnt):
                if 2 * k + 1 >= len(header):
                    break
                onum, off = header[2 * k], header[2 * k + 1]
                nxt = header[2 * k + 3] if 2 * k + 3 < len(header) else (len(body) - first)
                seg = body[first + off: first + nxt]
                self.objs.setdefault(onum, (seg, None))

    def decode(self, stream, dict_part):
        if b"/FlateDecode" in dict_part:
            try:
                return zlib.decompress(stream)
            except zlib.error:
                try:
                    return zlib.decompressobj().decompress(stream)
                except Exception:
                    return None
        return stream

    def get(self, num):
        return self.objs.get(num)

    def dict_of(self, num):
        o = self.objs.get(num)
        return o[0] if o else b""

    def stream_of(self, num):
        o = self.objs.get(num)
        if not o or o[1] is None:
            return None
        return self.decode(o[1], o[0])


def find_root(pdf):
    for num, (d, _) in pdf.objs.items():
        if b"/Type" in d and b"/Catalog" in d:
            m = re.search(rb"/Pages\s+(\d+)\s+0\s+R", d)
            if m:
                return int(m.group(1))
    return None


def walk_pages(pdf, node, out, depth=0):
    if depth > 32:
        return
    d = pdf.dict_of(node)
    if b"/Type" in d and b"/Page" in d and b"/Pages" not in d:
        out.append(node)
        return
    m = re.search(rb"/Kids\s*\[(.*?)\]", d, re.S)
    if m:
        for r in re.findall(rb"(\d+)\s+0\s+R", m.group(1)):
            walk_pages(pdf, int(r), out, depth + 1)
    else:
        k = re.search(rb"/Kids\s+(\d+)\s+0\s+R", d)
        if k:
            kd = pdf.dict_of(int(k.group(1)))
            for r in re.findall(rb"(\d+)\s+0\s+R", kd):
                walk_pages(pdf, int(r), out, depth + 1)


# ---------- ToUnicode CMap ----------
def parse_cmap(data):
    m = {}
    if not data:
        return m
    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", data, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            m[int(src, 16)] = _hex2str(dst)
    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", data, re.S):
        for lo, hi, dst in re.findall(
                rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(<[0-9A-Fa-f]+>|\[[^\]]*\])", blk):
            lo, hi = int(lo, 16), int(hi, 16)
            if dst.startswith(b"["):
                items = re.findall(rb"<([0-9A-Fa-f]+)>", dst)
                for k, it in enumerate(items):
                    m[lo + k] = _hex2str(it)
            else:
                base = int(dst[1:-1], 16)
                for k in range(hi - lo + 1):
                    m[lo + k] = chr(base + k)
    return m


def _hex2str(h):
    if isinstance(h, bytes):
        h = h.decode()
    b = bytes.fromhex(h if len(h) % 2 == 0 else "0" + h)
    try:
        return b.decode("utf-16-be")
    except UnicodeDecodeError:
        return ""


# ---------- 内容流 ----------
def unescape(s):
    out, i = bytearray(), 0
    while i < len(s):
        c = s[i]
        if c == 0x5C and i + 1 < len(s):
            n = s[i + 1]
            mp = {0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12,
                  0x28: 40, 0x29: 41, 0x5C: 92}
            if n in mp:
                out.append(mp[n]); i += 2; continue
            if 0x30 <= n <= 0x37:
                oct_digits = s[i + 1:i + 4]
                k = 0
                while k < len(oct_digits) and 0x30 <= oct_digits[k] <= 0x37:
                    k += 1
                out.append(int(oct_digits[:k], 8) & 0xFF)
                i += 1 + k; continue
            i += 2
            continue
        out.append(c); i += 1
    return bytes(out)


STR_RE = re.compile(rb"\((?:\\.|[^\\()])*\)|<[0-9A-Fa-f\s]*>", re.S)


def decode_text(raw, cmap, two_byte):
    if not cmap:
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1", "replace")
    out = []
    if two_byte:
        for i in range(0, len(raw) - 1, 2):
            code = (raw[i] << 8) | raw[i + 1]
            out.append(cmap.get(code, ""))
    else:
        for b in raw:
            out.append(cmap.get(b, ""))
    return "".join(out)


def extract(content, font_map, pdf):
    text, cur, two = [], None, True
    line = []

    def flush():
        if line:
            text.append("".join(line))
            line.clear()

    i, n = 0, len(content)
    while i < n:
        c = content[i:i + 1]
        if c == b"(" or c == b"<":
            m = STR_RE.match(content, i)
            if m:
                s = m.group(0)
                raw = unescape(s[1:-1]) if s[:1] == b"(" else bytes.fromhex(
                    re.sub(rb"\s", b"", s[1:-1]).decode() or "")
                line.append(decode_text(raw, font_map.get(cur, (None, True))[0],
                                        font_map.get(cur, (None, True))[1]))
                i = m.end()
                continue
        m = re.match(rb"/([A-Za-z0-9#\-\+\.]+)\s+[\d\.]+\s+Tf", content[i:i + 60])
        if m:
            cur = m.group(1)
            i += m.end()
            continue
        if content.startswith(b"T*", i) or content.startswith(b"ET", i):
            flush(); i += 2; continue
        m = re.match(rb"(-?[\d\.]+)\s+(-?[\d\.]+)\s+(Td|TD)", content[i:i + 40])
        if m:
            if abs(float(m.group(2))) > 0.5:
                flush()
            i += m.end()
            continue
        i += 1
    flush()
    return "\n".join(text)


def font_table(pdf, resources_dict):
    fonts = {}
    m = re.search(rb"/Font\s*<<(.*?)>>", resources_dict, re.S)
    block = m.group(1) if m else b""
    if not block:
        r = re.search(rb"/Font\s+(\d+)\s+0\s+R", resources_dict)
        if r:
            block = pdf.dict_of(int(r.group(1)))
    for name, num in re.findall(rb"/([A-Za-z0-9#\-\+\.]+)\s+(\d+)\s+0\s+R", block):
        fd = pdf.dict_of(int(num))
        tu = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", fd)
        cmap = parse_cmap(pdf.stream_of(int(tu.group(1)))) if tu else {}
        two = b"/Type0" in fd or b"Identity" in fd or b"CIDFont" in fd
        fonts[name] = (cmap, two)
    return fonts


def pages_text(path):
    pdf = PDF(open(path, "rb").read())
    root = find_root(pdf)
    pages = []
    if root:
        walk_pages(pdf, root, pages)
    if not pages:
        pages = [num for num, (d, _) in pdf.objs.items()
                 if b"/Type" in d and b"/Page" in d and b"/Pages" not in d]
    chunks = []
    for p in pages:
        d = pdf.dict_of(p)
        res = re.search(rb"/Resources\s+(\d+)\s+0\s+R", d)
        resd = pdf.dict_of(int(res.group(1))) if res else d
        fonts = font_table(pdf, resd)
        cs = re.search(rb"/Contents\s+(\d+)\s+0\s+R", d)
        if cs:
            conts = [pdf.stream_of(int(cs.group(1)))]
        else:
            arr = re.search(rb"/Contents\s*\[(.*?)\]", d, re.S)
            conts = [pdf.stream_of(int(x)) for x in re.findall(rb"(\d+)\s+0\s+R", arr.group(1))] if arr else []
        body = b"\n".join([c for c in conts if c])
        if body:
            chunks.append(extract(body, fonts, pdf))
    return "\n\n".join(chunks)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    txt = pages_text(sys.argv[1])
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w", encoding="utf-8").write(txt)
        print("wrote", sys.argv[2], len(txt), "chars")
    else:
        print(txt)
