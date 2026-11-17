#!/usr/bin/env python3
"""
doc_reader.py - One-stop AI bid-document speed-read (BidHunter v2.0, B1+B2).

Pipeline:
  1. parse document text (PDF/DOCX/TXT)         -> doc_parser
  2. extract structured clauses via MiniMax     -> clause_extractor
  3. scan exclusionary / pre-determined risk     -> risk_scanner
Prints a clean 速读报告. Requires MiniMax key for step 2; step 1 & 3 work
offline (rule-based) and degrade gracefully when no key is set.

Usage:
  python3 doc_reader.py <招标文件.pdf|docx|txt> [--llm]
  python3 doc_reader.py 招标文件.pdf --llm        # LLM-assisted risk scan too
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))  # for minimax_client import path

from doc_parser import parse as parse_doc
from risk_scanner import rule_scan, llm_scan


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 doc_reader.py <file> [--llm]", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    use_llm = "--llm" in sys.argv[2:]
    if not os.path.exists(path):
        print(f"文件不存在: {path}", file=sys.stderr)
        sys.exit(1)

    text, backend = parse_doc(path)
    print("=" * 54)
    print(f"📄 AI 速读 · {os.path.basename(path)}")
    print(f"   解析后端: {backend} | 文本长度: {len(text)} 字")
    print("=" * 54)

    if not text:
        print("⚠️ 未能提取文本。请安装解析依赖：pip install PyPDF2 python-docx")
        sys.exit(1)

    # Step 2: structured extraction (needs MiniMax)
    clauses = None
    try:
        from clause_extractor import extract
        clauses = extract(text)
        print("\n【结构化抽取】")
        print(json.dumps(clauses, ensure_ascii=False, indent=2))
    except Exception as e:
        print("\n【结构化抽取】⚠️ 跳过（需配置 MiniMax API Key）")
        print(f"   原因: {e}")
        print("   配置: 在 ~/.config/bidhunter/ai.json 写入 {\"api_key\":\"...\"}")

    # Step 3: risk scan
    print("\n【风险条款扫描】")
    findings = rule_scan(text)
    if use_llm:
        findings += llm_scan(text)
    if not findings:
        print("  ✅ 未发现明显排他/内定倾向条款（规则层）。")
    else:
        for f in findings:
            icon = {"high": "🔴", "medium": "🟡", "low": "🟢", "info": "ℹ️"}.get(f["severity"], "•")
            print(f"  {icon} [{f['severity']}] {f['type']}")
            if f.get("snippet"):
                print(f"     …{f['snippet']}…")

    print("\n" + "=" * 54)
    print("⚠️ 本报告由 AI 自动生成，仅供参考，最终以招标文件原文及人工研判为准。")
    print("=" * 54)


if __name__ == "__main__":
    main()
