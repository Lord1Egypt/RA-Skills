#!/usr/bin/env python3
"""
auto_link.py — Claude-Obsidian 双向链接自动织网工具
扫描 vault 中所有 .md 文件，检测死链和孤儿笔记
"""

import re
import os
import sys
from pathlib import Path
from collections import defaultdict

def extract_links(content):
    """提取 [[双向链接]] 中的笔记名"""
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def extract_title(content):
    """从 frontmatter 或首行提取标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def get_note_title(filepath, content):
    """获取笔记标题，优先用 frontmatter"""
    title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return extract_title(content) or filepath.stem

def scan_vault(vault_path, dry_run=False):
    vault = Path(vault_path)
    if not vault.exists():
        print(f"❌ Vault 不存在: {vault_path}")
        return

    all_files = list(vault.rglob("*.md"))
    # 排除 cache 和隐藏文件
    all_files = [f for f in all_files if not any(p.startswith('.') for p in f.parts)]

    # 建立 title -> filepath 映射
    title_to_file = {}
    file_to_title = {}
    all_links = defaultdict(list)  # filepath -> [linked_titles]
    orphan_notes = []

    for f in all_files:
        try:
            content = f.read_text(encoding='utf-8')
        except Exception:
            continue

        title = get_note_title(f, content)
        if title:
            title_to_file[title.lower()] = f
            file_to_title[f] = title

        links = extract_links(content)
        if links:
            all_links[f] = links
        else:
            # 非 index/CLAUDE.md 的无链接笔记
            if f.name not in ['index.md', 'CLAUDE.md', 'SCHEMA.md']:
                orphan_notes.append(f)

    # 检测死链
    dead_links = []
    for f, links in all_links.items():
        for link in links:
            link_clean = link.strip().lower()
            # 支持 | 别名语法 [[笔记名|显示名]]
            if '|' in link_clean:
                link_clean = link_clean.split('|')[0].strip()
            if link_clean not in title_to_file:
                dead_links.append({
                    'file': f,
                    'link': link,
                    'suggestion': link_clean.replace(' ', '-').lower()
                })

    # 孤儿笔记（被链接但从未被链接到的笔记）
    linked_files = set()
    for f, links in all_links.items():
        for link in links:
            link_clean = link.split('|')[0].strip().lower()
            if link_clean in title_to_file:
                linked_files.add(title_to_file[link_clean])

    orphans = [f for f in orphan_notes if f not in linked_files]

    # 输出报告
    print("=" * 50)
    print("📊 Claude-Obsidian 链接分析报告")
    print("=" * 50)
    print(f"总笔记数：{len(all_files)}")
    print(f"总链接数：{sum(len(v) for v in all_links.values())}")
    print()

    if dead_links:
        print("🚨 死链报告（共 {} 处）".format(len(dead_links)))
        for dl in dead_links:
            print(f"  ❌ [[{dl['link']}]]")
            print(f"     在: {dl['file'].relative_to(vault)}")
            print(f"     建议: [[{dl['suggestion']}]]")
        print()
    else:
        print("✅ 无死链")

    if orphans:
        print("📌 孤儿笔记（共 {} 篇，未被任何笔记链接）".format(len(orphans)))
        for o in orphans:
            print(f"  🔗 {file_to_title.get(o, o.stem)} → {o.relative_to(vault)}")
        print()
    else:
        print("✅ 无孤儿笔记")

    # 生成修复建议（dry_run=false 时输出可执行脚本）
    if not dry_run and (dead_links or orphans):
        fix_script = vault / ".claude_fix_suggestions.sh"
        with open(fix_script, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n# Claude-Obsidian 修复建议（手动确认后执行）\n\n")
            for dl in dead_links:
                f.write(f"# 在 {dl['file'].relative_to(vault)} 中将 [[{dl['link']}]] 替换为 [[{dl['suggestion']}]]\n")
        print(f"💡 修复建议已保存: {fix_script}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Claude-Obsidian 双向链接织网工具")
    parser.add_argument("vault_path", help="Vault 目录路径")
    parser.add_argument("--dry-run", action="store_true", help="仅报告，不生成修复脚本")
    args = parser.parse_args()
    scan_vault(args.vault_path, args.dry_run)
