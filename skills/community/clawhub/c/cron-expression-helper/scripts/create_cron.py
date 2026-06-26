#!/usr/bin/env python3
"""
交互式创建cron表达式的脚本
通过问答方式帮助用户构建cron表达式
"""

import argparse
import sys
from datetime import datetime

def get_field_input(field_name, field_range, examples, default="*"):
    """
    获取cron字段的输入
    """
    print(f"\n=== {field_name}字段 ===")
    print(f"取值范围: {field_range}")
    print(f"示例: {examples}")
    print(f"特殊字符: * (任何值), , (列表), - (范围), / (步长)")
    
    while True:
        value = input(f"请输入{field_name}的值 (默认: {default}): ").strip()
        if not value:
            value = default
        
        # 简单的验证
        if value == "*":
            return value
        
        # 检查是否包含有效字符
        valid_chars = set("0123456789*,-/")
        if all(c in valid_chars for c in value):
            return value
        else:
            print("错误: 包含无效字符。请只使用数字和特殊字符(*,-,/)")

def create_cron_interactive():
    """
    交互式创建cron表达式
    """
    print("=" * 50)
    print("Cron表达式创建助手")
    print("=" * 50)
    print("我将通过几个问题帮助你创建cron表达式。")
    print("cron表达式格式: 分钟 小时 日 月 星期")
    print()
    
    # 获取各个字段的值
    minute = get_field_input(
        "分钟", "0-59", 
        "0 (整点), */5 (每5分钟), 0,15,30,45 (每15分钟)",
        "*"
    )
    
    hour = get_field_input(
        "小时", "0-23", 
        "0 (午夜), 9 (上午9点), 9-17 (工作时间), */2 (每2小时)",
        "*"
    )
    
    day = get_field_input(
        "日", "1-31", 
        "1 (每月1号), */2 (每2天), 1,15 (每月1号和15号)",
        "*"
    )
    
    month = get_field_input(
        "月", "1-12 或 JAN-DEC", 
        "* (每月), 1-6 (1月到6月), 1,4,7,10 (季度初)",
        "*"
    )
    
    weekday = get_field_input(
        "星期", "0-6 或 SUN-SAT (0和7都表示周日)", 
        "1-5 (周一到周五), 0 (周日), 6 (周六)",
        "*"
    )
    
    # 构建cron表达式
    cron_expr = f"{minute} {hour} {day} {month} {weekday}"
    
    print("\n" + "=" * 50)
    print("生成的cron表达式:")
    print(f"  {cron_expr}")
    print()
    print("表达式解释:")
    print(f"  分钟: {minute}")
    print(f"  小时: {hour}")
    print(f"  日: {day}")
    print(f"  月: {month}")
    print(f"  星期: {weekday}")
    print("=" * 50)
    
    return cron_expr

def create_cron_from_args(args):
    """
    从命令行参数创建cron表达式
    """
    cron_expr = f"{args.minute} {args.hour} {args.day} {args.month} {args.weekday}"
    
    print(f"生成的cron表达式: {cron_expr}")
    print()
    print("表达式解释:")
    print(f"  分钟: {args.minute}")
    print(f"  小时: {args.hour}")
    print(f"  日: {args.day}")
    print(f"  月: {args.month}")
    print(f"  星期: {args.weekday}")
    
    return cron_expr

def main():
    parser = argparse.ArgumentParser(description="创建cron表达式")
    parser.add_argument("--minute", default="*", help="分钟字段 (0-59)")
    parser.add_argument("--hour", default="*", help="小时字段 (0-23)")
    parser.add_argument("--day", default="*", help="日字段 (1-31)")
    parser.add_argument("--month", default="*", help="月字段 (1-12 或 JAN-DEC)")
    parser.add_argument("--weekday", default="*", help="星期字段 (0-6 或 SUN-SAT)")
    parser.add_argument("--interactive", action="store_true", help="使用交互模式")
    
    args = parser.parse_args()
    
    if args.interactive or (len(sys.argv) == 1):
        cron_expr = create_cron_interactive()
    else:
        cron_expr = create_cron_from_args(args)
    
    # 询问是否保存到文件
    save = input("\n是否将cron表达式保存到文件? (y/N): ").strip().lower()
    if save == 'y':
        filename = input("请输入文件名 (默认: cron_expression.txt): ").strip()
        if not filename:
            filename = "cron_expression.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 生成的cron表达式\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{cron_expr}\n")
            f.write(f"\n# 解释:\n")
            f.write(f"# 分钟: {args.minute if not args.interactive else '交互式输入'}\n")
            f.write(f"# 小时: {args.hour if not args.interactive else '交互式输入'}\n")
            f.write(f"# 日: {args.day if not args.interactive else '交互式输入'}\n")
            f.write(f"# 月: {args.month if not args.interactive else '交互式输入'}\n")
            f.write(f"# 星期: {args.weekday if not args.interactive else '交互式输入'}\n")
        
        print(f"Cron表达式已保存到 {filename}")

if __name__ == "__main__":
    main()