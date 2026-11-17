#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""夸克网盘批量下载器（已验证方案，2026-08-29/30）

方案要点（全部实测）：
- 客户端 UA 调 drive-pc.quark.cn/1/clouddrive/file/download 拿直链（绕过 size limit 23018）
- 直链绑定获取 IP，拿直链和下载必须同机
- aria2c -x16 -s16 高并发（单文件 1.8G 约 40 秒）
- 3 路并发（>8 路会触发限流 → 空壳文件）
- 已存在且 ffprobe 完整则跳过（断点续跑安全）

用法：
    python3 quark_download.py files.tsv --cookie cookies.txt --dir 输出目录 [--jobs 3]
    python3 quark_download.py files.tsv --cookie cookies.txt --dir 输出目录 --resume

files.tsv 格式（制表符分隔，无表头）：
    <fid>\t<相对路径/文件名>

凭证文件（Netscape 格式）由 get_quark_cookies.js 导出。
"""
import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import time

QUARK_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) quark-cloud-drive/2.5.56 Chrome/100.0.4896.160 "
            "Electron/18.3.5.12 Safari/537.36 Channel/pckk_other_ch")
DOWNLOAD_API = "https://drive-pc.quark.cn/1/clouddrive/file/download"

def read_tsv(path):
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                items.append((parts[0].strip(), parts[1].strip()))
            else:
                print(f"[warn] 跳过无法解析的行: {line}", flush=True)
    return items

def read_cookie_header(path):
    """Netscape cookie 文件 → Cookie header 字符串"""
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

def get_download_url(fid, cookie_header):
    """客户端 UA 拿直链，返回 (url, filename) 或 None"""
    import requests
    headers = {
        "Cookie": cookie_header,
        "User-Agent": QUARK_UA,
        "Referer": "https://pan.quark.cn/",
        "Content-Type": "application/json",
    }
    r = requests.post(DOWNLOAD_API, headers=headers, json={"fids": [fid]}, timeout=20)
    body = r.text.strip()
    if r.status_code != 200 or ("download_url" not in body and "downloadUrl" not in body):
        # 401 + base64 加密串 = 账号级封禁
        if r.status_code == 401 or "code" in body:
            print(f"[fail] fid={fid} status={r.status_code}（401=可能账号封禁）", flush=True)
        else:
            print(f"[fail] fid={fid} status={r.status_code} body={body[:120]}", flush=True)
        return None, None
    data = r.json()
    item = data.get("data", [{}])[0]
    url = item.get("download_url") or item.get("downloadUrl")
    filename = item.get("file_name") or os.path.basename(url.split("?")[0])
    return url, filename

def is_complete(path):
    """ffprobe 校验：duration 非空且 > 0 视为完整（防 moov atom 缺失空壳）"""
    if not os.path.exists(path) or os.path.getsize(path) < 1024:
        return False
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return False
    try:
        return float(r.stdout.strip()) > 0
    except ValueError:
        return False

def download_one(args):
    fid, relpath, cookie_header, outdir = args
    target = os.path.join(outdir, relpath)
    os.makedirs(os.path.dirname(target), exist_ok=True) if os.path.dirname(relpath) else None
    if is_complete(target):
        print(f"[skip] 已存在且完整: {relpath}", flush=True)
        return True
    url, filename = get_download_url(fid, cookie_header)
    if not url:
        return False
    tmp = target + ".part"
    # aria2c 高并发 + 断点续传 + 16 分片
    cmd = ["aria2c", "-x", "16", "-s", "16", "--continue", "--dir", outdir,
           "--out", relpath, "--file-allocation=none", "--summary-interval=0", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if r.returncode != 0 or not is_complete(target):
        # 空壳清理：分片残留 .aria2
        for p in [target + ".aria2", tmp]:
            if os.path.exists(p):
                os.remove(p)
        print(f"[fail] 下载失败或校验不过: {relpath}", flush=True)
        return False
    print(f"[ok] {relpath} ({os.path.getsize(target)/1024/1024:.0f}MB)", flush=True)
    return True

def main():
    ap = argparse.ArgumentParser(description="夸克网盘批量下载器")
    ap.add_argument("tsv", help="文件清单 TSV（fid\\t相对路径）")
    ap.add_argument("--cookie", required=True, help="Netscape cookie 文件路径")
    ap.add_argument("--dir", required=True, help="输出目录")
    ap.add_argument("--jobs", type=int, default=3, help="并发路数（默认3，>8触发限流）")
    args = ap.parse_args()

    items = read_tsv(args.tsv)
    cookie = read_cookie_header(args.cookie)
    if not items:
        print("清单为空", file=sys.stderr)
        sys.exit(1)
    print(f"共 {len(items)} 个文件，并发 {args.jobs} 路", flush=True)

    os.makedirs(args.dir, exist_ok=True)
    tasks = [(fid, rel, cookie, args.dir) for fid, rel in items]
    ok = fail = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(download_one, t): t for t in tasks}
        for fut in concurrent.futures.as_completed(futs):
            if fut.result():
                ok += 1
            else:
                fail += 1
                print(f"[fail-list] {futs[fut][1]}", flush=True)
    print(f"\n完成：成功 {ok} / 失败 {fail}", flush=True)
    sys.exit(0 if fail == 0 else 1)

if __name__ == "__main__":
    main()
