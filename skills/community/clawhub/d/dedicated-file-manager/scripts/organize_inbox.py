#!/usr/bin/env python3
"""
Inbox 整理脚本
扫描 inbox 目录，自动分流文件到对应目录
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta


# 文件类型到目标目录的映射
FILE_TYPE_RULES = {
    # 文档类 -> references/
    "references": [
        ".md", ".docx", ".doc", ".pdf", ".txt", ".xlsx", ".xls",
        ".csv", ".pptx", ".ppt", ".odt", ".ods", ".odp"
    ],
    # 代码类 -> projects/
    "projects": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".cs", ".cpp", ".c", ".h",
        ".java", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
        ".html", ".css", ".scss", ".sass", ".less", ".vue", ".svelte",
        ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
        ".sql", ".r", ".R",
        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".env"
    ],
    # 素材类 -> scratch/ (稍后由用户分类)
    "scratch": [
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
        ".psd", ".ai", ".sketch", ".fig", ".xd",
        ".mp3", ".wav", ".ogg", ".flac", ".aac",
        ".mp4", ".mov", ".avi", ".mkv", ".webm",
        ".fbx", ".obj", ".blend", ".max", ".ma", ".mb",
        ".ttf", ".otf", ".woff", ".woff2"
    ],
    # Unity 专项
    "unity": [
        ".unity", ".prefab", ".mat", ".asset", ".shader",
        ".compute", ".asmdef", ".controller", ".anim",
        ".physicMaterial", ".inputactions"
    ]
}

# 临时文件特征
TEMP_PATTERNS = ["_temp", "_tmp", "~", "_backup", "_copy", "_副本", ".bak", ".tmp", ".cache", ".log"]


def get_destination(file_path: Path, root: Path) -> str:
    """根据文件类型确定目标目录"""
    ext = file_path.suffix.lower()
    name_lower = file_path.name.lower()

    # 检查临时文件
    for pattern in TEMP_PATTERNS:
        if pattern in name_lower:
            return "scratch"

    # 检查类型
    for category, extensions in FILE_TYPE_RULES.items():
        if ext in extensions:
            if category == "projects":
                return "projects"
            elif category == "unity":
                return "projects/unity"  # Unity 专用子目录
            else:
                return category

    return "scratch"  # 默认到 scratch


def organize_inbox(inbox_path: str, root_path: str, dry_run: bool = False) -> dict:
    """整理 inbox 目录"""
    inbox = Path(inbox_path)
    root = Path(root_path)

    if not inbox.exists():
        return {"error": f"Inbox 不存在: {inbox_path}"}

    if not inbox.is_dir():
        return {"error": f"不是目录: {inbox_path}"}

    results = {
        "processed": [],
        "moved": [],
        "errors": [],
        "skipped": []
    }

    # 确保目标目录存在
    for subdir in ["references", "projects", "scratch", "archives"]:
        target = root / subdir
        if not target.exists():
            if not dry_run:
                target.mkdir(parents=True, exist_ok=True)

    # 处理每个文件
    for item in inbox.iterdir():
        if item.is_dir():
            continue

        results["processed"].append(item.name)
        destination = get_destination(item, root)
        target_dir = root / destination

        # 处理冲突
        target_path = target_dir / item.name
        if target_path.exists():
            # 同名文件，添加序号
            base = item.stem
            ext = item.suffix
            counter = 1
            while target_path.exists():
                new_name = f"{base}_{counter:02d}{ext}"
                target_path = target_dir / new_name
                counter += 1

        results["moved"].append({
            "file": item.name,
            "from": str(item),
            "to": str(target_path),
            "category": destination
        })

        if not dry_run:
            shutil.move(str(item), str(target_path))

    return results


def clean_old_temp(root_path: str, days: int = 30, dry_run: bool = False) -> dict:
    """清理旧临时文件"""
    root = Path(root_path)
    scratch = root / "scratch"

    if not scratch.exists():
        return {"cleaned": [], "skipped": []}

    cutoff = datetime.now() - timedelta(days=days)
    results = {"cleaned": [], "skipped": []}

    for item in scratch.iterdir():
        if item.is_file():
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff:
                results["cleaned"].append(str(item))
                if not dry_run:
                    # 移入 archives
                    archives = root / "archives"
                    archives.mkdir(exist_ok=True)
                    shutil.move(str(item), str(archives / item.name))
            else:
                results["skipped"].append(str(item))

    return results


def generate_report(organize_results: dict, clean_results: dict) -> str:
    """生成整理报告"""
    lines = [
        "# 定期整理报告",
        "",
        f"**日期**：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        ""
    ]

    # 移动文件
    if organize_results.get("moved"):
        lines.append("## 已整理文件")
        lines.append("")
        lines.append("| 文件名 | 原位置 | 目标位置 | 类型 |")
        lines.append("|--------|--------|----------|------|")

        for item in organize_results["moved"]:
            filename = Path(item["file"]).name
            from_path = Path(item["from"]).name
            lines.append(f"| {filename} | {from_path} | {item['category']}/ | {item['category']} |")
        lines.append("")
    else:
        lines.append("## 已整理文件")
        lines.append("*无文件需要整理*")
        lines.append("")

    # 清理临时文件
    if clean_results.get("cleaned"):
        lines.append("## 已清理临时文件")
        lines.append("")
        for f in clean_results["cleaned"]:
            lines.append(f"- {Path(f).name}")
        lines.append("")
        lines.append(f"*共清理 {len(clean_results['cleaned'])} 个文件，已移入 archives/*")
        lines.append("")
    else:
        lines.append("## 已清理临时文件")
        lines.append("*无过期临时文件*")
        lines.append("")

    # 错误
    if organize_results.get("errors"):
        lines.append("## 错误")
        for err in organize_results["errors"]:
            lines.append(f"- {err}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*此报告由 file-manager skill 自动生成*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="整理 inbox 目录")
    parser.add_argument("root", help="根目录路径（专属文件夹）")
    parser.add_argument("--inbox", "-i", default="inbox", help="Inbox 目录名（默认 inbox）")
    parser.add_argument("--clean-days", type=int, default=30, help="临时文件保留天数（默认30）")
    parser.add_argument("--dry-run", "-n", action="store_true", help="模拟运行，不实际移动文件")
    parser.add_argument("--report", "-r", help="报告输出路径")

    args = parser.parse_args()

    inbox_path = Path(args.root) / args.inbox

    # 整理 inbox
    organize_results = organize_inbox(str(inbox_path), args.root, args.dry_run)

    if "error" in organize_results:
        print(f"错误: {organize_results['error']}")
        return 1

    # 清理临时文件
    clean_results = clean_old_temp(args.root, args.clean_days, args.dry_run)

    # 生成报告
    report = generate_report(organize_results, clean_results)

    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"报告已保存: {args.report}")
    else:
        print(report)

    # 输出摘要
    print(f"\n摘要: 整理 {len(organize_results['moved'])} 个文件, 清理 {len(clean_results['cleaned'])} 个临时文件")

    return 0


if __name__ == "__main__":
    exit(main())
