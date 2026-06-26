#!/usr/bin/env python3
"""
Anti-Hallucination Tool Hook
在工具调用后验证输出，检测潜在幻觉。
可作为 OpenClaw tool hook 使用。
"""
import json
import sys
import re


def check_tool_output(tool_name: str, output: str) -> dict:
    """检查工具输出，返回验证结果。"""
    result = {
        "tool": tool_name,
        "valid": True,
        "warnings": [],
    }

    # 检查空输出
    if not output or not output.strip():
        result["warnings"].append("工具返回空输出，可能是执行失败")
        result["valid"] = False

    # 检查错误信号
    error_patterns = [
        r"(?i)error",
        r"(?i)exception",
        r"(?i)traceback",
        r"(?i)failed",
        r"(?i)not found",
        r"找不到",
        r"失败",
        r"错误",
    ]
    for pattern in error_patterns:
        if re.search(pattern, output):
            result["warnings"].append(f"工具输出包含错误信号: {pattern}")
            result["valid"] = False
            break

    # 检查超长输出（可能是模型编造的）
    if len(output) > 50000:
        result["warnings"].append("工具输出异常长，可能是模型编造的")

    return result


def check_file_written(file_path: str, expected_content: str = None) -> dict:
    """验证文件是否真的被写入了。"""
    import os
    result = {
        "path": file_path,
        "exists": os.path.exists(file_path),
        "warnings": [],
    }

    if not result["exists"]:
        result["warnings"].append(f"文件不存在: {file_path}")
        return result

    if expected_content:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                actual = f.read()
            if expected_content not in actual:
                result["warnings"].append("文件内容与预期不符")
        except Exception as e:
            result["warnings"].append(f"读取文件失败: {e}")

    return result


if __name__ == "__main__":
    # 测试模式
    test_cases = [
        ("exec", "Error: command not found"),
        ("read", ""),
        ("write", "Successfully wrote 1234 bytes"),
    ]
    for tool, output in test_cases:
        result = check_tool_output(tool, output)
        print(f"\n{tool}: {json.dumps(result, ensure_ascii=False, indent=2)}")
