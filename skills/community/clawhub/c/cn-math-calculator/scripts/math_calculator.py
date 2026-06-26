#!/usr/bin/env python3
"""
数学表达式计算器
使用AST解析器安全求值，完全不使用eval()
"""

import argparse
import ast
import sys
import json
import math
import operator
import re
from typing import Dict, Any

# 安全的数学函数映射
SAFE_FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'log': math.log10,
    'ln': math.log,
    'log2': math.log2,
    'sqrt': math.sqrt,
    'abs': abs,
    'floor': math.floor,
    'ceil': math.ceil,
    'round': round,
    'exp': math.exp,
    'pow': pow,
}

SAFE_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
}

# 安全的二元运算符映射
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# 安全的一元运算符映射
SAFE_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# 单位换算表
UNIT_CONVERSIONS = {
    'length': {
        'km': 1000, '公里': 1000, '千米': 1000,
        'm': 1, '米': 1,
        'cm': 0.01, '厘米': 0.01,
        'mm': 0.001, '毫米': 0.001,
        'mile': 1609.344, '英里': 1609.344,
        'yard': 0.9144, '码': 0.9144,
        'ft': 0.3048, '英尺': 0.3048,
        'inch': 0.0254, '英寸': 0.0254,
        '里': 500, '丈': 3.333, '尺': 0.333, '寸': 0.0333,
    },
    'weight': {
        't': 1000, '吨': 1000,
        'kg': 1, '千克': 1, '公斤': 1,
        'g': 0.001, '克': 0.001,
        'mg': 0.000001, '毫克': 0.000001,
        'lb': 0.453592, '磅': 0.453592,
        'oz': 0.0283495, '盎司': 0.0283495,
        '斤': 0.5, '两': 0.05, '钱': 0.005,
    },
    'temperature': {
        'c': 'c', '摄氏度': 'c', '摄氏': 'c',
        'f': 'f', '华氏度': 'f', '华氏': 'f',
        'k': 'k', '开尔文': 'k',
    },
    'area': {
        'km2': 1e6, '平方公里': 1e6,
        'm2': 1, '平方米': 1, '平米': 1,
        'cm2': 0.0001, '平方厘米': 0.0001,
        'ha': 10000, '公顷': 10000,
        'acre': 4046.86, '英亩': 4046.86,
        '亩': 666.67,
    },
}


class ASTEvaluator:
    """基于AST的安全表达式求值器，完全不使用eval()"""

    def __init__(self):
        self.constants = SAFE_CONSTANTS
        self.functions = SAFE_FUNCTIONS

    def evaluate(self, expression: str) -> float:
        """安全地计算数学表达式"""
        # 预处理：替换 ^ 为 **（Python幂运算符）
        expr = expression.strip()
        expr = expr.replace('^', '**')

        # 解析为AST
        try:
            tree = ast.parse(expr, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"表达式语法错误: {e}")

        # 遍历AST求值
        result = self._visit(tree.body)
        return float(result)

    def _visit(self, node):
        """递归遍历AST节点"""
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"不支持的常量类型: {type(node.value)}")

        elif isinstance(node, ast.Num):  # Python 3.7 兼容
            return node.n

        elif isinstance(node, ast.Name):
            # 只允许预定义的常量
            name = node.id.lower()
            if name in self.constants:
                return self.constants[name]
            raise ValueError(f"未知常量: {node.id}")

        elif isinstance(node, ast.BinOp):
            left = self._visit(node.left)
            right = self._visit(node.right)
            op_type = type(node.op)
            if op_type in SAFE_OPERATORS:
                return SAFE_OPERATORS[op_type](left, right)
            raise ValueError(f"不支持的运算符: {op_type.__name__}")

        elif isinstance(node, ast.UnaryOp):
            operand = self._visit(node.operand)
            op_type = type(node.op)
            if op_type in SAFE_UNARY_OPERATORS:
                return SAFE_UNARY_OPERATORS[op_type](operand)
            raise ValueError(f"不支持的一元运算符: {op_type.__name__}")

        elif isinstance(node, ast.Call):
            # 只允许预定义的函数
            if isinstance(node.func, ast.Name):
                func_name = node.func.id.lower()
                if func_name in self.functions:
                    args = [self._visit(arg) for arg in node.args]
                    return self.functions[func_name](*args)
                raise ValueError(f"未知函数: {node.func.id}")
            raise ValueError("不支持复杂的函数调用")

        else:
            raise ValueError(f"不支持的表达式类型: {type(node).__name__}")


def safe_eval(expression: str) -> float:
    """安全求值（AST解析，不使用eval）"""
    evaluator = ASTEvaluator()
    return evaluator.evaluate(expression)


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """温度换算"""
    if from_unit == 'c':
        celsius = value
    elif from_unit == 'f':
        celsius = (value - 32) * 5 / 9
    elif from_unit == 'k':
        celsius = value - 273.15
    else:
        raise ValueError(f"不支持的温度单位: {from_unit}")

    if to_unit == 'c':
        return celsius
    elif to_unit == 'f':
        return celsius * 9 / 5 + 32
    elif to_unit == 'k':
        return celsius + 273.15
    else:
        raise ValueError(f"不支持的温度单位: {to_unit}")


def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
    """单位换算"""
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if from_unit == to_unit:
        return value

    for category, units in UNIT_CONVERSIONS.items():
        if from_unit in units and to_unit in units:
            if category == 'temperature':
                return convert_temperature(value, units[from_unit], units[to_unit])
            else:
                factor_from = units[from_unit]
                factor_to = units[to_unit]
                return value * factor_from / factor_to

    raise ValueError(f"不支持的单位换算: {from_unit} -> {to_unit}")


def parse_convert_request(text: str) -> tuple:
    """解析单位换算请求"""
    cn_pattern = r'([\d\.]+)\s*([^\s等于]+?)\s*等于?\s*(?:多少)?\s*([^\s]+)'
    match = re.search(cn_pattern, text)
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(3)
        return value, from_unit, to_unit

    en_pattern = r'([\d\.]+)\s*(\w+)\s+to\s+(\w+)'
    match = re.search(en_pattern, text, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(3)
        return value, from_unit, to_unit

    return None, None, None


def main():
    parser = argparse.ArgumentParser(description="数学表达式计算器")
    parser.add_argument("expression", nargs="?", help="数学表达式")
    parser.add_argument("-c", "--convert", help="单位换算")
    parser.add_argument("-j", "--json", action="store_true", help="JSON输出")

    args = parser.parse_args()

    result = None
    error = None

    try:
        if args.convert:
            value, from_unit, to_unit = parse_convert_request(args.convert)
            if value is None:
                value, from_unit, to_unit = parse_convert_request(args.expression)

            if value is not None:
                result = convert_unit(value, from_unit, to_unit)
            else:
                error = "无法解析单位换算请求"
        elif args.expression:
            result = safe_eval(args.expression)
        else:
            error = "请提供数学表达式或换算请求"
    except Exception as e:
        error = str(e)

    if args.json:
        output = {
            "success": result is not None,
            "result": result,
            "error": error
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if error:
            print(f"错误: {error}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"结果: {result}")


if __name__ == "__main__":
    main()
