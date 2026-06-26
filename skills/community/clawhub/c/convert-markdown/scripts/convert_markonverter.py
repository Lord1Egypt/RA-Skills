#!/usr/bin/env python3
"""
MarkItDown 包装器 - 提供简化的命令行接口
"""

import sys
from pathlib import Path
from markitdown import MarkItDown


def simple_convert(input_path, output_path=None, overwrite=False):
    """
    简单转换函数

    Args:
        input_path: 输入文件或目录路径
        output_path: 输出文件或目录路径（默认为输入同名 .md）
        overwrite: 是否覆盖已存在的文件

    Returns:
        成功返回 True，否则 False
    """
    md = MarkItDown()
    input_p = Path(input_path)

    if not input_p.exists():
        print(f"错误：路径不存在 '{input_path}'")
        return False

    # 确定输出路径
    if output_path is None:
        if input_p.is_file():
            output_p = input_p.with_suffix('.md')
        else:
            output_p = input_p
    else:
        output_p = Path(output_path)

    # 处理文件
    if input_p.is_file():
        return _convert_file(md, input_p, output_p, overwrite)
    elif input_p.is_dir():
        return _convert_directory(md, input_p, output_p, overwrite)
    else:
        print(f"错误：'{input_path}' 不是有效的文件或目录")
        return False


def _convert_file(md, input_file, output_file, overwrite):
    """转换单个文件"""
    if output_file.exists() and not overwrite:
        print(f"跳过（已存在）: {input_file.name}")
        return True

    try:
        result = md.convert(str(input_file))
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result.text_content, encoding='utf-8')
        print(f"✓ {input_file} -> {output_file}")
        return True
    except Exception as e:
        print(f"✗ {input_file}: {e}")
        return False


def _convert_directory(md, input_dir, output_dir, overwrite):
    """转换目录"""
    files = list(input_dir.rglob("*"))
    supported = {'.pdf', '.docx', '.pptx', '.xlsx', '.txt',
                 '.html', '.csv', '.json', '.xml', '.zip'}

    success = 0
    for file_path in files:
        if file_path.is_file() and file_path.suffix.lower() in supported:
            rel = file_path.relative_to(input_dir)
            out_file = output_dir / rel.with_suffix('.md')
            if _convert_file(md, file_path, out_file, overwrite):
                success += 1

    print(f"完成：成功 {success} 个文件")
    return True


def cli():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        prog='convert-md',
        description='简易 MarkItDown 转换工具'
    )
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('-o', '--output', help='输出文件或目录')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件')
    parser.add_argument('--version', action='version', version='MarkItDown Skill Wrapper 1.0')

    args = parser.parse_args()

    success = simple_convert(
        input_path=args.input,
        output_path=args.output,
        overwrite=args.overwrite
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    cli()