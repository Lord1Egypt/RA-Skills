#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股分析系统 - 报告目录整理脚本
将旧格式报告移动到新的二级目录结构
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime


def organize_reports(output_dir: str):
    """整理报告到二级目录"""
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"目录不存在：{output_path}")
        return
    
    print("=" * 60)
    print("A 股分析系统 - 报告目录整理")
    print("=" * 60)
    print()
    
    # 统计
    moved_count = 0
    error_count = 0
    skip_count = 0
    
    # 遍历所有文件
    for file_path in output_path.iterdir():
        if file_path.is_file():
            # 提取股票代码（文件名开头的 6 位数字）
            match = re.match(r'^(\d{6})_', file_path.name)
            if match:
                stock_code = match.group(1)
                
                # 创建股票代码目录
                stock_dir = output_path / stock_code
                stock_dir.mkdir(exist_ok=True)
                
                # 移动文件
                new_path = stock_dir / file_path.name
                try:
                    shutil.move(str(file_path), str(new_path))
                    print(f"[OK] {file_path.name} -> {stock_code}/")
                    moved_count += 1
                except Exception as e:
                    print(f"[FAIL] {file_path.name}: {e}")
                    error_count += 1
            else:
                print(f"[SKIP] {file_path.name} (无股票代码)")
                skip_count += 1
    
    print()
    print("=" * 60)
    print(f"整理完成!")
    print(f"  移动文件：{moved_count} 个")
    print(f"  跳过文件：{skip_count} 个")
    print(f"  错误：{error_count} 个")
    print("=" * 60)


if __name__ == "__main__":
    # 默认报告目录
    default_dir = os.path.expanduser("~/.openclaw/workspace/a-share-reports")
    
    print(f"报告目录：{default_dir}")
    print()
    
    # 整理报告
    organize_reports(default_dir)
    
    print()
    print("提示：可以使用以下命令查看整理结果:")
    print(f"  ls {default_dir}/")
    print(f"  ls {default_dir}/*/")
