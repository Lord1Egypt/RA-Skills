#!/usr/bin/env python3
"""estimate_tokens.py — 估算文本 Token 数(与 SKILL.md 的估算规则一致)

规则:
  - CJK(中日韩字符)  : 字符数 × 1.25 (区间 1.0~1.5 的中位近似)
  - ASCII 连续文本    : 字符数 ÷ 4
  - 代码/JSON 等高密度: 字符数 ÷ 3 (由调用方传 --code 或按内容自动判断)
  - 其他 Unicode      : 字符数 × 0.6

用法:
  echo "要估算的文本" | python3 estimate_tokens.py
  python3 estimate_tokens.py --file transcript.jsonl
  python3 estimate_tokens.py --text "一段文本"
  python3 estimate_tokens.py --code 'def foo(): pass'

输出: 单个整数(估算 Token 数)。所有结果均为估算值,SKILL.md 要求报告中以"≈"呈现。
"""
import argparse
import json
import sys

def _count_cjk(s: str) -> int:
    n = 0
    for ch in s:
        o = ord(ch)
        if (0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or
            0x3040 <= o <= 0x30FF or 0xAC00 <= o <= 0xD7AF or
            0xF900 <= o <= 0xFAFF):
            n += 1
    return n

def estimate(text: str, force_code: bool = False) -> int:
    if not text:
        return 0
    total = len(text)
    cjk = _count_cjk(text)
    rest = total - cjk
    # 代码判断:传了 --code,或代码特征密度高(花括号/分号/等号占比)
    if not force_code and rest > 0:
        density = sum(text.count(c) for c in "{};=()[]<>") / max(rest, 1)
        force_code = density > 0.08
    tokens = cjk * 1.25
    if rest:
        tokens += rest / (3 if force_code else 4)
    return max(1, round(tokens))

def main():
    ap = argparse.ArgumentParser(description="估算文本 Token 数(估算值)")
    ap.add_argument("--text", help="直接传入文本")
    ap.add_argument("--file", help="从文件读取(纯文本或 JSONL)")
    ap.add_argument("--code", help="按代码密度估算的文本")
    ap.add_argument("--jsonl-field", default=None,
                    help="JSONL 模式下抽取每行 JSON 的指定字段路径,如 message.content")
    args = ap.parse_args()

    if args.code:
        print(estimate(args.code, force_code=True)); return
    if args.text:
        print(estimate(args.text)); return
    if args.file:
        texts = []
        with open(args.file, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if args.jsonl_field:
                    try:
                        obj = json.loads(line)
                        cur = obj
                        for key in args.jsonl_field.split("."):
                            if isinstance(cur, dict):
                                cur = cur.get(key)
                            else:
                                cur = None; break
                        if isinstance(cur, str):
                            texts.append(cur)
                        continue
                    except json.JSONDecodeError:
                        pass  # 非法行按纯文本处理
                texts.append(line)
        print(estimate("\n".join(texts))); return
    # 无参数:读 stdin
    print(estimate(sys.stdin.read()))

if __name__ == "__main__":
    main()
