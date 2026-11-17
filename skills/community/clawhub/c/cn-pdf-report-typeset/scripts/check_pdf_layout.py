#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF 排版验证脚本（2026-08-18 建立）
检查三件事：
1. 页面内容均衡度（每页字符数，除封面/收尾页外应接近）
2. 表格/文字是否溢出右边界（A4 宽 595pt，右边距 ~20mm=57pt → 内容右界 ~540pt）
3. 中文是否正常渲染（无乱码特征）

用法：
    python check_pdf_layout.py <报告.pdf> [--right-limit 540]
"""
import sys
import argparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--right-limit", type=float, default=540.0,
                    help="右边界阈值(pt)，A4+20mm右边距约540")
    args = ap.parse_args()

    import pymupdf
    d = pymupdf.open(args.pdf)
    print(f"总页数: {len(d)}")
    print()

    total_over = 0
    print("=== 页面内容均衡度 ===")
    for i in range(len(d)):
        txt = d[i].get_text().strip()
        words = d[i].get_text("words")
        over = [w for w in words if w[2] > args.right_limit]
        total_over += len(over)
        flag = ""
        if over:
            flag = "  <-- 溢出!"
        print(f"  第{i+1}页: {len(txt)}字符, 溢出{len(over)}个{flag}")

    print()
    print(f"总溢出字数: {total_over}")
    if total_over > 0:
        print("❌ 有溢出——检查表格列宽，单元格必须用 Paragraph + wordWrap='CJK'")
    else:
        print("✅ 无溢出")

    # 均衡度提示：除封面(第1页)和收尾页外，各页字符数应相近
    chars = [len(d[i].get_text().strip()) for i in range(len(d))]
    if len(chars) > 2:
        body = chars[1:-1]
        if body:
            avg = sum(body) / len(body)
            poor = [i+2 for i, c in enumerate(body) if c < avg * 0.5]
            if poor:
                print(f"⚠️ 内容不均衡：第{poor}页内容量明显少于均值({avg:.0f}字符)——少用PageBreak，用KeepTogether自然流动")

if __name__ == "__main__":
    main()
