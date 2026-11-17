# -*- coding: utf-8 -*-
"""给AI前脱敏器：交给 AI 之前，先把文本里的敏感信息打码。零依赖。

规则：手机号 / 邮箱 / 证件号(18位) / 银行长号(13-19位) / 指定人名(--names)。
输出：脱敏文本 + 脱敏报告（各类命中数）。--json 给结构化结果。
三律映射：LGD-III 有门禁 —— 交给 AI 前的最后一道脱敏门。

用法：
  python data_minimizer.py --file input.txt --out masked.txt
  python data_minimizer.py --text "找张三 13812345678" --names 张三 李四 --json
"""
import argparse, json, pathlib, re, sys

PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
IDCARD = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")
LONGNUM = re.compile(r"(?<!\d)\d{13,19}(?!\d)")
MASKS = {"phone": "〔手机号〕", "email": "〔邮箱〕", "idcard": "〔证件号〕", "longnum": "〔长号〕", "name": "〔人名〕"}


def mask_phone(m):
    s = m.group(0)
    return s[:3] + "****" + s[-2:]


def mask_id(m):
    s = m.group(0)
    return s[:4] + "***********" + s[-2:]


def run(text, names):
    counts = {}
    def sub(pat, repl, key):
        nonlocal text
        text, n = pat.subn(repl, text)
        counts[key] = counts.get(key, 0) + n
    sub(IDCARD, mask_id, "idcard")          # 先证件（18位含长号前缀，防误吞）
    sub(PHONE, mask_phone, "phone")
    sub(EMAIL, MASKS["email"], "email")
    sub(LONGNUM, MASKS["longnum"], "longnum")
    for nm in names or []:
        if nm:
            sub(re.compile(re.escape(nm)), MASKS["name"], "name")
    return text, counts


def main():
    ap = argparse.ArgumentParser(description="给AI前脱敏器 · 发给 AI 前先脱敏")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="输入文件")
    src.add_argument("--text", help="输入文本（内联 / @文件 / 纯路径）")
    ap.add_argument("--names", nargs="*", default=[], help="要打码的人名/代号")
    ap.add_argument("--out", help="脱敏文本输出路径")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        if a.file:
            text = pathlib.Path(a.file).read_text(encoding="utf-8-sig")
        else:
            q = a.text[1:] if a.text.startswith("@") else a.text
            text = pathlib.Path(q).read_text(encoding="utf-8-sig") if pathlib.Path(q).is_file() else q
    except OSError as e:
        print(f"输入不可读：{e}", file=sys.stderr)
        sys.exit(2)
    masked, counts = run(text, a.names)
    if a.out:
        outp = pathlib.Path(a.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(masked, encoding="utf-8")
    if a.json:
        print(json.dumps({"masked_text": masked, "counts": counts, "out": a.out},
                         ensure_ascii=False, indent=2))
    else:
        print("=== 脱敏文本 ===")
        print(masked)
        print("=== 脱敏报告 ===")
        for k, n in counts.items():
            print(f"  {MASKS.get(k, k)}：{n} 处")
        if a.out:
            print(f"已写出：{a.out}")
    sys.exit(0)


if __name__ == "__main__":
    main()
