#!/usr/bin/env python3
"""
工程量计算脚本
支持常见工程量计算公式
"""

import argparse
import json
from datetime import datetime

# 工程量计算公式库
FORMULAS = {
    "concrete": {
        "name": "混凝土",
        "unit": "m³",
        "formula": "length * width * height",
        "description": "体积 = 长 × 宽 × 高"
    },
    "steel": {
        "name": "钢筋",
        "unit": "吨",
        "formula": "length * weight_per_meter / 1000",
        "description": "重量 = 长度 × 每米重量 ÷ 1000"
    },
    "brick": {
        "name": "砌砖",
        "unit": "m³",
        "formula": "length * height * thickness",
        "description": "体积 = 长 × 高 × 厚"
    },
    "floor": {
        "name": "地面",
        "unit": "m²",
        "formula": "length * width",
        "description": "面积 = 长 × 宽"
    },
    "wall": {
        "name": "墙面",
        "unit": "m²",
        "formula": "(length + width) * 2 * height - openings",
        "description": "面积 = 周长 × 高 - 门窗洞口"
    }
}

def calculate(item_type, params):
    """计算工程量"""
    if item_type not in FORMULAS:
        return {"error": f"未知类型：{item_type}"}
    
    formula = FORMULAS[item_type]
    
    try:
        if item_type == "concrete":
            result = params.get("length", 0) * params.get("width", 0) * params.get("height", 0)
        elif item_type == "steel":
            result = params.get("length", 0) * params.get("weight_per_meter", 0) / 1000
        elif item_type == "brick":
            result = params.get("length", 0) * params.get("height", 0) * params.get("thickness", 0)
        elif item_type == "floor":
            result = params.get("length", 0) * params.get("width", 0)
        elif item_type == "wall":
            perimeter = (params.get("length", 0) + params.get("width", 0)) * 2
            openings = params.get("openings", 0)
            result = perimeter * params.get("height", 0) - openings
        else:
            result = 0
        
        return {
            "item": formula["name"],
            "result": round(result, 3),
            "unit": formula["unit"],
            "formula": formula["description"],
            "params": params
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="工程量计算工具")
    parser.add_argument("--type", "-t", required=True, help="计算类型")
    parser.add_argument("--params", "-p", type=json.loads, help="参数 JSON")
    parser.add_argument("--output", "-o", help="输出文件")
    
    args = parser.parse_args()
    
    result = calculate(args.type, args.params or {})
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到：{args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
