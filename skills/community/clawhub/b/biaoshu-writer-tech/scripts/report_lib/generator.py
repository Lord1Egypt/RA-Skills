"""Report generation entrypoints."""

import argparse
import json
import os
from datetime import datetime

from .common import _LABEL, _auto_tender_name, _safe_name, _unwrap
from .renderers import RENDERERS
from .writers import build_docx


def generate(data, service=None, fmt="html", out_dir=".", basename=None, tender_name=None):
    """Render report files and return output paths."""
    detected, result = _unwrap(data)
    service = service or detected
    if service not in RENDERERS:
        raise ValueError(f"未知 service：{service}（应为 interpretation / compliance / bid_duplicate）")
    html, blocks = RENDERERS[service](result)
    os.makedirs(out_dir, exist_ok=True)
    label = _LABEL[service]
    tender_name = tender_name or _auto_tender_name(service, result)
    if basename:
        base = basename
    elif tender_name:
        base = f"{_safe_name(tender_name)}_{label}"
    else:
        base = f"{label}_{datetime.now():%Y%m%d_%H%M%S}"
    outs = []
    if fmt in ("html", "both"):
        p = os.path.join(out_dir, base + ".html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        outs.append(p)
    if fmt in ("docx", "both"):
        p = os.path.join(out_dir, base + ".docx")
        with open(p, "wb") as f:
            f.write(build_docx(blocks))
        outs.append(p)
    return outs


def main():
    ap = argparse.ArgumentParser(description="把解读/合规/查重结果 JSON 渲染成 HTML/Word 报告")
    ap.add_argument("--in", dest="infile", required=True, help="结果 JSON 文件（/result 响应或 result 体）")
    ap.add_argument("--service", choices=["interpretation", "compliance", "bid_duplicate"], help="不指定则自动识别")
    ap.add_argument("--format", choices=["html", "docx", "both"], default="html",
                    help="默认 html；要 Word 传 docx 或 both")
    ap.add_argument("-o", "--out-dir", default=".", help="输出目录")
    ap.add_argument("--basename", help="完整文件名（不含扩展名），优先级最高")
    ap.add_argument("--tender-name", help="招标文件名，用于默认命名 招标文件名_{智能解读|合规审查}")
    args = ap.parse_args()
    with open(args.infile, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in generate(data, service=args.service, fmt=args.format,
                      out_dir=args.out_dir, basename=args.basename, tender_name=args.tender_name):
        print(p)
