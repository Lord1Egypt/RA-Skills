#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""磁力/BT 批量下载器（已验证方案，2026-08-30）

要点（全部实测）：
- aria2c + 79 tracker 增强（ngosang trackers_all.txt），metadata 秒拿
- --seed-time=0 下完即停
- 小体积种子（seeders 5-12 个）反而卡 metadata，别迷信小体积=快
- 反复重启 aria2 会清空 peer 缓存，错误做法；用 --continue 断点续传

用法：
    python3 bt_download.py magnets.txt --dir 下载目录 [--concurrent 5] [--trackers trackers.txt]

magnets.txt 格式：每行一个磁力链接，支持 # 注释。
"""
import argparse
import os
import subprocess
import sys

def read_lines(path):
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

def main():
    ap = argparse.ArgumentParser(description="磁力/BT 批量下载器")
    ap.add_argument("magnets", help="磁力清单文件（每行一个）")
    ap.add_argument("--dir", default="/tmp/bt_dl", help="下载目录")
    ap.add_argument("--concurrent", type=int, default=5, help="最大并发下载数")
    ap.add_argument("--trackers", help="tracker 列表文件（每行一个）")
    ap.add_argument("--split", type=int, default=16, help="每任务分片数")
    args = ap.parse_args()

    magnets = read_lines(args.magnets)
    if not magnets:
        print("磁力清单为空", file=sys.stderr)
        sys.exit(1)
    os.makedirs(args.dir, exist_ok=True)

    cmd = ["aria2c", "--input-file", args.magnets, "--dir", args.dir,
           "--seed-time=0", "--max-concurrent-downloads", str(args.concurrent),
           "--split", str(args.split), "--bt-max-peers=0", "--continue",
           "--file-allocation=none", "--summary-interval=0",
           "--log", os.path.join(args.dir, "bt_dl.log")]
    if args.trackers:
        trackers = read_lines(args.trackers)
        if trackers:
            cmd += ["--bt-tracker=" + ",".join(trackers)]
    print("启动 aria2c：" + " ".join(cmd[:8]) + " ...", flush=True)
    r = subprocess.run(cmd)
    print(f"aria2c 退出码 {r.returncode}", flush=True)
    sys.exit(r.returncode)

if __name__ == "__main__":
    main()
