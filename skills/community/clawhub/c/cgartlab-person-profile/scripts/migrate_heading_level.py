#!/usr/bin/env python3
"""
migrate_heading_level.py — 批量迁移档案标题级别。

用法:
  python migrate_heading_level.py path/to/library/ --from # --to ## --dry-run
  python migrate_heading_level.py path/to/library/ --from # --to ##

功能:
  把 h1 级章节标题（# 章节名）迁移到 h2 级（## 章节名）
  注意：文档标题（YAML frontmatter 里的 title）不受影响。

重要：
  执行前会列出所有将被修改的位置。
  不 --dry-run 时才会真正写入。
"""
import os
import re
import sys
import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "执行摘要", "关系网络", "时间线与主要作品/言论", "核心价值观",
    "思维模式", "方法论", "创作如何变成影响", "争议与风险点",
    "可信度与信息差异", "可操作建议", "主要参考来源",
]

INDEX_FILES = ["人物-README.md", "person-README.md", "README.md"]


def migrate_file(path: Path, dry_run: bool) -> tuple:
    """迁移单份文件。返回 (issues, changes)。"""
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    new_lines = []
    changes = 0
    
    # 跳过 frontmatter
    in_frontmatter = False
    if lines and lines[0].startswith("---"):
        in_frontmatter = True
    
    for line in lines:
        if line.startswith("---") and not in_frontmatter:
            in_frontmatter = True
            new_lines.append(line)
            continue
        if in_frontmatter:
            if line.startswith("---"):
                in_frontmatter = False
            new_lines.append(line)
            continue
        
        # 匹配 h1 章节
        m = re.match(r"^# (.+)$", line)
        if m:
            section_name = m.group(1).strip()
            if section_name in REQUIRED_SECTIONS:
                new_lines.append(f"## {section_name}")
                changes += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    if changes > 0 and not dry_run:
        path.write_text("\n".join(new_lines), encoding="utf-8")
    
    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="档案库目录")
    parser.add_argument("--from", dest="from_level", default="#", help="源标题级别")
    parser.add_argument("--to", dest="to_level", default="##", help="目标标题级别")
    parser.add_argument("--dry-run", action="store_true", help="只报告，不修改")
    args = parser.parse_args()
    
    if args.from_level != "#" or args.to_level != "##":
        print("当前只支持 # → ## 的迁移（模板要求所有章节都是 ##）")
        sys.exit(1)
    
    lib_path = Path(args.path)
    if not lib_path.exists():
        print(f"错误: 目录不存在: {args.path}")
        sys.exit(1)
    
    mode = "[DRY-RUN] " if args.dry_run else ""
    
    total_changes = 0
    files_changed = 0
    
    print(f"{mode}扫描目录: {lib_path}")
    print(f"{mode}目标迁移: # → ##")
    print()
    
    for fname in sorted(os.listdir(lib_path)):
        if not fname.endswith(".md") or fname in INDEX_FILES:
            continue
        path = lib_path / fname
        changes = migrate_file(path, args.dry_run)
        if changes > 0:
            files_changed += 1
            total_changes += changes
            print(f"  📄 {fname}: {changes} 处")
    
    print(f"\n{'='*60}")
    print(f"{mode}修改文件数: {files_changed}")
    print(f"{mode}总修改处数: {total_changes}")
    
    if args.dry_run:
        print("\n提示：这是 dry-run。去掉 --dry-run 才能真正写入。")
    else:
        print("\n执行完成。建议立即运行 validate_library.py 验证。")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
