#!/usr/bin/env python3
"""
deterministic-calc Skill - 确定性计算技能

核心理念：大模型擅长预测（猜），但不擅长确定性计算。
本 Skill 将确定性计算固化为代码执行，避免模型"猜"结果。
"""

import subprocess
import re
import ast
import operator
from typing import Dict, Any, Optional, List

__version__ = "1.0.0"
__author__ = "OpenClaw Community"


# ============================================================================
# 安全的数学表达式求值（无 eval 风险）
# ============================================================================

# 支持的运算符
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# 支持的函数
ALLOWED_FUNCTIONS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'pow': pow,
}


def _safe_eval_node(node: ast.AST) -> Any:
    """递归安全求值 AST 节点"""
    
    # 数字
    if isinstance(node, ast.Num):  # Python 3.7 及以下
        return node.n
    
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"不支持的常量类型：{type(node.value)}")
    
    # 二元运算
    if isinstance(node, ast.BinOp):
        left = _safe_eval_node(node.left)
        right = _safe_eval_node(node.right)
        op_type = type(node.op)
        
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"不支持的运算符：{op_type}")
        
        # 防止除零
        if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
            raise ValueError("除零错误")
        
        # 防止过大指数
        if op_type == ast.Pow and isinstance(right, (int, float)) and abs(right) > 1000:
            raise ValueError("指数过大")
        
        op_func = ALLOWED_OPERATORS[op_type]
        return op_func(left, right)
    
    # 一元运算
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval_node(node.operand)
        op_type = type(node.op)
        
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"不支持的一元运算符：{op_type}")
        
        op_func = ALLOWED_OPERATORS[op_type]
        return op_func(operand)
    
    # 函数调用
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("只支持简单函数调用")
        
        func_name = node.func.id
        
        if func_name not in ALLOWED_FUNCTIONS:
            raise ValueError(f"不支持的函数：{func_name}")
        
        func = ALLOWED_FUNCTIONS[func_name]
        args = [_safe_eval_node(arg) for arg in node.args]
        
        return func(*args)
    
    # 列表
    if isinstance(node, ast.List):
        return [_safe_eval_node(elt) for elt in node.elts]
    
    # 元组
    if isinstance(node, ast.Tuple):
        return tuple(_safe_eval_node(elt) for elt in node.elts)
    
    raise ValueError(f"不支持的表达式类型：{type(node)}")


def safe_eval(expression: str) -> Dict[str, Any]:
    """
    安全执行数学表达式（无代码注入风险）
    
    参数:
        expression: 数学表达式字符串
    
    返回:
        dict: {"success": bool, "result": value, "error": str}
    """
    try:
        # 解析表达式
        tree = ast.parse(expression.strip(), mode='eval')
        
        # 安全求值
        result = _safe_eval_node(tree.body)
        
        return {
            "success": True,
            "expression": expression,
            "result": result
        }
        
    except Exception as e:
        return {
            "success": False,
            "expression": expression,
            "error": str(e)
        }


# ============================================================================
# 数学计算（支持更多运算符）
# ============================================================================

def calculate(expression: str) -> Dict[str, Any]:
    """
    执行数学表达式计算
    
    支持：+ - * / // % ** () 以及 math 函数
    
    参数:
        expression: 数学表达式字符串
    
    返回:
        dict: {"success": bool, "result": value, "error": str}
    """
    try:
        # 尝试使用 safe_eval
        result = safe_eval(expression)
        
        if result["success"]:
            return result
        
        # 如果 safe_eval 失败，尝试用 Python 执行
        return run_python(f"print({expression})")
        
    except Exception as e:
        return {
            "success": False,
            "expression": expression,
            "error": str(e)
        }


# ============================================================================
# Python 代码执行
# ============================================================================

def run_python(code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    执行 Python 代码并返回结果
    
    参数:
        code: Python 代码
        timeout: 超时时间（秒）
    
    返回:
        dict: {"success": bool, "stdout": str, "stderr": str, "exit_code": int}
    """
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "code": code
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"代码执行超时（{timeout}秒）",
            "exit_code": -1,
            "code": code
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "code": code
        }


# ============================================================================
# Shell 命令执行
# ============================================================================

def run_shell(command: str, timeout: int = 30, shell: bool = True) -> Dict[str, Any]:
    """
    执行 Shell 命令并返回结果
    
    参数:
        command: Shell 命令
        timeout: 超时时间（秒）
        shell: 是否使用 shell 执行
    
    返回:
        dict: {"success": bool, "stdout": str, "stderr": str, "exit_code": int}
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "command": command
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"命令执行超时（{timeout}秒）",
            "exit_code": -1,
            "command": command
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "command": command
        }


# ============================================================================
# 文件操作（确定性）
# ============================================================================

def read_file(path: str, max_bytes: int = 1024 * 1024) -> Dict[str, Any]:
    """
    读取文件内容（确定性操作，不依赖模型）
    
    参数:
        path: 文件路径
        max_bytes: 最大读取字节数
    
    返回:
        dict: {"success": bool, "content": str, "error": str}
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read(max_bytes)
        
        return {
            "success": True,
            "path": path,
            "content": content,
            "bytes_read": len(content.encode('utf-8'))
        }
        
    except Exception as e:
        return {
            "success": False,
            "path": path,
            "error": str(e)
        }


def write_file(path: str, content: str) -> Dict[str, Any]:
    """
    写入文件内容（确定性操作）
    
    参数:
        path: 文件路径
        content: 文件内容
    
    返回:
        dict: {"success": bool, "bytes_written": int}
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "path": path,
            "bytes_written": len(content.encode('utf-8'))
        }
        
    except Exception as e:
        return {
            "success": False,
            "path": path,
            "error": str(e)
        }


# ============================================================================
# 数据验证（确定性）
# ============================================================================

def validate_json(json_string: str) -> Dict[str, Any]:
    """
    验证 JSON 字符串是否有效
    
    参数:
        json_string: JSON 字符串
    
    返回:
        dict: {"success": bool, "data": parsed_data, "error": str}
    """
    import json
    
    try:
        data = json.loads(json_string)
        return {
            "success": True,
            "valid": True,
            "data": data
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "valid": False,
            "error": str(e)
        }


def validate_xml(xml_string: str) -> Dict[str, Any]:
    """
    验证 XML 字符串是否有效
    
    参数:
        xml_string: XML 字符串
    
    返回:
        dict: {"success": bool, "valid": bool, "error": str}
    """
    import xml.etree.ElementTree as ET
    
    try:
        ET.fromstring(xml_string)
        return {
            "success": True,
            "valid": True
        }
    except ET.ParseError as e:
        return {
            "success": False,
            "valid": False,
            "error": str(e)
        }


# ============================================================================
# CLI 入口
# ============================================================================

if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("用法：python -m deterministic_calc <command> [args]")
        print("命令:")
        print("  calc <expression>     - 计算数学表达式")
        print("  safe <expression>     - 安全求值")
        print("  python <code>         - 执行 Python 代码")
        print("  shell <command>       - 执行 Shell 命令")
        print("  read <file>           - 读取文件")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "calc":
        expr = " ".join(sys.argv[2:])
        result = calculate(expr)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "safe":
        expr = " ".join(sys.argv[2:])
        result = safe_eval(expr)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "python":
        code = " ".join(sys.argv[2:])
        result = run_python(code)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "shell":
        cmd = " ".join(sys.argv[2:])
        result = run_shell(cmd)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "read":
        path = sys.argv[2] if len(sys.argv) > 2 else "/dev/stdin"
        result = read_file(path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
