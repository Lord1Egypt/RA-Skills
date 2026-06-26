#!/usr/bin/env python3
"""
饮食记录工具 - 生成固定格式的饮食记录文件

用法:
    python3 log_diet.py --date 2026-03-27 --meal 晚饭 --items "红烧肉,米饭"
    python3 log_diet.py --meal 早饭 --items "鸡蛋,牛奶"

参数:
    --date: 日期 (默认今天，格式 YYYY-MM-DD)
    --meal: 餐段 (早饭/中饭/晚饭/加餐)
    --items: 食物列表，逗号分隔
"""

import argparse
import os
from datetime import datetime

# 配置
VAULT_PATH = "/mnt/c/Users/loong/iCloudDrive/iCloud~md~obsidian/HomeMo.Art"
DAILY_DIR = os.path.join(VAULT_PATH, "05-Daily")


def get_template(date_str: str) -> str:
    """获取文件模板"""
    return f"""# {date_str} 饮食记录

## 早饭

## 中饭

## 晚饭

## 加餐

---
*记录时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""


def parse_items(items_str: str) -> list:
    """解析食物列表"""
    return [item.strip() for item in items_str.split(",") if item.strip()]


def format_items(items: list) -> str:
    """格式化食物列表为 markdown"""
    return "\n".join([f"- {item}" for item in items])


def read_or_create_file(filepath: str, date_str: str) -> str:
    """读取文件，如果不存在则创建"""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return get_template(date_str)


def update_meal(content: str, meal: str, items: list) -> str:
    """在对应餐段追加食物"""
    items_md = format_items(items)
    meal_header = f"## {meal}"
    
    lines = content.split("\n")
    result = []
    meal_found = False
    meal_line_idx = -1
    
    # 找到餐段位置
    for i, line in enumerate(lines):
        if line.strip() == meal_header:
            meal_found = True
            meal_line_idx = i
            result.append(line)
            # 在餐段标题后添加食物
            result.append(items_md)
        else:
            result.append(line)
    
    # 如果没找到餐段，追加到最后
    if not meal_found:
        result.append(f"\n## {meal}")
        result.append(items_md)
    
    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(description="记录饮食")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                        help="日期 (YYYY-MM-DD)")
    parser.add_argument("--meal", required=True,
                        choices=["早饭", "中饭", "晚饭", "加餐"],
                        help="餐段")
    parser.add_argument("--items", required=True,
                        help="食物列表，逗号分隔")
    
    args = parser.parse_args()
    
    # 确保目录存在
    os.makedirs(DAILY_DIR, exist_ok=True)
    
    # 文件路径
    filename = f"饮食记录-{args.date}.md"
    filepath = os.path.join(DAILY_DIR, filename)
    
    # 读取或创建文件
    content = read_or_create_file(filepath, args.date)
    
    # 解析食物
    items = parse_items(args.items)
    
    # 更新内容
    new_content = update_meal(content, args.meal, items)
    
    # 保存文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ 已记录: {args.meal} - {', '.join(items)}")
    print(f"📁 文件: {filepath}")


if __name__ == "__main__":
    main()
