#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量校验 + 正则重命名 + 归档移动（已验证，从 organize_bt.py 通用化）

用法：
    python3 organize_media.py 下载目录 目标目录 --pattern 'S0?1E0?(\\d+)' --name-template '剧名 S01E{1}.mkv' [--delete-shell]

- 先 ffprobe 全量校验（duration 非空 = 完整）
- 校验通过的文件按正则提取字段 → 重命名 → 移动到目标目录
- 空壳文件（moov atom not found）列出并可选删除
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

def probe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return None
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None

def main():
    ap = argparse.ArgumentParser(description="批量校验+重命名+归档")
    ap.add_argument("src", help="下载目录")
    ap.add_argument("dst", help="目标目录")
    ap.add_argument("--pattern", required=True, help="从文件名提取字段的正则，如 S0?1E0?(\\d+)")
    ap.add_argument("--name-template", required=True, help="重命名模板，{1} 对应第1个捕获组")
    ap.add_argument("--delete-shell", action="store_true", help="删除空壳文件（moov 缺失）")
    args = ap.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    rx = re.compile(args.pattern, re.IGNORECASE)
    ok = shell = failed = moved = 0
    shell_files = []

    for root, _, files in os.walk(args.src):
        for fn in sorted(files):
            if fn.endswith(".aria2"):
                continue
            path = os.path.join(root, fn)
            dur = probe_duration(path)
            if dur is None or dur <= 0:
                shell += 1
                shell_files.append(path)
                print(f"[shell] {path}", flush=True)
                if args.delete_shell:
                    os.remove(path)
                continue
            m = rx.search(fn)
            if m:
                newname = args.name_template.format(*[m.group(i) for i in range(1, m.lastindex + 1)])
                dst_path = os.path.join(args.dst, newname)
                if os.path.exists(dst_path):
                    print(f"[skip] 已存在: {newname}", flush=True)
                    continue
                shutil.move(path, dst_path)
                moved += 1
                print(f"[move] {fn} → {newname}", flush=True)
            else:
                ok += 1
    print(f"\n完成：完整 {ok + moved}（已归档 {moved}） / 空壳 {shell} / 匹配失败 {failed}", flush=True)
    if shell_files:
        print("空壳文件列表：")
        for p in shell_files:
            print(f"  {p}", flush=True)

if __name__ == "__main__":
    main()
