#!/usr/bin/env python3
"""PDF Reader CLI - 命令行入口"""
import sys
import os
import subprocess

# 检测并使用 venv（如果存在）
skill_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(skill_dir, '.venv', 'bin', 'python3')

if os.path.exists(venv_python) and venv_python != sys.executable:
    # 用 venv 的 python 重新执行
    os.execv(venv_python, [venv_python, __file__] + sys.argv[1:])

# 添加 skill 目录到路径
pdf_reader_dir = os.path.join(skill_dir, 'pdf_reader')
sys.path.insert(0, pdf_reader_dir)

from pdf_reader import handle_message


def main():
    if len(sys.argv) < 2:
        print("用法: pdf_reader_cli.py <指令>")
        print("示例: pdf_reader_cli.py '帮助'")
        sys.exit(1)
    
    command = " ".join(sys.argv[1:])
    result = handle_message(command)
    print(result)


if __name__ == "__main__":
    main()
