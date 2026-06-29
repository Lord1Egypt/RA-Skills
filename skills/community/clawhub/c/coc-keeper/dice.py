#!/usr/bin/env python3
"""
COC骰子脚本
用法: python dice.py [NdS...]
示例:
  python dice.py 1d20        # 1个20面骰
  python dice.py 2d6         # 2个6面骰
  python dice.py 1d20 2d6    # 1个20面骰和2个6面骰
  python dice.py 100         # 1个100面骰（兼容旧格式）
"""

import sys
import secrets
import re

def parse_dice_expression(expr):
    """
    解析骰子表达式
    格式: NdS (N个S面骰子)
    返回: (数量, 面数) 或 None（如果格式错误）
    """
    # 匹配 NdS 格式
    match = re.match(r'^(\d+)[dD](\d+)$', expr)
    if match:
        count = int(match.group(1))
        sides = int(match.group(2))
        if count <= 0 or sides <= 0:
            return None
        return (count, sides)

    # 兼容旧格式：纯数字表示1个N面骰
    try:
        sides = int(expr)
        if sides <= 0:
            return None
        return (1, sides)
    except ValueError:
        return None

def roll_dice(count, sides):
    """
    投掷N个S面骰子
    返回: 结果列表
    """
    return [secrets.randbelow(sides) + 1 for _ in range(count)]

def main():
    # 如果没有参数，默认1个100面骰
    if len(sys.argv) < 2:
        results = roll_dice(1, 100)
        print(results[0])
        return

    # 解析并投掷每个骰子表达式
    all_results = []
    for expr in sys.argv[1:]:
        parsed = parse_dice_expression(expr)
        if parsed is None:
            print(f"错误：无法解析骰子表达式 '{expr}'")
            print("格式应为 NdS（如 1d20, 2d6）或纯数字（如 100）")
            sys.exit(1)

        count, sides = parsed
        results = roll_dice(count, sides)
        all_results.append((expr, results))

    # 输出结果
    for expr, results in all_results:
        if len(results) == 1:
            print(f"{expr}: {results[0]}")
        else:
            total = sum(results)
            print(f"{expr}: {results} = {total}")

if __name__ == "__main__":
    main()
