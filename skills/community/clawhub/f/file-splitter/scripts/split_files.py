#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用文件拆分脚本 - 支持 JSON / MD / TXT
用法:
  python split_files.py --input <输入文件夹> --output <输出文件夹> [选项]

选项:
  --max-size      每块最大字节数 (默认 500KB)
  --min-size      每块最小字节数 (默认 400KB)
  --seq-digits    序号位数 (默认 9)
  --formats       要处理的扩展名，逗号分隔 (默认 json,md,txt)
  --name-pattern  命名模式: {name}{seq}{ext} (默认)
  --dry-run       只预览，不实际拆分
"""

import os
import sys
import json
import argparse
import re

# ============================================================
# 常量
# ============================================================
KB = 1024
DEFAULT_MAX_SIZE = 500 * KB
DEFAULT_MIN_SIZE = 400 * KB
DEFAULT_SEQ_DIGITS = 9
SUPPORTED_FORMATS = {".json", ".md", ".txt"}


# ============================================================
# 工具函数
# ============================================================
def fmt_size(n):
    """格式化字节数为可读字符串"""
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.1f}MB"
    return f"{n / KB:.1f}KB"


def find_files(folder, formats):
    """查找文件夹中指定格式的文件（不递归）"""
    result = []
    for f in sorted(os.listdir(folder)):
        full = os.path.join(folder, f)
        if os.path.isfile(full) and os.path.splitext(f)[1].lower() in formats:
            result.append(full)
    return result


def is_already_split(filename, seq_digits):
    """判断文件名是否已经是拆分后的产物（末尾有 N 位数字序号）"""
    name, ext = os.path.splitext(filename)
    if len(name) >= seq_digits and name[-seq_digits:].isdigit():
        return True
    return False


# ============================================================
# JSON 拆分
# ============================================================
def split_json(filepath, output_folder, max_size, min_size, seq_digits, name_pattern, dry_run):
    """按 JSON 数组元素边界拆分"""
    base = os.path.splitext(os.path.basename(filepath))[0]
    ext = os.path.splitext(filepath)[1]

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        # 如果是对象，尝试找其中的列表值
        if isinstance(data, dict):
            lists = {k: v for k, v in data.items() if isinstance(v, list)}
            if not lists:
                print(f"  [SKIP] 不是 JSON 数组，也没有列表值")
                return 0, 0
            # 取最长的列表
            key = max(lists, key=lambda k: len(lists[k]))
            data = lists[key]
            print(f"  [INFO] 使用对象中的 '{key}' 数组 ({len(data)} 条)")
        else:
            print(f"  [SKIP] 不是 JSON 数组")
            return 0, 0

    total = len(data)
    if total == 0:
        print(f"  [SKIP] 空数组")
        return 0, 0

    # 估算平均记录大小
    sample_n = min(100, total)
    sample_bytes = len(json.dumps(data[:sample_n], ensure_ascii=False).encode("utf-8"))
    avg = sample_bytes / sample_n

    chunks = []
    current = []
    current_size = 0

    for rec in data:
        rec_bytes = len(json.dumps(rec, ensure_ascii=False).encode("utf-8"))
        if current and (current_size + rec_bytes) > max_size and current_size >= min_size:
            chunks.append(current)
            current = []
            current_size = 0
        current.append(rec)
        current_size += rec_bytes

    if current:
        chunks.append(current)

    written = 0
    for idx, chunk in enumerate(chunks):
        seq = str(idx + 1).zfill(seq_digits)
        out_name = f"{base}{seq}{ext}"
        out_path = os.path.join(output_folder, out_name)

        if dry_run:
            print(f"  [DRY] {out_name} ({len(chunk)} 条)")
        else:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(chunk, f, ensure_ascii=False, indent=2)
            actual = os.path.getsize(out_path)
            print(f"  [OK] {out_name} ({fmt_size(actual)}, {len(chunk)} 条)")
        written += len(chunk)

    print(f"  [验证] 原始 {total} 条 -> 拆分后 {written} 条 {'[PASS]' if total == written else '[FAIL 数据丢失]'}")
    return len(chunks), written


# ============================================================
# MD / TXT 拆分（按段落/行边界）
# ============================================================
def split_text_file(filepath, output_folder, max_size, min_size, seq_digits, name_pattern, dry_run, is_md=True):
    """
    按段落边界拆分 MD/TXT 文件。
    MD: 优先在标题（# 开头）或空行处切分
    TXT: 在空行处切分，无空行则按行切分
    """
    base = os.path.splitext(os.path.basename(filepath))[0]
    ext = os.path.splitext(filepath)[1]

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    total_bytes = len(content.encode("utf-8"))
    if total_bytes <= max_size:
        print(f"  [SKIP] 文件 {fmt_size(total_bytes)} <= 上限 {fmt_size(max_size)}")
        return 0, 0

    # 拆分单元：MD 按标题块，TXT 按段落/行
    if is_md:
        blocks = _split_md_blocks(content)
    else:
        blocks = _split_txt_blocks(content)

    chunks = []
    current = []
    current_size = 0

    for block in blocks:
        block_bytes = len(block.encode("utf-8"))
        # 如果单个块就超过 max_size，强制单独成块
        if block_bytes > max_size:
            if current:
                chunks.append("".join(current))
                current = []
                current_size = 0
            chunks.append(block)
            continue

        if current and (current_size + block_bytes) > max_size and current_size >= min_size:
            chunks.append("".join(current))
            current = []
            current_size = 0
        current.append(block)
        current_size += block_bytes

    if current:
        chunks.append("".join(current))

    written_bytes = 0
    for idx, chunk in enumerate(chunks):
        seq = str(idx + 1).zfill(seq_digits)
        out_name = f"{base}{seq}{ext}"
        out_path = os.path.join(output_folder, out_name)

        chunk_bytes = len(chunk.encode("utf-8"))
        if dry_run:
            print(f"  [DRY] {out_name} ({fmt_size(chunk_bytes)})")
        else:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(chunk)
            actual = os.path.getsize(out_path)
            print(f"  [OK] {out_name} ({fmt_size(actual)})")
        written_bytes += chunk_bytes

    print(f"  [验证] 原始 {fmt_size(total_bytes)} -> 拆分后 {fmt_size(written_bytes)} {'[PASS]' if total_bytes == written_bytes else '[FAIL]'}")
    return len(chunks), written_bytes


def _split_md_blocks(content):
    """
    将 MD 内容按标题块拆分。
    每个块以 # 开头或前一个块结束到下一个 # 之前。
    """
    lines = content.split("\n")
    blocks = []
    current = []

    for line in lines:
        if re.match(r"^#{1,6}\s", line) and current:
            # 遇到新标题，保存之前的块
            blocks.append("\n".join(current) + "\n")
            current = [line]
        else:
            current.append(line)

    if current:
        blocks.append("\n".join(current) + "\n")

    return blocks


def _split_txt_blocks(content):
    """
    将 TXT 内容按段落（空行分隔）拆分。
    如果没有空行，则按行拆分。
    """
    if "\n\n" in content:
        # 有段落分隔
        raw = content.split("\n\n")
        blocks = [b + "\n\n" for b in raw if b.strip()]
    else:
        # 按行拆分
        lines = content.split("\n")
        blocks = [l + "\n" for l in lines]

    return blocks


# ============================================================
# 主流程
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="通用文件拆分工具 (JSON / MD / TXT)")
    parser.add_argument("--input", required=True, help="输入文件夹路径")
    parser.add_argument("--output", required=True, help="输出文件夹路径")
    parser.add_argument("--max-size", type=int, default=DEFAULT_MAX_SIZE, help=f"每块最大字节数 (默认 {DEFAULT_MAX_SIZE})")
    parser.add_argument("--min-size", type=int, default=DEFAULT_MIN_SIZE, help=f"每块最小字节数 (默认 {DEFAULT_MIN_SIZE})")
    parser.add_argument("--seq-digits", type=int, default=DEFAULT_SEQ_DIGITS, help=f"序号位数 (默认 {DEFAULT_SEQ_DIGITS})")
    parser.add_argument("--formats", default="json,md,txt", help="要处理的格式，逗号分隔 (默认 json,md,txt)")
    parser.add_argument("--dry-run", action="store_true", help="只预览不执行")
    args = parser.parse_args()

    # 解析格式
    formats = {"." + f.strip().lower() for f in args.formats.split(",")}
    formats &= SUPPORTED_FORMATS
    if not formats:
        print("[ERROR] 没有有效的文件格式")
        sys.exit(1)

    # 验证输入文件夹
    input_folder = args.input
    if not os.path.isdir(input_folder):
        print(f"[ERROR] 输入文件夹不存在: {input_folder}")
        sys.exit(1)

    # 创建输出文件夹
    output_folder = args.output
    os.makedirs(output_folder, exist_ok=True)

    print("=" * 60)
    print("通用文件拆分工具")
    print("=" * 60)
    print(f"输入: {input_folder}")
    print(f"输出: {output_folder}")
    print(f"格式: {', '.join(formats)}")
    print(f"大小: {fmt_size(args.min_size)} - {fmt_size(args.max_size)}")
    print(f"序号: {args.seq_digits} 位")
    print(f"模式: {'预览 (dry-run)' if args.dry_run else '执行'}")
    print()

    # 查找文件
    all_files = find_files(input_folder, formats)
    if not all_files:
        print("[INFO] 没有找到需要处理的文件")
        return

    # 筛选需要拆分的文件（> max_size 且不是已拆分产物）
    to_split = []
    to_skip = []
    for fp in all_files:
        sz = os.path.getsize(fp)
        fn = os.path.basename(fp)
        if is_already_split(fn, args.seq_digits):
            to_skip.append((fp, sz, "已是拆分产物"))
        elif sz > args.max_size:
            to_split.append((fp, sz))
        else:
            to_skip.append((fp, sz, f"<= {fmt_size(args.max_size)}"))

    print(f"找到 {len(all_files)} 个文件")
    print(f"  需要拆分: {len(to_split)} 个")
    print(f"  跳过: {len(to_skip)} 个")

    if to_skip:
        for fp, sz, reason in to_skip:
            print(f"    [SKIP] {os.path.basename(fp)} ({fmt_size(sz)}) - {reason}")
    print()

    if not to_split:
        print("[INFO] 没有需要拆分的文件")
        return

    # 顺序处理
    total_chunks = 0
    total_original = 0
    total_written = 0

    for idx, (fp, sz) in enumerate(to_split, 1):
        fn = os.path.basename(fp)
        ext = os.path.splitext(fp)[1].lower()
        print(f"[{idx}/{len(to_split)}] {fn} ({fmt_size(sz)})")

        if ext == ".json":
            chunks, written = split_json(
                fp, output_folder, args.max_size, args.min_size,
                args.seq_digits, None, args.dry_run
            )
        elif ext == ".md":
            chunks, written = split_text_file(
                fp, output_folder, args.max_size, args.min_size,
                args.seq_digits, None, args.dry_run, is_md=True
            )
        elif ext == ".txt":
            chunks, written = split_text_file(
                fp, output_folder, args.max_size, args.min_size,
                args.seq_digits, None, args.dry_run, is_md=False
            )
        else:
            print(f"  [SKIP] 不支持的格式 {ext}")
            continue

        total_chunks += chunks
        total_original += sz
        total_written += written

    # 汇总
    print()
    print("=" * 60)
    print("拆分完成")
    print("=" * 60)
    print(f"处理文件: {len(to_split)} 个")
    print(f"生成块文件: {total_chunks} 个")
    print(f"原始总大小: {fmt_size(total_original)}")
    print(f"拆分后总大小: {fmt_size(total_written)}")
    if total_original == total_written:
        print("数据完整性: [PASS] 无丢失")
    else:
        print(f"数据完整性: [WARN] 差异 {fmt_size(abs(total_original - total_written))}")


if __name__ == "__main__":
    main()
