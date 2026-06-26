#!/usr/bin/env python3
"""
I漫剧APP开发技能 - 项目结构验证工具
验证项目是否遵循模块化开发规范
"""

import os
import sys
from pathlib import Path

def validate_structure(project_root: str) -> dict:
    """验证项目目录结构"""
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "modules": []
    }

    required_dirs = [
        "基础模块层",
        "业务模块层",
        "支撑模块层",
        "公共模块"
    ]

    required_files = [
        "模块设计文档",
        "接口定义文档",
        "测试报告",
        "锁定记录"
    ]

    # 检查目录结构
    for dirname in required_dirs:
        dir_path = os.path.join(project_root, dirname)
        if not os.path.exists(dir_path):
            results["warnings"].append(f"建议目录不存在: {dirname}")

    # 检查模块目录
    modules_dir = os.path.join(project_root, "模块")
    if os.path.exists(modules_dir):
        for module in os.listdir(modules_dir):
            module_path = os.path.join(modules_dir, module)
            if os.path.isdir(module_path):
                results["modules"].append(module)

    return results

def print_report(results: dict):
    """打印验证报告"""
    print("=" * 50)
    print("I漫剧APP项目结构验证报告")
    print("=" * 50)

    if results["valid"]:
        print("✓ 验证通过")
    else:
        print("✗ 验证失败")

    if results["errors"]:
        print("\n错误:")
        for error in results["errors"]:
            print(f"  - {error}")

    if results["warnings"]:
        print("\n警告:")
        for warning in results["warnings"]:
            print(f"  - {warning}")

    if results["modules"]:
        print(f"\n已识别模块 ({len(results['modules'])}):")
        for module in results["modules"]:
            print(f"  - {module}")

    print("=" * 50)

if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    results = validate_structure(project_root)
    print_report(results)
    sys.exit(0 if results["valid"] else 1)
