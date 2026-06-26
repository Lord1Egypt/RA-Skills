#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并章节脚本 - 确保章节间有空行分隔
版本：v1.1 (2026-04-14)
修复：章节文件末尾无换行时，合并时自动补充空行
"""

import os
import sys


def merge_chapters(chapter_dir, output_path):
    """合并章节文件夹下的所有 md 文件，按序号排序，确保章节间有空行分隔"""
    if not os.path.isdir(chapter_dir):
        print(f"❌ 目录不存在：{chapter_dir}")
        return False

    files = sorted(os.listdir(chapter_dir), key=lambda x: int(x.split('_')[0]))
    print(f"发现 {len(files)} 个章节文件：{files}")

    merged_parts = []

    for fname in files:
        fpath = os.path.join(chapter_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 去掉末尾多余空行（最多保留1个）
        content = content.rstrip('\n')
        # 去掉开头空行
        content = content.lstrip('\n')

        if merged_parts:
            # 上一个文件末尾没有空行 → 补充2个空行分隔
            merged_parts.append('\n\n')

        merged_parts.append(content)

    merged_text = '\n'.join(merged_parts)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged_text)

    print(f"✅ 合并完成：{output_path}")
    print(f"   总行数：{len(merged_text.splitlines())}")
    return True


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('用法: python3 merge_chapters.py <章节目录> <输出文件>')
        sys.exit(1)

    success = merge_chapters(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
