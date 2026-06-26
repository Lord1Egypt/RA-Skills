#!/usr/bin/env python3
"""
百分比计算器
支持多种百分比计算场景
"""

import argparse
import sys
import json
import re
from typing import Optional, Dict, Any

def percent_of(part: float, whole: float) -> float:
    """
    计算部分占整体的百分比
    """
    if whole == 0:
        raise ValueError("除数不能为零")
    return (part / whole) * 100

def value_of_percent(whole: float, percent: float) -> float:
    """
    计算整体的某个百分比的值
    """
    return whole * (percent / 100)

def growth_rate(old_value: float, new_value: float) -> float:
    """
    计算增长率
    """
    if old_value == 0:
        raise ValueError("原始值不能为零")
    return ((new_value - old_value) / old_value) * 100

def discount_price(original: float, discount: float) -> float:
    """
    计算折扣后价格
    discount: 折扣率 (如8折输入80或8)
    """
    # 处理输入可能是 8 或 80 的情况
    if discount > 1:
        discount = discount / 10
    elif discount > 0.1:
        discount = discount / 100
    
    return original * discount

def vat_calculation(price: float, rate: float = 13, include_vat: bool = False) -> Dict[str, float]:
    """
    计算增值税
    rate: 税率，默认13%
    include_vat: 价格是否已含税
    """
    if include_vat:
        # 价格含税，计算不含税价格和税额
        base = price / (1 + rate / 100)
        vat = price - base
        return {"base": base, "vat": vat, "total": price}
    else:
        # 价格不含税，计算含税价格
        vat = price * (rate / 100)
        total = price + vat
        return {"base": price, "vat": vat, "total": total}

def parse_natural_input(text: str) -> Optional[Dict[str, Any]]:
    """
    解析自然语言输入
    """
    text = text.strip()
    
    # "X是Y的百分之几" 或 "X占Y的%"
    match = re.search(r'([\d\.]+)\s*[是占]\s*([\d\.]+)\s*的?百分之?几', text)
    if match:
        return {"type": "percent", "part": float(match.group(1)), "whole": float(match.group(2))}
    
    # "Y的X%是多少" 或 "Y的百分之X"
    match = re.search(r'([\d\.]+)\s*的?\s*([\d\.]+)\s*%?\s*[是等于]?\s*多少', text)
    if match:
        return {"type": "value", "whole": float(match.group(1)), "percent": float(match.group(2))}
    
    # "从A涨到B" 或 "从A到B增长"
    match = re.search(r'从\s*([\d\.]+)\s*[涨增]?到\s*([\d\.]+)', text)
    if match:
        return {"type": "growth", "old": float(match.group(1)), "new": float(match.group(2))}
    
    # "原价X打Y折"
    match = re.search(r'原价\s*([\d\.]+)\s*打\s*([\d\.]+)\s*折', text)
    if match:
        return {"type": "discount", "original": float(match.group(1)), "discount": float(match.group(2))}
    
    return None

def main():
    parser = argparse.ArgumentParser(description="百分比计算器")
    parser.add_argument("input", nargs="?", help="自然语言输入或数值")
    parser.add_argument("-t", "--type", choices=["percent", "value", "growth", "discount", "vat"],
                        help="计算类型")
    parser.add_argument("-v1", "--value1", type=float, help="第一个数值")
    parser.add_argument("-v2", "--value2", type=float, help="第二个数值")
    parser.add_argument("-j", "--json", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    result = None
    
    # 尝试解析自然语言
    if args.input and not args.type:
        parsed = parse_natural_input(args.input)
        if parsed:
            if parsed["type"] == "percent":
                result = {"type": "百分比", "value": percent_of(parsed["part"], parsed["whole"])}
            elif parsed["type"] == "value":
                result = {"type": "占比值", "value": value_of_percent(parsed["whole"], parsed["percent"])}
            elif parsed["type"] == "growth":
                result = {"type": "增长率", "value": growth_rate(parsed["old"], parsed["new"])}
            elif parsed["type"] == "discount":
                result = {"type": "折扣价", "value": discount_price(parsed["original"], parsed["discount"])}
    
    # 使用参数模式
    elif args.type and args.value1 is not None and args.value2 is not None:
        if args.type == "percent":
            result = {"type": "百分比", "value": percent_of(args.value1, args.value2)}
        elif args.type == "value":
            result = {"type": "占比值", "value": value_of_percent(args.value1, args.value2)}
        elif args.type == "growth":
            result = {"type": "增长率", "value": growth_rate(args.value1, args.value2)}
        elif args.type == "discount":
            result = {"type": "折扣价", "value": discount_price(args.value1, args.value2)}
        elif args.type == "vat":
            vat_result = vat_calculation(args.value1, args.value2)
            result = {"type": "增值税", "base": vat_result["base"], "vat": vat_result["vat"], "total": vat_result["total"]}
    
    if result is None:
        print("错误：请提供有效的输入或参数", file=sys.stderr)
        sys.exit(1)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "value" in result:
            print(f"{result['type']}: {result['value']:.2f}%".replace("%", "%%").replace("%%%", "%"))
        elif "base" in result:
            print(f"不含税价: {result['base']:.2f}")
            print(f"税额: {result['vat']:.2f}")
            print(f"含税价: {result['total']:.2f}")

if __name__ == "__main__":
    main()
