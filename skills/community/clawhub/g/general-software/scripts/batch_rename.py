#!/usr/bin/env python3
"""批量文件重命名工具"""
import argparse
import os
import re
import json
from pathlib import Path


def batch_rename(directory, pattern, replacement, regex=False, preview=True, recursive=False):
    """
    pattern: 旧名称模式
    replacement: 新名称模板
    regex: 是否使用正则
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"[ERROR] 目录不存在: {directory}")
        return

    glob_pattern = '**/*' if recursive else '*'
    files = [f for f in dir_path.glob(glob_pattern) if f.is_file()]
    renamed = []
    skipped = []

    for f in files:
        old_name = f.name
        if regex:
            try:
                new_name = re.sub(pattern, replacement, old_name)
            except re.error as e:
                print(f"[ERROR] 正则错误: {e}")
                continue
        else:
            new_name = old_name.replace(pattern, replacement)

        if new_name == old_name:
            skipped.append(old_name)
            continue

        new_path = f.parent / new_name
        if preview:
            print(f"  预览: {old_name} → {new_name}")
        else:
            if new_path.exists():
                print(f"[SKIP] 目标已存在: {new_name}")
                skipped.append(old_name)
                continue
            f.rename(new_path)
            print(f"  重命名: {old_name} → {new_name}")
        renamed.append({'from': old_name, 'to': new_name})

    print(f"\n总计: {len(renamed)} 个文件待处理, {len(skipped)} 个跳过")
    return renamed, skipped


def rename_with_seq(directory, prefix='', suffix='', ext=None, start=1, preview=True):
    """序号命名"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"[ERROR] 目录不存在: {directory}")
        return

    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    renamed = []
    for i, f in enumerate(files, start=start):
        old_name = f.name
        new_ext = ext or f.suffix
        new_name = f"{prefix}{i:03d}{suffix}{new_ext}"
        new_path = f.parent / new_name
        if preview:
            print(f"  预览: {old_name} → {new_name}")
        else:
            if new_path.exists() and new_path != f:
                new_name = f"{prefix}{i:03d}{suffix}_{new_ext}"
                new_path = f.parent / new_name
            f.rename(new_path)
            print(f"  重命名: {old_name} → {new_name}")
        renamed.append({'from': old_name, 'to': new_name})
    print(f"\n总计: {len(renamed)} 个文件")
    return renamed


def rename_with_date(directory, prefix='', date_format='%Y%m%d', preview=True):
    """按文件日期命名"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"[ERROR] 目录不存在: {directory}")
        return
    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    renamed = []
    for f in files:
        old_name = f.name
        mtime = f.stat().st_mtime
        from datetime import datetime
        date_str = datetime.fromtimestamp(mtime).strftime(date_format)
        new_name = f"{prefix}{date_str}_{old_name}"
        new_path = f.parent / new_name
        if preview:
            print(f"  预览: {old_name} → {new_name}")
        else:
            f.rename(new_path)
            print(f"  重命名: {old_name} → {new_name}")
        renamed.append({'from': old_name, 'to': new_name})
    return renamed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='批量重命名工具')
    sub = parser.add_subparsers(dest='cmd')
    r = sub.add_parser('replace', help='替换命名')
    r.add_argument('directory')
    r.add_argument('pattern')
    r.add_argument('replacement')
    r.add_argument('--regex', '-r', action='store_true')
    r.add_argument('--execute', '-e', action='store_true', help='执行（否则仅预览）')
    r.add_argument('--recursive', '-R', action='store_true')
    s = sub.add_parser('seq', help='序号命名')
    s.add_argument('directory')
    s.add_argument('--prefix', '-p', default='')
    s.add_argument('--suffix', '-s', default='')
    s.add_argument('--ext', default=None)
    s.add_argument('--start', type=int, default=1)
    s.add_argument('--execute', '-e', action='store_true')
    d = sub.add_parser('date', help='日期命名')
    d.add_argument('directory')
    d.add_argument('--prefix', '-p', default='')
    d.add_argument('--format', '-f', default='%Y%m%d')
    d.add_argument('--execute', '-e', action='store_true')
    args = parser.parse_args()
    if args.cmd == 'replace':
        batch_rename(args.directory, args.pattern, args.replacement, args.regex, not args.execute, args.recursive)
    elif args.cmd == 'seq':
        rename_with_seq(args.directory, args.prefix, args.suffix, args.ext, args.start, not args.execute)
    elif args.cmd == 'date':
        rename_with_date(args.directory, args.prefix, args.format, not args.execute)
