#!/usr/bin/env python3
"""
check_bidirectional.py — 检查档案库里的双向链完整性。

用法:
  python check_bidirectional.py path/to/library/

功能:
  找出所有单向链：A 档案链到 B，但 B 档案没有链回 A。
  输出所有需要补链的档案对。

退出码:
  0: 无单向链
  1: 存在单向链
"""
import os
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

INDEX_FILES = ["人物-README.md", "person-README.md", "README.md"]


def extract_wikilinks(content: str) -> set:
    """提取所有 [[...]] wikilinks。"""
    return set(re.findall(r"\[\[([^\]|#]+)", content))


def build_link_graph(lib_path: Path) -> dict:
    """构建档案名 -> 链向档案名集合 的映射。"""
    graph = {}
    for fname in os.listdir(lib_path):
        if not fname.endswith(".md") or fname in INDEX_FILES:
            continue
        name = fname[:-3]  # 去掉 .md
        path = lib_path / fname
        content = path.read_text(encoding="utf-8")
        links = extract_wikilinks(content)
        # 只保留库内存在的档案
        valid_links = set()
        for link in links:
            if (lib_path / f"{link}.md").exists():
                valid_links.add(link)
        graph[name] = valid_links
    return graph


def find_unidirectional(graph: dict) -> list:
    """找出单向链对：(A, B) 表示 A 链到 B 但 B 未链回 A。"""
    unidirectional = []
    for a, links_a in graph.items():
        for b in links_a:
            if b in graph and a not in graph[b]:
                unidirectional.append((a, b))
    return sorted(unidirectional)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="档案库目录")
    args = parser.parse_args()
    
    lib_path = Path(args.path)
    if not lib_path.exists():
        print(f"错误: 目录不存在: {args.path}")
        sys.exit(1)
    
    graph = build_link_graph(lib_path)
    print(f"档案总数: {len(graph)}")
    total_links = sum(len(v) for v in graph.values())
    print(f"总链接数: {total_links}")
    
    unidirectional = find_unidirectional(graph)
    if not unidirectional:
        print("✅ 双向链完整，无单向链。")
        sys.exit(0)
    
    print(f"\n❌ 发现 {len(unidirectional)} 对单向链：")
    print(f"{'A 档案':<25} {'B 档案':<25}")
    print("=" * 55)
    for a, b in unidirectional:
        print(f"{a:<25} → {b:<25}")
    
    print("\n需要在对应 B 档案的『关系网络』章节追加 [[A]] 条目。")
    sys.exit(1)


if __name__ == "__main__":
    main()
