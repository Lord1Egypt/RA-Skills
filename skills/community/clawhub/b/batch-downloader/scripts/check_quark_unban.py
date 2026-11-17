#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""夸克下载接口解封检测（风控恢复探测）— 已验证 2026-08-30

用法：
    python3 check_quark_unban.py --cookie cookies.txt [--fid 测试文件fid]
    输出：UNBANNED（退出码0）/ STILL_BANNED（1）/ NO_COOKIE（2）/ ERROR（3）

原理：用小文件 fid 调 file/download，200 + download_url = 解封。
"""
import argparse
import os
import sys

try:
    import requests
except ImportError:
    print("缺少 requests 库", file=sys.stderr)
    sys.exit(3)

QUARK_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) quark-cloud-drive/2.5.56 Chrome/100.0.4896.160 "
            "Electron/18.3.5.12 Safari/537.36 Channel/pckk_other_ch")
API = "https://drive-pc.quark.cn/1/clouddrive/file/download"

def read_cookie_header(path):
    pairs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 7 and parts[0] != "":
                pairs.append(f"{parts[5]}={parts[6]}")
    return "; ".join(pairs)

def main():
    ap = argparse.ArgumentParser(description="夸克解封检测")
    ap.add_argument("--cookie", required=True, help="Netscape cookie 文件")
    ap.add_argument("--fid", default="58b1a50e459d4facac2d342b5e7f9b06",
                    help="测试用小文件 fid（默认：夸克网盘使用指南.jpg）")
    args = ap.parse_args()

    if not os.path.exists(args.cookie):
        print("NO_COOKIE", flush=True)
        sys.exit(2)
    ck = read_cookie_header(args.cookie)
    headers = {"Cookie": ck, "User-Agent": QUARK_UA,
               "Referer": "https://pan.quark.cn/", "Content-Type": "application/json"}
    try:
        r = requests.post(API, headers=headers, json={"fids": [args.fid]}, timeout=20)
        body = r.text.strip()
        if r.status_code == 200 and ("download_url" in body or "downloadUrl" in body):
            print("UNBANNED", flush=True)
            print(body[:500], flush=True)
            sys.exit(0)
        print(f"STILL_BANNED status={r.status_code}", flush=True)
        print(body[:120].replace("\n", " "), flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR {e}", flush=True)
        sys.exit(3)

if __name__ == "__main__":
    main()
