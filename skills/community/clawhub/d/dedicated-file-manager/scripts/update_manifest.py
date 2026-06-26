#!/usr/bin/env python3
"""
Manifest 更新脚本
扫描目录并更新 manifest.md 文件
"""

import os
import argparse
from pathlib import Path
from datetime import datetime


def generate_manifest_content(root_path: str) -> str:
    """生成 manifest.md 内容"""
    root = Path(root_path)

    lines = [
        "# 文件清单",
        "",
        f"**更新时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**根目录**：{root}",
        "",
        "---",
        ""
    ]

    # 分类统计
    categories = {
        "文档": [".md", ".docx", ".doc", ".pdf", ".txt", ".xlsx", ".xls", ".csv", ".pptx", ".ppt"],
        "代码": [".py", ".js", ".ts", ".cs", ".cpp", ".java", ".go", ".rs", ".rb", ".html", ".css", ".json", ".xml", ".yaml", ".yml"],
        "素材": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp3", ".wav", ".ogg", ".mp4", ".mov", ".webm", ".fbx", ".obj", ".blend"],
        "Unity": [".unity", ".prefab", ".mat", ".asset", ".shader", ".controller", ".anim"],
        "配置": [".ini", ".toml", ".conf", ".env"],
        "压缩": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "临时": ["_temp", "_tmp", "~", ".tmp", ".bak", ".cache", ".log"]
    }

    # 文件列表
    files_by_category = {cat: [] for cat in categories}
    other_files = []

    for item in root.rglob("*"):
        if item.is_file() and not item.name.startswith("manifest"):
            ext = item.suffix.lower()
            matched = False

            for cat, extensions in categories.items():
                if ext in extensions or any(p in item.name for p in extensions if len(p) > 2):
                    files_by_category[cat].append(item)
                    matched = True
                    break

            if not matched:
                other_files.append(item)

    # 生成分类表格
    for cat, files in files_by_category.items():
        if files:
            lines.append(f"## {cat}类文件")
            lines.append("")
            lines.append("| 文件名 | 相对路径 | 大小 | 修改时间 |")
            lines.append("|--------|----------|------|----------|")

            for f in sorted(files, key=lambda x: x.name):
                size = f.stat().st_size
                size_str = format_size(size)
                mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')
                rel_path = f.relative_to(root)
                lines.append(f"| {f.name} | {rel_path} | {size_str} | {mtime} |")

            lines.append("")

    # 其他文件
    if other_files:
        lines.append("## 其他文件")
        lines.append("")
        lines.append("| 文件名 | 相对路径 | 大小 | 修改时间 |")
        lines.append("|--------|----------|------|----------|")

        for f in sorted(other_files, key=lambda x: x.name):
            size = f.stat().st_size
            size_str = format_size(size)
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')
            rel_path = f.relative_to(root)
            lines.append(f"| {f.name} | {rel_path} | {size_str} | {mtime} |")

        lines.append("")

    # 目录结构
    lines.append("## 目录结构")
    lines.append("```")
    lines.append(f"./ ({root.name})")

    def print_tree(directory: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
        if current_depth >= max_depth:
            return

        items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        dirs = []
        files = []

        for item in items:
            if item.name.startswith(".") or item.name.startswith("_"):
                continue
            if item.is_dir():
                dirs.append(item)
            else:
                files.append(item)

        for i, d in enumerate(dirs):
            is_last = (i == len(dirs) - 1 and len(files) == 0)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{d.name}/")
            extension = "    " if is_last else "│   "
            print_tree(d, prefix + extension, max_depth, current_depth + 1)

        for i, f in enumerate(files):
            is_last = (i == len(files) - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{f.name}")

    print_tree(root)
    lines.append("```")

    return "\n".join(lines)


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def main():
    parser = argparse.ArgumentParser(description="生成或更新 manifest.md")
    parser.add_argument("path", help="目录路径")
    parser.add_argument("--output", "-o", help="输出文件路径（默认在目录内创建 manifest.md）")

    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"错误: 路径不存在: {root}")
        return 1

    if not root.is_dir():
        print(f"错误: 路径不是目录: {root}")
        return 1

    output_path = Path(args.output) if args.output else root / "manifest.md"

    content = generate_manifest_content(args.path)
    output_path.write_text(content, encoding="utf-8")

    print(f"Manifest 已更新: {output_path}")
    return 0


if __name__ == "__main__":
    exit(main())
