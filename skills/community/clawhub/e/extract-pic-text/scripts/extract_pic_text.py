#!/usr/bin/env python3
"""
extract-pic-text: 从图片文件名中提取指定位置的文本

功能：遍历指定目录下的所有图片文件，根据分隔符提取文件名中的特定部分
"""

import os
import sys
import argparse
from pathlib import Path


def extract_text_from_filename(filename, delimiter='_', position=1):
    """
    从文件名中提取指定位置的文本
    
    Args:
        filename: 文件名（不含路径）
        delimiter: 分隔符，默认为 '_'
        position: 要提取的部分索引，1表示第一个分隔符后、第二个分隔符前的内容
    
    Returns:
        提取的文本，如果格式不符返回 None
    """
    # 移除文件扩展名
    name = Path(filename).stem
    
    # 按分隔符分割
    parts = name.split(delimiter)
    
    # 检查是否有足够的部分
    if len(parts) <= position:
        return None
    
    # 返回指定位置的内容
    return parts[position]


def process_directory(directory, delimiter='_', position=1, extensions=None):
    """
    处理目录中的所有图片文件
    
    Args:
        directory: 要扫描的目录路径
        delimiter: 文件名分隔符
        position: 提取位置
        extensions: 图片扩展名列表，None表示使用默认列表
    
    Returns:
        (成功提取的列表, 格式不符的文件列表)
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif']
    
    # 转换为小写以便比较
    extensions = [ext.lower() for ext in extensions]
    
    extracted_values = []
    invalid_files = []
    
    try:
        # 遍历目录
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            # 跳过子目录
            if os.path.isdir(filepath):
                continue
            
            # 检查扩展名
            file_ext = Path(filename).suffix.lower()
            if file_ext not in extensions:
                continue
            
            # 提取文本
            value = extract_text_from_filename(filename, delimiter, position)
            
            if value is not None:
                extracted_values.append(value)
            else:
                invalid_files.append(filename)
    
    except Exception as e:
        print(f"错误: 无法读取目录 '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    
    return extracted_values, invalid_files


def main():
    parser = argparse.ArgumentParser(
        description='从图片文件名中提取指定位置的文本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s /path/to/images
  %(prog)s /path/to/images -d '-' -p 0
  %(prog)s /path/to/images --extensions .jpg .png

文件名示例 (默认分隔符 '_'，位置 1):
  BIN245_515194318_0128N.jpg  ->  515194318
  abc_def_ghi.png             ->  def
        """
    )
    
    parser.add_argument('directory', help='图片所在目录路径')
    parser.add_argument('-d', '--delimiter', default='_',
                        help='文件名分隔符 (默认: _)')
    parser.add_argument('-p', '--position', type=int, default=1,
                        help='要提取的部分位置，0为第一部分，1为第二部分 (默认: 1)')
    parser.add_argument('-e', '--extensions', nargs='+',
                        default=['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'],
                        help='图片扩展名列表 (默认: .jpg .jpeg .png .gif .bmp .webp .tiff .tif)')
    parser.add_argument('-o', '--output', help='输出文件路径 (默认输出到stdout)')
    parser.add_argument('--sort', action='store_true',
                        help='对结果进行排序')
    parser.add_argument('--unique', action='store_true',
                        help='去重')
    
    args = parser.parse_args()
    
    # 验证目录
    if not os.path.isdir(args.directory):
        print(f"错误: 目录不存在 '{args.directory}'", file=sys.stderr)
        sys.exit(1)
    
    # 处理文件
    extracted, invalid = process_directory(
        args.directory,
        delimiter=args.delimiter,
        position=args.position,
        extensions=args.extensions
    )
    
    # 排序和去重
    if args.sort:
        extracted.sort()
    if args.unique:
        seen = set()
        unique_list = []
        for x in extracted:
            if x not in seen:
                seen.add(x)
                unique_list.append(x)
        extracted = unique_list
    
    # 生成输出
    lines = []
    if extracted:
        lines.append(','.join(extracted))
    
    if invalid:
        if lines:
            lines.append('')
        lines.append(f"注意：{len(invalid)}个文件格式不符：{', '.join(invalid)}")
    
    output = '\n'.join(lines)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output + '\n')
        print(f"结果已保存到: {args.output}")
    else:
        print(output)
    
    # 统计信息
    print(f"\n统计: 成功提取 {len(extracted)} 个, 格式不符 {len(invalid)} 个", file=sys.stderr)


if __name__ == '__main__':
    main()
