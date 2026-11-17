#!/usr/bin/env python3
"""
check_prohibitions.py — 扫描档案库的禁词、破折号、格式违规。

用法:
  python check_prohibitions.py path/to/library/
  python check_prohibitions.py path/to/archive.md

输出:
  列出所有违规位置和内容

退出码:
  0: 无违规
  1: 有违规
"""
import os
import re
import sys
import argparse
from pathlib import Path

INDEX_FILES = ["人物-README.md", "person-README.md", "README.md"]

# 禁用破折号
PROHIBITED_DASHES = ["——", "—", "–"]

# 商业黑话
BUSINESS_JARGON = [
    "闭环", "能力沉淀", "赋能", "抓手", "底层逻辑",
    "内容矩阵", "拉通", "复利", "范本", "范式",
]

# 模型路标词
MODEL_BOILERPLATE = [
    "值得注意的是", "本质上", "由此可见",
    "从某种意义上说", "总之", "总体而言",
]

# 借喻词（谨慎使用，Obsidian 语境下"仓库"字面合理）
METAPHOR_WORDS = ["抽屉", "温度", "坍塌", "浪潮", "钥匙", "底座"]

# AI 残留
AI_RESIDUE_PATTERNS = [
    r"author:\s*ChatGPT",
    r"author:\s*GPT-4",
    r"<!--\s*AI\s*generated",
]


def is_inside_quotes(line: str, idx: int) -> bool:
    """判断 idx 位置是否在引号内（中英文引号都识别）。
    
    支持：
    - 中文直角引号「」
    - 中文弯引号“”
    - 英文弯引号 ""
    
    通过数当前字符之前的引号数量判断（奇数=在引号内）。
    """
    prefix = line[:idx]
    for open_q, close_q in [('「', '」'), ('“', '”'), ('"', '"'), ('《', '》')]:
        opens = prefix.count(open_q)
        closes = prefix.count(close_q)
        if opens > closes:
            return True
    return False


def scan_file(path: Path) -> list:
    """扫描单份文件的违规。"""
    issues = []
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # AI 残留检查必须在注释剥离之前运行（它本身匹配 <!-- AI generated --> 标记）
    for pattern in AI_RESIDUE_PATTERNS:
        for line_no, line in enumerate(lines, 1):
            if re.search(pattern, line):
                issues.append((line_no, "AI 残留", pattern, line.strip()))

    LINT_IGNORE_START = "<!-- lint-ignore-start -->"
    LINT_IGNORE_END = "<!-- lint-ignore-end -->"
    in_ignore_block = False
    in_html_comment = False
    
    for line_no, line in enumerate(lines, 1):
        # 处理 lint-ignore 区块：区块内的行全部跳过
        if LINT_IGNORE_START in line:
            in_ignore_block = True
            continue
        if in_ignore_block:
            if LINT_IGNORE_END in line:
                in_ignore_block = False
            continue
        # 处理 HTML 注释块 <!-- ... -->（模板规则说明所在），跳过其中内容
        stripped = line.strip()
        if stripped.startswith("<!--"):
            in_html_comment = True
        if in_html_comment:
            if "-->" in line:
                in_html_comment = False
            continue
        # 破折号：跳过引号内的
        for dash in PROHIBITED_DASHES:
            start = 0
            while True:
                idx = line.find(dash, start)
                if idx == -1:
                    break
                if not is_inside_quotes(line, idx):
                    issues.append((line_no, "禁用破折号", dash, line.strip()))
                start = idx + len(dash)
        
        # 商业黑话：跳过引号内的
        for w in BUSINESS_JARGON:
            start = 0
            while True:
                idx = line.find(w, start)
                if idx == -1:
                    break
                if not is_inside_quotes(line, idx):
                    issues.append((line_no, "商业黑话", w, line.strip()))
                start = idx + len(w)
        
        # 模型路标词：跳过引号内的
        for w in MODEL_BOILERPLATE:
            start = 0
            while True:
                idx = line.find(w, start)
                if idx == -1:
                    break
                if not is_inside_quotes(line, idx):
                    issues.append((line_no, "模型路标词", w, line.strip()))
                start = idx + len(w)
        
        # 借喻词（只警告）：跳过引号内的
        for w in METAPHOR_WORDS:
            start = 0
            while True:
                idx = line.find(w, start)
                if idx == -1:
                    break
                if not is_inside_quotes(line, idx):
                    issues.append((line_no, "借喻词（谨慎）", w, line.strip()))
                start = idx + len(w)
        
        # AI 残留（不在引号内检查）
        for pattern in AI_RESIDUE_PATTERNS:
            if re.search(pattern, line):
                issues.append((line_no, "AI 残留", pattern, line.strip()))
    
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="档案或目录路径")
    parser.add_argument("--min-severity", choices=["warn", "error"], default="warn")
    args = parser.parse_args()
    
    p = Path(args.path)
    
    if p.is_file():
        files = [p]
    elif p.is_dir():
        files = sorted([
            p / f for f in os.listdir(p)
            if f.endswith(".md") and f not in INDEX_FILES
        ])
    else:
        print(f"错误: 路径不存在: {args.path}")
        sys.exit(1)
    
    total_issues = 0
    files_with_issues = 0
    
    for f in files:
        issues = scan_file(f)
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"\n📄 {f.name} ({len(issues)} 个问题):")
            for line_no, category, hit, line in issues:
                print(f"  L{line_no:>4} [{category}] {hit!r}")
                # 只打印片段
                truncated = line[:100] + ("..." if len(line) > 100 else "")
                print(f"       {truncated}")
    
    print(f"\n{'='*60}")
    print(f"扫描文件: {len(files)}")
    print(f"有问题的文件: {files_with_issues}")
    print(f"总问题数: {total_issues}")
    
    sys.exit(1 if total_issues > 0 else 0)


if __name__ == "__main__":
    main()
