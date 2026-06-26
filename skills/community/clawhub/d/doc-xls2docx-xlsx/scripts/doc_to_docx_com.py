#!/usr/bin/env python3
"""
doc_to_docx_com.py - 使用 Word COM 将 .doc 文件转换为 .docx 格式
仅限 Windows，需要安装 Microsoft Word
"""

import os
import sys
import glob
from pathlib import Path
import win32com.client
import pythoncom
import argparse


def convert_doc_to_docx(doc_path, output_path=None):
    """
    使用 Word COM 将 .doc 转换为 .docx
    """
    # 初始化 COM
    pythoncom.CoInitialize()

    word = None
    doc = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False  # 不显示弹窗

        # 打开 .doc 文件
        abs_path = os.path.abspath(doc_path)
        doc = word.Documents.Open(abs_path, ReadOnly=True)

        if output_path is None:
            output_path = os.path.abspath(doc_path + 'x')  # .docx

        # 保存为 .docx 格式 (16 = wdFormatXMLDocument)
        doc.SaveAs(output_path, FileFormat=16)
        doc.Close(SaveChanges=False)

        print(f'[OK] {os.path.basename(doc_path)} -> {os.path.basename(output_path)}')
        return True

    except Exception as e:
        print(f'[FAIL] {os.path.basename(doc_path)} - {e}')
        return False

    finally:
        if doc:
            try:
                doc.Close(SaveChanges=False)
            except:
                pass
        if word:
            try:
                word.Quit()
            except:
                pass
        pythoncom.CoUninitialize()


def batch_convert(input_dir, output_dir=None):
    """
    批量转换目录下的 .doc 文件
    """
    input_path = Path(input_dir)
    if output_dir is None:
        output_dir = input_path  # 保存到原目录
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # 查找所有 .doc 文件（不包括 .docx）
    doc_files = []
    for f in input_path.rglob('*.doc'):
        if not f.suffix.lower() == '.docx':  # 排除已经是 .docx 的
            doc_files.append(f)

    if not doc_files:
        print(f'在 {input_path} 中未找到 .doc 文件')
        return

    print(f'找到 {len(doc_files)} 个 .doc 文件\n')

    success = 0
    failed = []

    for doc_file in doc_files:
        rel_path = doc_file.relative_to(input_path)
        output_file = output_dir / rel_path.with_suffix('.docx')

        # 确保输出目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if convert_doc_to_docx(str(doc_file), str(output_file)):
            success += 1
        else:
            failed.append(str(doc_file))

    print(f'\n{"="*50}')
    print(f'完成: 成功 {success}/{len(doc_files)}')
    if failed:
        print(f'失败 {len(failed)} 个')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='使用 Word 将 .doc 转换为 .docx')
    parser.add_argument('input', help='输入 .doc 文件或目录')
    parser.add_argument('output', nargs='?', help='输出目录（默认原目录）')

    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_dir():
        batch_convert(args.input, args.output)
    else:
        if not input_path.exists():
            print(f'文件不存在: {input_path}')
            sys.exit(1)
        convert_doc_to_docx(str(input_path), args.output)