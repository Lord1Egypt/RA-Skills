#!/usr/bin/env python3
"""
目录扫描脚本
扫描指定目录，生成结构化的 JSON 报告
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def get_file_info(path: Path) -> dict:
    """获取文件信息"""
    stat = path.stat()
    return {
        "name": path.name,
        "path": str(path),
        "relative_path": str(path),
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "extension": path.suffix.lower(),
        "is_dir": path.is_dir()
    }


def scan_directory(root_path: str, max_depth: int = 3) -> dict:
    """扫描目录"""
    root = Path(root_path)

    if not root.exists():
        return {"error": f"路径不存在: {root_path}"}

    if not root.is_dir():
        return {"error": f"路径不是目录: {root_path}"}

    result = {
        "scan_time": datetime.now().isoformat(),
        "root_path": str(root),
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "by_extension": defaultdict(lambda: {"count": 0, "total_size": 0}),
        "files": [],
        "dirs": []
    }

    for item in root.rglob("*"):
        # 限制深度
        depth = len(item.relative_to(root).parts)
        if depth > max_depth:
            continue

        if item.is_file():
            file_info = get_file_info(item)
            result["files"].append(file_info)
            result["total_files"] += 1
            result["total_size"] += file_info["size"]

            ext = file_info["extension"] or "(无后缀)"
            result["by_extension"][ext]["count"] += 1
            result["by_extension"][ext]["total_size"] += file_info["size"]

        elif item.is_dir():
            result["dirs"].append({
                "name": item.name,
                "path": str(item),
                "relative_path": str(item.relative_to(root))
            })
            result["total_dirs"] += 1

    # 转换为普通字典
    result["by_extension"] = dict(result["by_extension"])

    return result


def analyze_problems(scan_result: dict) -> list:
    """分析扫描结果，识别问题"""
    problems = []

    for file_info in scan_result.get("files", []):
        problems_found = []

        # 检查空格
        if " " in file_info["name"]:
            problems_found.append("文件名包含空格")

        # 检查中文
        if any('\u4e00' <= c <= '\u9fff' for c in file_info["name"]):
            problems_found.append("文件名包含中文（代码类文件建议用英文）")

        # 检查过长名称
        if len(file_info["name"]) > 100:
            problems_found.append("文件名过长")

        # 检查无后缀
        if not file_info["extension"]:
            problems_found.append("文件无后缀")

        # 检查疑似临时文件
        temp_patterns = ["_temp", "_tmp", "~", "_backup", "_copy", "_副本"]
        if any(p in file_info["name"] for p in temp_patterns):
            problems_found.append("疑似临时/备份文件")

        # 检查疑似重复
        name_without_ext = file_info["name"].rsplit(".", 1)[0]
        if any("_v" in name_without_ext or "_draft" in name_without_ext or "_final" in name_without_ext
               for _ in [1]):
            problems_found.append("疑似版本文件")

        if problems_found:
            problems.append({
                "file": file_info["path"],
                "issues": problems_found
            })

    return problems


def main():
    parser = argparse.ArgumentParser(description="扫描目录并生成报告")
    parser.add_argument("path", help="要扫描的目录路径")
    parser.add_argument("--max-depth", type=int, default=3, help="最大扫描深度（默认3）")
    parser.add_argument("--output", "-o", help="输出文件路径（JSON）")
    parser.add_argument("--analyze", "-a", action="store_true", help="分析问题")

    args = parser.parse_args()

    result = scan_directory(args.path, args.max_depth)

    if "error" in result:
        print(f"错误: {result['error']}")
        return 1

    if args.analyze:
        result["problems"] = analyze_problems(result)

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"报告已保存到: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    exit(main())
