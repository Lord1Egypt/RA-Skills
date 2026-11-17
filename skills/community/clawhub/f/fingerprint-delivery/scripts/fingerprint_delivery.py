#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fingerprint_delivery.py - 指纹锁定交付工具

给交付物 HTML 一键加「内容快照指纹 + 最终文件校验指纹 + 时间戳」，产出 .sha256 校验文件。

用法:
    python fingerprint_delivery.py --html <path> [选项]

选项:
    --placeholder <字符串>   指纹占位符（默认 __FINGERPRINT__）
    --sha-suffix <后缀>      校验文件后缀（默认 .sha256）
    --no-inject              不注入，仅计算并输出两个指纹
    --stamp "<文本>"         注入时间戳文本（默认注入本地 ISO 时间戳）

输出:
    SNAPSHOT_FP = 内容快照指纹（含占位符的正文哈希，不含指纹字段自身）
    FINAL_FP    = 最终文件整体指纹（含指纹字段，写入 .sha256 校验文件）

示例:
    python fingerprint_delivery.py --html report.html
    sha256sum -c report.html.sha256   # 输出 OK = 未被篡改
"""

import argparse
import hashlib
import io
import sys
from datetime import datetime, timezone, timedelta


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="指纹锁定交付工具")
    parser.add_argument("--html", required=True, help="交付物 HTML 文件路径")
    parser.add_argument("--placeholder", default="__FINGERPRINT__", help="指纹占位符")
    parser.add_argument("--sha-suffix", default=".sha256", help="校验文件后缀")
    parser.add_argument("--no-inject", action="store_true", help="不注入，仅计算输出")
    parser.add_argument("--stamp", default=None, help="注入的时间戳文本（默认本地 ISO 时间）")
    args = parser.parse_args()

    path = args.html
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        print(f"ERROR: cannot read file: {e}")
        return 1

    # 1) 内容快照指纹：对"含占位符的正文"哈希（不含指纹字段自身）
    snap = sha256_hex(content)

    if args.no_inject:
        print("SNAPSHOT_FP =", snap)
        return 0

    if args.placeholder not in content:
        print(f"ERROR: placeholder '{args.placeholder}' not found in file")
        return 1

    # 2) 注入时间戳（可选）与指纹
    final = content
    if "__TIMESTAMP__" in final:
        ts = args.stamp if args.stamp is not None else datetime.now(
            timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S GMT+8")
        final = final.replace("__TIMESTAMP__", ts)
    final = final.replace(args.placeholder, snap)

    # 3) 写回最终文件
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(final)

    # 4) 最终文件指纹 + 校验文件
    final_hash = sha256_hex(final)
    sha_path = path + args.sha_suffix
    with io.open(sha_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{final_hash}  {path.split(chr(92))[-1]}\n")

    print("SNAPSHOT_FP =", snap)
    print("FINAL_FP    =", final_hash)
    print("SHA_FILE    =", sha_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
