#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf_verify.py —— PDF 交付验真（交付前最后一道关卡）

验真项目：
  V1 文件头 %PDF- 与 %%EOF 结尾
  V2 startxref / xref 表可解析，且偏移量指向真实 obj
  V3 页数符合预期（--pages）
  V4 中文字体已嵌入（/FontFile2 存在且 /Length1 > 1000）
  V5 图表标记数符合预期（--charts，基于内容流 % CHART: 注释）
  V6 表格标记数符合预期（--tables）
  V7 关键词全部可从文本层提取到（--expect-text，验证文字不是图片、且内容正确）
  V8 文本层可提取字符数 > 200（确认是可复制文本而非截图）
  V9 文件大小 > 1KB

用法：
  python pdf_verify.py --self-test
  python pdf_verify.py --pdf 报告.pdf --pages 3 --charts 3 --tables 1 --expect-text "保本ROI" "1.85"
  python pdf_verify.py --pdf 报告.pdf --json-out verify.json
退出码：0 通过；1 未通过；2 参数/文件错误。
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _streams(raw):
    out = []
    pos = 0
    while True:
        s = raw.find(b"stream", pos)
        if s < 0:
            break
        e = raw.find(b"endstream", s)
        if e < 0:
            break
        start = raw.find(b"\n", s)
        start = start + 1 if start >= 0 else s + 6
        if raw[start - 2:start] == b"\r\n":
            pass
        out.append(raw[start:e])
        pos = e + 9
    return out


def _tounicode_map(raw):
    m = {}
    for st in _streams(raw):
        if b"beginbfchar" not in st:
            continue
        try:
            txt = st.decode("latin-1")
        except Exception:
            continue
        for line in txt.splitlines():
            line = line.strip()
            mo = re.match(r"^<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>$", line)
            if mo:
                try:
                    m[int(mo.group(1), 16)] = chr(int(mo.group(2), 16))
                except ValueError:
                    pass
    return m


def extract_text(raw):
    cmap = _tounicode_map(raw)
    chunks = []
    for st in _streams(raw):
        if b"Tj" not in st:
            continue
        try:
            txt = st.decode("latin-1")
        except Exception:
            continue
        for mo in re.finditer(r"<([0-9a-fA-F]+)>\s*Tj", txt):
            h = mo.group(1)
            s = "".join(cmap.get(int(h[i:i + 4], 16), "") for i in range(0, len(h) - 3, 4))
            chunks.append(s)
        for mo in re.finditer(r"\((.*?)\)\s*Tj", txt):
            chunks.append(mo.group(1))
    return "".join(chunks)


def verify(pdf_path, pages=None, charts=None, tables=None, expect_text=None, min_text=200):
    if not os.path.exists(pdf_path):
        return {"ok": False, "checks": [{"id": "V0", "name": "文件存在", "pass": False, "detail": pdf_path}]}
    raw = open(pdf_path, "rb").read()
    checks = []

    def add(i, name, cond, detail=""):
        checks.append({"id": i, "name": name, "pass": bool(cond), "detail": detail})

    add("V1", "文件头与结尾", raw[:5] == b"%PDF-" and b"%%EOF" in raw[-1024:],
        "header=%s" % raw[:8].decode("latin-1", "ignore"))

    m = re.search(rb"startxref\s+(\d+)", raw)
    xref_ok = False
    objs = {}
    if m:
        xpos = int(m.group(1))
        xref_ok = raw[xpos:xpos + 4] == b"xref"
        # xref 条目格式：offset(10) gen(5) n
        for i, (off, gen) in enumerate(re.findall(rb"(\d{10}) (\d{5}) n", raw[xpos:xpos + 40000]), start=1):
            objs[i] = int(off)
    real = 0
    for off in objs.values():
        if off < len(raw) and b" obj" in raw[off:off + 24]:
            head = raw[off:off + 12].split(b" ")[0]
            if head.isdigit():
                real += 1
    add("V2", "xref 可解析且对象可定位", xref_ok and real >= 3, "解析到 %d 个对象，命中 %d" % (len(objs), real))

    npage = len(re.findall(rb"/Type\s*/Page[^s]", raw))
    add("V3", "页数符合预期", (pages is None) or (npage == pages), "实际 %d 页，预期 %s" % (npage, pages))

    fm = re.search(rb"/FontFile2\s+(\d+)\s+0\s+R", raw)
    fsize = 0
    if fm:
        lm = re.search(rb"/Length1\s+(\d+)", raw)
        fsize = int(lm.group(1)) if lm else 0
    add("V4", "中文字体已嵌入", bool(fm) and fsize > 1000, "FontFile2 大小 %d 字节" % fsize)

    nchart = len([c for c in re.findall(rb"% CHART:(\w+):", raw)
                  if c in (b"bar", b"line", b"pie", b"funnel", b"waterfall")])
    ntable = len([c for c in re.findall(rb"% CHART:(\w+):", raw) if c == b"table"])
    add("V5", "图表数符合预期", (charts is None) or (nchart >= charts), "图表 %d，预期 ≥ %s" % (nchart, charts))
    add("V6", "表格数符合预期", (tables is None) or (ntable >= tables), "表格 %d，预期 ≥ %s" % (ntable, tables))

    text = extract_text(raw)
    miss = [t for t in (expect_text or []) if t not in text]
    add("V7", "关键词可从文本层提取", not miss, "缺失：%s" % (miss if miss else "无"))
    add("V8", "文本层可复制（非图片）", len(text) >= min_text, "提取字符数 %d" % len(text))
    add("V9", "文件大小合理", len(raw) > 1024, "%.1f KB" % (len(raw) / 1024))

    ok = all(c["pass"] for c in checks)
    return {"ok": ok, "path": pdf_path, "bytes": len(raw), "pages": npage, "charts": nchart,
            "tables": ntable, "text_len": len(text), "checks": checks}


def render(res):
    o = ["【PDF 验真】%s → %s" % (os.path.basename(res["path"]), "PASS" if res["ok"] else "FAIL")]
    for c in res["checks"]:
        o.append("  [%s] %s %-22s %s" % ("√" if c["pass"] else "×", c["id"], c["name"], c["detail"]))
    return "\n".join(o)


def self_test() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    import report_pdf
    tmp = os.path.join(report_pdf._tmp_dir(), "_pdf_verify_selftest.pdf")
    info = report_pdf.build(report_pdf.DEMO_SPEC, tmp)
    res = verify(tmp, pages=info["pages"], charts=3, tables=1, expect_text=["保本", "1.85", "毛利率"])
    print("   " + render(res).replace("\n", "\n   "))
    chk("demo PDF 验真通过", res["ok"])
    chk("页数一致", res["pages"] == info["pages"])
    chk("图表数 >= 3", res["charts"] >= 3)
    # 反向用例：故意要求不存在的关键词
    bad = verify(tmp, expect_text=["这句话不可能出现在报告里"])
    chk("缺失关键词 → 判定 FAIL", not bad["ok"])
    chk("不存在文件 → 判定 FAIL", not verify(os.path.join(tmp, "nope.pdf"))["ok"])
    try:
        os.remove(tmp)
    except OSError:
        pass
    print("pdf_verify self-test: %s" % ("ALL PASS" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="PDF 交付验真")
    ap.add_argument("--pdf")
    ap.add_argument("--pages", type=int)
    ap.add_argument("--charts", type=int)
    ap.add_argument("--tables", type=int)
    ap.add_argument("--expect-text", nargs="*", default=[])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--json-out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.pdf:
        ap.error("需要 --pdf 或 --self-test")
    res = verify(a.pdf, a.pages, a.charts, a.tables, a.expect_text)
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else render(res))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
