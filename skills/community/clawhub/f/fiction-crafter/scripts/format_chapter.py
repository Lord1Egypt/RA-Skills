#!/usr/bin/env python3
"""
章节文件分隔符处理脚本
只保留首尾两个"---"分隔符，中间所有分隔符去掉
"""

import os
import sys
import re


def process_chapter_file(file_path, output_path=None):
    """
    处理章节文件，只保留首尾两个"---"分隔符

    Args:
        file_path: 输入文件路径
        output_path: 输出文件路径，默认为原文件（覆盖）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 按行分割
    lines = content.split('\n')

    # 找到所有"---"分隔符的行索引
    separator_indices = []
    for i, line in enumerate(lines):
        # 去除空白后判断是否是分隔符
        stripped = line.strip()
        if stripped == '---':
            separator_indices.append(i)

    # 如果分隔符数量小于2，无需处理
    if len(separator_indices) < 2:
        print(f"文件 {file_path} 分隔符数量不足2个，无需处理")
        return

    # 保留第一个和最后一个分隔符
    first_sep = separator_indices[0]
    last_sep = separator_indices[-1]

    # 删除中间的分隔符
    indices_to_remove = separator_indices[1:-1]

    # 构建新的行列表
    new_lines = []
    for i, line in enumerate(lines):
        if i in indices_to_remove:
            # 跳过中间的分隔符
            continue
        new_lines.append(line)

    # 合成新内容
    new_content = '\n'.join(new_lines)

    # 输出路径
    if output_path is None:
        output_path = file_path

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"处理完成: {file_path}")
    print(f"  - 原分隔符数量: {len(separator_indices)}")
    print(f"  - 删除分隔符数量: {len(indices_to_remove)}")
    print(f"  - 保留分隔符位置: 第{first_sep+1}行、第{last_sep+1}行")


def process_directory(directory):
    """
    处理目录下所有章节文件

    Args:
        directory: 目录路径
    """
    # 查找所有章节文件
    pattern = re.compile(r'^第\d+章.*\.md$')

    files_processed = 0
    for filename in os.listdir(directory):
        if pattern.match(filename):
            file_path = os.path.join(directory, filename)
            process_chapter_file(file_path)
            files_processed += 1

    print(f"\n共处理 {files_processed} 个章节文件")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python format_chapter.py <文件路径>           # 处理单个文件")
        print("  python format_chapter.py <目录路径>           # 处理目录下所有章节文件")
        print("  python format_chapter.py <文件路径> <输出路径> # 处理单个文件并输出到指定路径")
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        process_chapter_file(input_path, output_path)
    elif os.path.isdir(input_path):
        process_directory(input_path)
    elif os.path.isfile(input_path):
        process_chapter_file(input_path)
    else:
        print(f"路径不存在: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()