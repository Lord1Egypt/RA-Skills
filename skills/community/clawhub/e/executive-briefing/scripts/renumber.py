#!/usr/bin/env python3
"""章节编号自动重排

用法:
  python3 renumber.py <file> --after <N>    # 在第N章后插入，后续编号+1
  python3 renumber.py <file> --fix          # 修复跳号，从1连续重排
  python3 renumber.py <file> --after <N> --dry-run  # 预览不修改
"""
import re, sys, argparse
from pathlib import Path


def _part_matches(text):
    ms = list(re.finditer(r'^(## Part\s+)(\d+)', text, re.MULTILINE))
    return [(m.start(), m.group(1), int(m.group(2)), m.group(0)) for m in ms]


def _sub_matches(text):
    ms = list(re.finditer(r'^(###\s+)(\d+)\.(\d+)', text, re.MULTILINE))
    return [(m.start(), m.group(1), int(m.group(2)), int(m.group(3)), m.group(0)) for m in ms]


def shift_after(text, after_n):
    parts = _part_matches(text)
    if not parts:
        print('错误：未找到任何 Part 章节', file=sys.stderr)
        sys.exit(1)
    max_n = max(p[2] for p in parts)
    if after_n > max_n:
        print(f'错误：Part {after_n} 不存在，最大章节为 Part {max_n}', file=sys.stderr)
        sys.exit(1)
    result = list(text)
    for pos, prefix, num, full in sorted(parts, key=lambda x: -x[0]):
        if num > after_n:
            result[pos:pos + len(full)] = f'{prefix}{num + 1}'
    result_str = ''.join(result)
    subs = _sub_matches(result_str)
    result = list(result_str)
    for pos, prefix, pn, sn, full in sorted(subs, key=lambda x: -x[0]):
        if pn > after_n:
            result[pos:pos + len(full)] = f'{prefix}{pn + 1}.{sn}'
    return ''.join(result)


def fix_numbering(text):
    parts = _part_matches(text)
    if not parts:
        return text
    remap = {num: i + 1 for i, (_, _, num, _) in enumerate(sorted(parts, key=lambda x: x[0]))}
    result = list(text)
    for pos, prefix, num, full in sorted(parts, key=lambda x: -x[0]):
        new_num = remap[num]
        if new_num != num:
            result[pos:pos + len(full)] = f'{prefix}{new_num}'
    result_str = ''.join(result)
    subs = _sub_matches(result_str)
    result = list(result_str)
    for pos, prefix, pn, sn, full in sorted(subs, key=lambda x: -x[0]):
        if pn in remap and remap[pn] != pn:
            result[pos:pos + len(full)] = f'{prefix}{remap[pn]}.{sn}'
    return ''.join(result)


def main():
    p = argparse.ArgumentParser(description='章节编号自动重排')
    p.add_argument('file')
    p.add_argument('--after', type=int)
    p.add_argument('--fix', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f'错误：文件不存在 {args.file}', file=sys.stderr)
        sys.exit(1)
    text = path.read_text(encoding='utf-8')
    new_text = shift_after(text, args.after) if args.after else fix_numbering(text)
    if args.dry_run:
        print(new_text)
    else:
        path.write_text(new_text, encoding='utf-8')
        print(f'已更新：{args.file}')


if __name__ == '__main__':
    main()
