#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
convert-markdown 技能 - OpenClaw 命令入口

支持的命令:
  convert   - 转换单个文件或目录
  batch     - 批量转换目录
"""

import argparse
import subprocess
import sys
from pathlib import Path

# 指向实际的处理脚本
CONVERTER_SCRIPT = Path(__file__).parent / "convert_markonverter.py"

def cmd_convert(args):
    """转换单个文件或目录"""
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    if not input_path.exists():
        print(f"错误：输入路径不存在 - {input_path}")
        return 1

    # 调用原始脚本
    cmd = [
        sys.executable,
        str(CONVERTER_SCRIPT),
        str(input_path)
    ]

    if output_path:
        cmd.extend(["-o", str(output_path)])

    if args.overwrite:
        cmd.append("--overwrite")

    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

def cmd_batch(args):
    """批量转换目录"""
    source = Path(args.source)
    target = Path(args.target)

    if not source.exists():
        print(f"错误：源目录不存在 - {source}")
        return 1

    # 递归处理所有支持格式
    include_formats = args.include.split(',') if args.include else None
    exclude_formats = args.exclude.split(',') if args.exclude else None

    # 收集文件
    files = list(source.rglob("*"))
    supported = set(args.formats.split(',') if args.formats else [
        '.pdf', '.docx', '.xlsx', '.pptx', '.txt',
        '.html', '.csv', '.json', '.xml', '.zip'
    ])

    success = 0
    for file_path in files:
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext not in supported:
                continue
            if include_formats and ext not in include_formats:
                continue
            if exclude_formats and ext in exclude_formats:
                continue

            # 计算输出路径
            rel = file_path.relative_to(source)
            out_file = target / rel.with_suffix('.md')
            out_file.parent.mkdir(parents=True, exist_ok=True)

            # 调用转换
            cmd = [
                sys.executable,
                str(CONVERTER_SCRIPT),
                str(file_path),
                "-o",
                str(out_file)
            ]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                success += 1
                print(f"✓ {file_path.name}")
            else:
                print(f"✗ {file_path.name}: {result.stderr.decode().strip()}")

    print(f"\n批量转换完成: {success} 个文件成功")
    return 0 if success > 0 else 1

def main():
    parser = argparse.ArgumentParser(
        prog='convert-markdown',
        description='OpenClaw convert-markdown 技能接口'
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # convert 子命令
    parser_convert = subparsers.add_parser('convert', help='转换文件或目录')
    parser_convert.add_argument('--input', '-i', required=True, help='输入文件或目录')
    parser_convert.add_argument('--output', '-o', help='输出文件或目录')
    parser_convert.add_argument('--overwrite', action='store_true', help='覆盖已存在文件')

    # batch 子命令
    parser_batch = subparsers.add_parser('batch', help='批量转换目录')
    parser_batch.add_argument('--source', '-s', required=True, help='源目录')
    parser_batch.add_argument('--target', '-t', required=True, help='目标目录')
    parser_batch.add_argument('--include', help='包含的格式（逗号分隔）')
    parser_batch.add_argument('--exclude', help='排除的格式（逗号分隔）')
    parser_batch.add_argument('--formats', help='支持格式列表（默认全部）')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'convert':
        return cmd_convert(args)
    elif args.command == 'batch':
        return cmd_batch(args)
    else:
        print(f"未知命令: {args.command}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
