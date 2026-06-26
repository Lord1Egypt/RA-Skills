#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化转换工具：先检查并修复MD格式，再转换为DOCX
"""

import sys
import os

# 导入格式检查函数和转换函数
try:
    from validate_and_fix_md import validate_and_fix_markdown
    from md_to_docx import convert_md_to_docx
except ImportError as e:
    print("导入错误: {}".format(e))
    print("请确保 validate_and_fix_md.py 和 md_to_docx.py 在同一目录下")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("用法: python auto_convert.py <md文件路径> [输出docx路径]")
        print("\n示例:")
        print("  python auto_convert.py input.md")
        print("  python auto_convert.py input.md output.docx")
        sys.exit(1)

    md_path = sys.argv[1]

    if len(sys.argv) >= 3:
        docx_path = sys.argv[2]
    else:
        # 自动生成docx路径
        docx_path = os.path.splitext(md_path)[0] + '.docx'

    # 检查输入文件是否存在
    if not os.path.exists(md_path):
        print("错误：MD文件不存在 - {}".format(md_path))
        sys.exit(1)

    print("=" * 60)
    print("自动化转换流程")
    print("=" * 60)
    print("输入文件: {}".format(md_path))
    print("输出文件: {}".format(docx_path))
    print()

    # 步骤1：格式检查与修复
    print("【步骤1/2】检查并修复MD格式...")
    print("-" * 60)
    try:
        validate_and_fix_markdown(md_path, fix=True)
        print("✓ 格式检查与修复完成")
    except Exception as e:
        print("警告：格式检查失败 - {}".format(e))
        print("将尝试继续转换...")

    print()
    print("-" * 60)
    
    # 步骤2：转换为DOCX
    print("【步骤2/2】转换为DOCX...")
    print("-" * 60)
    try:
        convert_md_to_docx(md_path, docx_path)
        print("✓ 转换完成")
    except Exception as e:
        print("错误：转换失败 - {}".format(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print()
    print("=" * 60)
    print("✓ 全部完成！")
    print("输出文件: {}".format(docx_path))
    print("=" * 60)


if __name__ == '__main__':
    main()
