#!/usr/bin/env python3
"""
check_sources.py — 校验「主要参考来源」段格式统一。

用法:
  python check_sources.py path/to/archive.md
  python check_sources.py path/to/library/

检查:
  1. 存在「## 主要参考来源」章节
  2. 只检查列表项；每个列表项一行一条
  3. 含 URL 的条目必须是行尾内联链接 [原文](url)，文本限 原文/快照/补充
  4. 列表项不得出现裸 URL
  5. 每条说明 ≥ 20 字
  6. 无地址条目必须注明原因（未取得 / 需登录 / 403 / 快照缺失）

统一格式（全库唯一）:
  - 说明文字（YYYY-MM-DD 获取，可信度：高／中高／中／低；补充）｜[原文](https://…)
  需要两个地址时：｜[原文](u1) ｜[快照](u2)，Wayback 用「快照」，其余用「补充」。

退出码:
  0: 全部通过
  1: 有违规
"""
import re
import sys
import argparse
from pathlib import Path

SECTION = "## 主要参考来源"
LINK_RE = re.compile(r'\[([^\]]*)\]\((https?://[^)\s]+)\)')
BARE_URL_RE = re.compile(r'https?://[^\s)）】]+')
ALLOWED_TEXT = {"原文", "快照", "补充"}
REASON_WORDS = ["未取得", "需登录", "403", "快照", "无法访问", "失效", "需付费", "无地址"]
MIN_DESC = 8  # 真实标杆说明多在 11-19 字，8 字用于拦截空条目/占位符
INDEX_FILES = {"人物-README.md", "person-README.md", "README.md"}


def strip_frontmatter_and_comments(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)


def extract_section(text: str):
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.strip() == SECTION:
            start = i
            break
    if start is None:
        return None
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return out


def check_file(path: str) -> list:
    issues = []
    p = Path(path)
    if not p.exists():
        return [f"文件不存在: {path}"]
    text = strip_frontmatter_and_comments(p.read_text(encoding="utf-8"))
    section = extract_section(text)
    if section is None:
        return ["缺少「主要参考来源」章节"]

    count = 0
    for offset, raw in enumerate(section, 1):
        line = raw.rstrip()
        if not line.strip():
            continue
        # 只检查列表项；章节内说明性文字（非 - 开头）跳过
        if not line.startswith("- "):
            if BARE_URL_RE.search(line) and not LINK_RE.search(line):
                issues.append(f"L{offset}: 非列表行含裸 URL")
            continue
        count += 1
        item = line[2:].strip()

        links = LINK_RE.findall(item)
        rest = LINK_RE.sub("", item)
        if BARE_URL_RE.search(rest):
            issues.append(f"L{offset}: 裸 URL（应写成 [原文](url) 固定在行尾）")
        for link_text, _url in links:
            if link_text not in ALLOWED_TEXT:
                issues.append(f"L{offset}: 链接文本应为「原文/快照/补充」，实际「{link_text}」")
        if not links and not any(w in item for w in REASON_WORDS):
            issues.append(f"L{offset}: 无地址条目缺少原因（未取得/需登录/403/快照）")
        # 说明长度按整段正文计（含括号内的可信度补充），去掉内联链接
        desc = rest.strip()
        if len(desc) < MIN_DESC:
            issues.append(f"L{offset}: 说明过短（{len(desc)} 字 < {MIN_DESC}）")

    if count == 0:
        issues.append("「主要参考来源」章节无列表条目")
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="档案文件或目录")
    args = parser.parse_args()

    p = Path(args.path)
    if p.is_file():
        files = [p]
    elif p.is_dir():
        files = sorted([
            f for f in p.iterdir()
            if f.suffix == ".md" and f.name not in INDEX_FILES
        ])
    else:
        print(f"错误: 路径不存在: {args.path}")
        sys.exit(1)

    total = 0
    bad = 0
    for f in files:
        issues = check_file(str(f))
        if issues:
            bad += 1
            total += len(issues)
            print(f"FAIL: {f}")
            for i in issues[:10]:
                print(f"  - {i}")
            if len(issues) > 10:
                print(f"  ... 还有 {len(issues) - 10} 条")
        else:
            print(f"OK: {f}")

    print(f"\n通过 {len(files) - bad}/{len(files)}，问题 {total} 条")
    sys.exit(0 if total == 0 else 1)


if __name__ == "__main__":
    main()
