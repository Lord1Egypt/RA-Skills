#!/usr/bin/env python3
"""
批量文档转换工具
将指定目录中的所有支持文件转换为 Markdown 格式
"""

import sys
from pathlib import Path
from markitdown import MarkItDown


def convert_directory(input_dir, output_dir, recursive=True, overwrite=False):
    """
    批量转换目录中的文档

    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
        recursive: 是否递归处理子目录
        overwrite: 是否覆盖已存在的输出文件
    """
    md = MarkItDown()
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        print(f"错误: 输入目录不存在: {input_dir}")
        return False

    output_path.mkdir(parents=True, exist_ok=True)

    # 收集文件
    if recursive:
        files = list(input_path.rglob("*"))
    else:
        files = list(input_path.glob("*"))

    # 筛选支持的文件
    supported_extensions = {'.pdf', '.docx', '.pptx', '.xlsx', '.txt',
                           '.html', '.csv', '.json', '.xml', '.zip',
                           '.epub', '.png', '.jpg', '.jpeg', '.gif',
                           '.mp3', '.wav', '.m4a'}

    files_to_convert = [f for f in files if f.is_file() and f.suffix.lower() in supported_extensions]

    if not files_to_convert:
        print(f"在 '{input_dir}' 中没有找到支持的文档")
        return False

    print(f"找到 {len(files_to_convert)} 个文件待转换")

    success_count = 0
    error_count = 0

    for file_path in files_to_convert:
        try:
            # 计算输出路径
            if recursive:
                rel_path = file_path.relative_to(input_path)
                output_file = output_path / rel_path.with_suffix('.md')
            else:
                output_file = output_path / file_path.with_suffix('.md').name

            output_file.parent.mkdir(parents=True, exist_ok=True)

            # 检查是否已存在
            if output_file.exists() and not overwrite:
                print(f"跳过 (已存在): {file_path.name}")
                continue

            # 转换
            result = md.convert(str(file_path))
            output_file.write_text(result.text_content, encoding='utf-8')
            print(f"✓ {file_path.name} -> {output_file.relative_to(output_path)}")
            success_count += 1

        except Exception as e:
            print(f"✗ {file_path.name}: {str(e)[:100]}")
            error_count += 1

    print(f"\n完成: 成功 {success_count}, 失败 {error_count}")
    return True


def main():
    """命令行入口点"""
    import argparse

    parser = argparse.ArgumentParser(
        description='批量转换文档为 Markdown 格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s ./documents ./markdown
  %(prog)s ./input ./output --no-recursive
  %(prog)s ./source ./out --overwrite
        """
    )

    parser.add_argument('input_dir', help='输入目录路径')
    parser.add_argument('output_dir', help='输出目录路径')
    parser.add_argument('--no-recursive', action='store_true',
                       help='不递归处理子目录')
    parser.add_argument('--overwrite', action='store_true',
                       help='覆盖已存在的输出文件')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')

    args = parser.parse_args()

    if args.verbose:
        print(f"输入: {args.input_dir}")
        print(f"输出: {args.output_dir}")
        print(f"递归: {not args.no_recursive}")
        print(f"覆盖: {args.overwrite}")

    success = convert_directory(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        recursive=not args.no_recursive,
        overwrite=args.overwrite
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()