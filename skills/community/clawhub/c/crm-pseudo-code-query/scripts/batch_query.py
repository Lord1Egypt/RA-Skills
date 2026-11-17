#!/usr/bin/env python3
"""
CRM 批量查询伪码
用法: python3 batch_query.py --cert <cert.pem> --password <pwd> <userid1> [userid2] ...
示例: python3 batch_query.py --cert ~/my_cert.pem --password <你的CRM密码> 11010686 485462305

前置条件:
  1. mTLS 客户端证书已从 macOS Keychain 导出（详见 SKILL.md）
  2. HexinCA 根证书已添加为受信任根
  3. curl 命令行工具可用
"""
import subprocess
import re
import time
import os
import sys
import argparse
from pathlib import Path

# ─── 参数解析 ───
parser = argparse.ArgumentParser(description="CRM 批量查询伪码")
parser.add_argument("userids", nargs="+", help="要查询的 userid 列表")
parser.add_argument("--cert", required=True, help="mTLS 客户端证书文件路径 (含证书+私钥的 PEM)")
parser.add_argument("--password", required=True, help="CRM 登录密码")
parser.add_argument("--output", default="伪码查询结果.txt", help="结果输出文件路径 (默认: 当前目录)")
args = parser.parse_args()

CERT = args.cert
PASSWORD = args.password
USERIDS = args.userids
OUTPUT_FILE = args.output

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
JAR = "/tmp/crm_final_jar.txt"


def curl(url, extra_args=None, timeout=30):
    """Execute a curl request with mTLS cert and return stdout bytes."""
    cmd = [
        "curl", "-s", "-k",
        "--cert", CERT, "--key", CERT,
        "--noproxy", "*",
        "-A", UA,
        "--connect-timeout", "15",
        "--max-time", str(timeout),
        "-b", JAR, "-c", JAR,
    ]
    if extra_args:
        cmd += extra_args
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
    return result.stdout


def login():
    """Three-step CRM authentication. Returns True on success."""
    # Step 1: GET login page — obtain initial PHPSESSID
    curl("https://crm.10jqka.com.cn/gb_v3/default/index/login")

    # Step 2: GET auth API — validate password, obtain crm_user_token
    curl(f"https://crm.10jqka.com.cn/auth/crm/cloud-software/auth/login?password={PASSWORD}&mailFlag=0&email=")

    # Step 3: POST form — create authenticated session
    stdout = curl("https://crm.10jqka.com.cn/gb_v3/default/index/login", extra_args=[
        "-X", "POST",
        "-d", f"state=1&oldurl=&mailFlag=0&password=*&si_passwd={PASSWORD}",
    ])
    html = stdout.decode("gbk", errors="replace")
    return "登录成功" in html


def extract_pseudo_codes(html):
    """Extract all pseudo codes (format #数字#) from a CRM client detail page."""
    results = []

    # Method 1: labeled fake_tel inputs
    pattern = re.compile(
        r'<font[^>]*>([^<]*)</font>\s*<input[^>]*class="fake_tel"[^>]*value="#(\d+)#"',
        re.DOTALL
    )
    for m in pattern.finditer(html):
        label = m.group(1).strip()
        code = m.group(2)
        results.append({"label": label, "code": f"#{code}#"})

    # Method 2: unlabeled fake_tel inputs
    if not results:
        pattern2 = re.compile(r'<input[^>]*class="fake_tel"[^>]*value="#(\d+)#"', re.DOTALL)
        for m in pattern2.finditer(html):
            results.append({"label": "未知", "code": f"#{m.group(1)}#"})

    # Method 3: fallback — any #number# pattern
    if not results:
        for m in re.finditer(r'#(\d{2,})#', html):
            results.append({"label": "fallback", "code": f"#{m.group(1)}#"})

    return results


def main():
    # Validate cert file
    if not os.path.exists(CERT):
        print(f"错误: 证书文件不存在: {CERT}")
        print("请先从 Keychain 导出 mTLS 客户端证书，详见 SKILL.md")
        sys.exit(1)

    print("=" * 60)
    print("CRM 批量查询伪码")
    print("=" * 60)

    # Login
    print("\n  登录 CRM...")
    if login():
        print("   登录成功！")
    else:
        print("   登录失败！请检查证书和密码。")
        sys.exit(1)

    # Batch query
    print(f"\n  开始查询 {len(USERIDS)} 个 userid...\n")

    all_results = {}
    for i, userid in enumerate(USERIDS, 1):
        url = f"https://crm.10jqka.com.cn/gb_v3/default/account/clientsdetailsinformation?ai_userid={userid}"
        stdout = curl(url)
        html = stdout.decode("gbk", errors="replace")

        # Check for session expiry
        if "登录成功" not in html and ("index/login" in html or "请输入密码" in html or len(html) < 500):
            print(f"  [{i:>2}/{len(USERIDS)}] userid={userid:>12s}  会话过期，重新登录...")
            login()
            stdout = curl(url)
            html = stdout.decode("gbk", errors="replace")

        codes = extract_pseudo_codes(html)

        if codes:
            code_strs = [c["code"] for c in codes]
            print(f"  [{i:>2}/{len(USERIDS)}] userid={userid:>12s}  {', '.join(code_strs)}")
            for c in codes:
                print(f"         - {c['label']}: {c['code']}")
            all_results[userid] = codes
        else:
            print(f"  [{i:>2}/{len(USERIDS)}] userid={userid:>12s}  未找到伪码 (页面大小: {len(html)})")
            all_results[userid] = []

        time.sleep(0.3)

    # Summary
    print("\n" + "=" * 60)
    print("查询结果汇总")
    print("=" * 60)
    print(f"{'userid':>14s}  |  伪码")
    print("-" * 50)
    for userid in USERIDS:
        codes = all_results.get(userid, [])
        if codes:
            code_str = ", ".join([c["code"] for c in codes])
            print(f"{userid:>14s}  |  {code_str}")
        else:
            print(f"{userid:>14s}  |  (无)")

    # Save to file
    with open(OUTPUT_FILE, "w") as f:
        f.write("伪码查询结果\n")
        f.write(f"查询时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        for userid in USERIDS:
            codes = all_results.get(userid, [])
            if codes:
                for c in codes:
                    f.write(f"userid={userid}\t{c['label']}\t伪码={c['code']}\n")
            else:
                f.write(f"userid={userid}\t(未找到伪码)\n")
    print(f"\n结果已保存: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
