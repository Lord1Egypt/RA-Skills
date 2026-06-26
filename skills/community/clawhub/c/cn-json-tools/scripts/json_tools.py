#!/usr/bin/env python3
"""cn-json-tools - JSON工具箱"""
import json, sys

def format_json(text, indent=2):
    """格式化JSON"""
    try:
        obj = json.loads(text)
        return json.dumps(obj, indent=indent, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"JSON解析错误: {e}"

def minify_json(text):
    """压缩JSON"""
    try:
        obj = json.loads(text)
        return json.dumps(obj, separators=(',', ':'))
    except json.JSONDecodeError as e:
        return f"JSON解析错误: {e}"

def validate_json(text):
    """验证JSON"""
    try:
        json.loads(text)
        return {"valid": True}
    except json.JSONDecodeError as e:
        return {"valid": False, "error": str(e)}

def extract_keys(text, path=None):
    """提取JSON中的值"""
    try:
        obj = json.loads(text)
        if path:
            for key in path.split('.'):
                obj = obj[key]
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"提取失败: {e}"

if __name__ == '__main__':
    text = sys.stdin.read() if not sys.stdin.isatty() else sys.argv[1] if len(sys.argv) > 1 else '{"key": "value"}'
    print(format_json(text))
