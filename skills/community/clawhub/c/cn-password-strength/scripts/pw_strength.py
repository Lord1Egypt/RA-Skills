#!/usr/bin/env python3
"""Password strength estimator (stdlib only)."""
import sys, math, argparse, re

COMMON = {"123456","password","12345678","qwerty","111111","abc123","admin","letmein","iloveyou","000000"}

def score(pw):
    issues = []
    if len(pw) < 8:
        issues.append("长度不足8位")
    classes = sum([
        bool(re.search(r'[a-z]', pw)),
        bool(re.search(r'[A-Z]', pw)),
        bool(re.search(r'\d', pw)),
        bool(re.search(r'[^A-Za-z0-9]', pw)),
    ])
    pool = 0
    if re.search(r'[a-z]', pw): pool += 26
    if re.search(r'[A-Z]', pw): pool += 26
    if re.search(r'\d', pw): pool += 10
    if re.search(r'[^A-Za-z0-9]', pw): pool += 33
    entropy = len(pw) * math.log2(pool) if pool else 0
    if classes < 3:
        issues.append("字符种类少于3类")
    if pw.lower() in COMMON:
        issues.append("命中常见弱密码库")
    if re.search(r'(.)\1\1', pw):
        issues.append("存在3位以上重复字符")
    if re.search(r'(012|123|234|345|456|567|678|789|abc|bcd|cde)', pw.lower()):
        issues.append("存在连续序列")
    s = int(min(entropy / 4, 25)) * 4
    s = max(0, min(100, s))
    rating = "弱" if s < 40 else "中" if s < 65 else "强" if s < 85 else "极强"
    return s, rating, entropy, issues

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("password", nargs="?")
    ap.add_argument("--check-list")
    args = ap.parse_args()
    if args.check_list:
        with open(args.check_list, encoding="utf-8") as f:
            for line in f:
                pw = line.strip()
                if pw:
                    s, r, e, iss = score(pw)
                    print(f"{r:>2} ({s:3}/100, {e:.1f}bit) {pw}  {'; '.join(iss)}")
        return
    if not args.password:
        print("用法: pw_strength.py <密码> [--check-list 文件]")
        return
    s, r, e, iss = score(args.password)
    print(f"评级: {r}")
    print(f"评分: {s}/100")
    print(f"熵值: {e:.1f} bit")
    if iss:
        print("问题: " + "; ".join(iss))
    else:
        print("无明显弱点 ✅")

if __name__ == "__main__":
    main()
