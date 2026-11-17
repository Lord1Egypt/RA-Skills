#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ggb_patch —— 为 .ggb 注入按钮/更新脚本。

背景（真机实测）：本引擎经 evalCommand 无法创建「带脚本的按钮」
（Button("标题","脚本") 静默失败）；桌面版按钮脚本在 .ggb 内以
<ggbscript val="…"/>（点击）与 <ggbscript onUpdate="…"/>（更新）存储。
本工具在导出后的 .ggb 上直接注入脚本（结构与桌面版一致）。

用法：
    python ggb_patch.py --ggb <输入.ggb> --spec <脚本清单.json> --out <输出.ggb>
                        [--report <报告.json>]

spec 格式（JSON 数组）：
[
  {"label": "btnReset", "event": "onClick",
   "script": "SetValue(a, 1)\\nSetValue(h, 0.8)"},
  {"label": "kk", "event": "onUpdate", "script": "…"}
]
- label：目标对象名（按钮、滑块等）
- event：onClick（点击触发）或 onUpdate（对象更新时触发）
- script：GGBScript 文本；多语句用换行（\\n）
"""
import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from xml.sax.saxutils import escape

ESCAPES = {'"': '&quot;', '\n': '&#xa;', '\r': ''}


def patch_xml(xml, label, event, script):
    tag = re.compile(r'<element\b[^>]*label="%s"[^>]*>' % re.escape(label))
    m = tag.search(xml)
    if not m:
        return xml, "SKIP: 未找到 label=%s 的 element" % label
    start = m.start()
    end = xml.find("</element>", start)
    if end < 0:
        return xml, "SKIP: label=%s 的 element 不是配对结构（可能自闭合）" % label
    seg = xml[start:end]
    val = escape(script, ESCAPES)
    if event == "onClick":
        inject = '<ggbscript val="%s"/>' % val
    elif event == "onUpdate":
        inject = '<ggbscript onUpdate="%s"/>' % val
    else:
        return xml, "SKIP: 未知 event=%s（仅支持 onClick / onUpdate）" % event
    existing = re.search(r"<ggbscript\b[^>]*/>", seg)
    if existing:
        seg_new = seg[:existing.start()] + inject + seg[existing.end():]
        action = "REPLACE"
    else:
        seg_new = seg + "\t" + inject + "\n"
        action = "INJECT"
    return xml[:start] + seg_new + xml[end:], "%s: %s (%s)" % (action, label, event)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ggb", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    spec = json.load(open(args.spec, encoding="utf-8"))
    zin = zipfile.ZipFile(args.ggb)
    xml = zin.read("geogebra.xml").decode("utf-8")

    results = []
    for item in spec:
        xml, note = patch_xml(xml, item["label"], item.get("event", "onClick"), item["script"])
        results.append(note)

    tmp = args.out + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in zin.namelist():
            if name == "geogebra.xml":
                zout.writestr(name, xml.encode("utf-8"))
            else:
                zout.writestr(name, zin.read(name))
    zin.close()
    shutil.move(tmp, args.out)

    report = {"ok": all(r.startswith(("INJECT", "REPLACE")) for r in results) if results else False,
              "patched": sum(1 for r in results if r.startswith(("INJECT", "REPLACE"))),
              "details": results, "out": os.path.abspath(args.out)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.report:
        json.dump(report, open(args.report, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
