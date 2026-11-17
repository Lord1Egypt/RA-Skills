#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
find_blocks.py —— Mermaid 文本陷阱扫描器 / 自动修复器（Python 版）

用途：
    arc4plus1 技能的强制门禁脚本。在阶段 3 写盘前执行 `fix` 自动修复常见陷阱，
    在阶段 4 验证时执行 `check` 做最终静态扫描（exit 0 = 干净 / exit 1 = 有陷阱）。

特性：
    - 纯 Python 3.10+ 实现，仅依赖标准库（re / sys / pathlib / argparse）
    - 中文/全角字符安全（默认 UTF-8）
    - 19 条规则（R1~R19），详见下方"规则总览"
    - 退出码：0=干净 / 1=有陷阱

用法：
    python find_blocks.py check <files...>   # 仅扫描，输出警告，不修改文件
    python find_blocks.py fix   <files...>   # 原地自动修复常见陷阱

规则总览（与 SKILL.md 附录 A.5/A.6/A.7 一一对应）：
    R1.  菱形节点含方括号             [需人工]
    R2.  矩形节点含 ASCII ()          [fix 加引号]
    R3.  subgraph 标签含 ASCII ()     [fix 加引号]
    R4.  矩形节点含 ---               [fix 加引号]
    R5.  矩形节点 label 含未引号 :    [fix 加引号]
    R6.  subgraph ID 后挂括号         [fix 改 ID["label"]]
    R7.  sequenceDiagram 漏 participant [fix 自动补]
    R8.  颜色超 A.3 白名单            [需人工]
    R9.  flowchart 误用序列图语法      [需人工重写]
    R10. (保留)
    R11. (保留)
    R12. 序列图漏写 participant 关键字 [同 R7，向后兼容]
    R13. flowchart 边标签 |..| 裸双引号 [fix 转 &quot;]
    R14. flowchart 关键字误大写       [fix 归一小写]
    R15. flowchart 非法虚线箭头 ..>   [fix 改 -.->]
    R16. flowchart 矩形 label 双重引号 [fix 去重]
    R17. flowchart 矩形 label 嵌套方括号（如 [..[o]..]）[fix 加引号]
    R18. flowchart 矩形 label 非 HTML 尖括号 [fix 转义]
    R19. flowchart 矩形 label 裸双引号 [fix 转 &quot;]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# 块类型常量
# ---------------------------------------------------------------------------
BLOCK_FC = "FC"   # flowchart / graph
BLOCK_SQ = "SQ"   # sequenceDiagram
BLOCK_CL = "CL"   # classDiagram
BLOCK_ST = "ST"   # stateDiagram

# ---------------------------------------------------------------------------
# A.3 颜色白名单（与 SKILL.md 保持同步，大小写不敏感，3 位 hex 自动归一）
# ---------------------------------------------------------------------------
ALLOWED_COLORS_RAW = {
    # 基础 6 色
    "ff0000", "00ff00", "0000ff", "ffff00", "ff00ff", "00ffff",
    # 浅填充 6 色
    "a4c9a0", "e8a26d", "9bbde0", "f9d56e", "bdbdbd", "e69191",
    # 描边 4 色
    "000000", "000", "666666", "999999", "ffffff", "fff",
}


def _normalize_hex(hex_str: str) -> str:
    """3 位 hex → 6 位 hex 归一（#f00 → ff0000），统一小写。"""
    h = hex_str.lower()
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return h


ALLOWED_COLORS = {_normalize_hex(c) for c in ALLOWED_COLORS_RAW}


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------
@dataclass
class MermaidBlock:
    """一个 mermaid 代码块（不含围栏 ``` 本身）。"""

    file: Path
    start_line: int   # ```mermaid 所在行（1-based）
    block_type: str = ""  # FC / SQ / CL / ST
    lines: list[str] = field(default_factory=list)

    @property
    def end_line(self) -> int:
        """块结束（下一个 ```）所在行（1-based，不含围栏行）。"""
        return self.start_line + len(self.lines)


@dataclass
class Issue:
    """一条扫描命中（warning）。"""

    rule: str
    file: Path
    lineno: int
    snippet: str

    def format(self) -> str:
        s = self.snippet.strip()
        if len(s) > 120:
            s = s[:117] + "..."
        return f"  ⚠️ {self.rule}：{self.file}:{self.lineno}:{s}"


# ---------------------------------------------------------------------------
# 块解析：抽取 ```mermaid ... ``` 区间，标记块类型
# ---------------------------------------------------------------------------
_FENCE_OPEN = re.compile(r"^```mermaid\s*$")
_FENCE_CLOSE = re.compile(r"^```\s*$")
_BLOCK_HEADER = [
    (BLOCK_FC, re.compile(r"^[ \t]*(?:flowchart|graph)(?:[ \t].*)?$")),
    (BLOCK_SQ, re.compile(r"^[ \t]*sequenceDiagram(?:[ \t].*)?$")),
    (BLOCK_CL, re.compile(r"^[ \t]*classDiagram(?:[ \t].*)?$")),
    (BLOCK_ST, re.compile(r"^[ \t]*stateDiagram.*$")),
]


def parse_blocks(file: Path) -> list[MermaidBlock]:
    """读取整个 .md 文件，返回所有 mermaid 代码块。"""
    blocks: list[MermaidBlock] = []
    in_block = False
    current: MermaidBlock | None = None

    try:
        text = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # 兼容 GBK 等编码
        text = file.read_text(encoding="gbk", errors="replace")

    for i, line in enumerate(text.splitlines(), start=1):
        if not in_block:
            if _FENCE_OPEN.match(line):
                in_block = True
                current = MermaidBlock(file=file, start_line=i)
        else:
            if _FENCE_CLOSE.match(line):
                in_block = False
                if current is not None:
                    blocks.append(current)
                    current = None
            elif current is not None:
                if not current.block_type:
                    for bt, pat in _BLOCK_HEADER:
                        if pat.match(line):
                            current.block_type = bt
                            break
                current.lines.append(line)

    return blocks


# ---------------------------------------------------------------------------
# 修复规则（fix 模式）
# ---------------------------------------------------------------------------
# 规则 1: 矩形节点含 ASCII () → 加引号包裹（允许缩进 + 箭头前缀，排除 subgraph 行）
# v1.1.1 改进：允许节点出现在 "--> " 等箭头行中段（不仅是行首）
_R_RECT_PAREN = re.compile(
    r'^([ \t]*(?:\w+(?:\[[^\]]*\])?\s+(?:-->|-.->|==>|---)\s+)?)(?!subgraph\b)(\w+)\[(?!")([^\[\]]*\([^\)]*\)[^\[\]]*)\]'
)
# 规则 2: 矩形节点含 --- → 加引号包裹（排除 subgraph 行）
_R_RECT_DASHES = re.compile(
    r'^([ \t]*)(?!subgraph\b)(\w+)\[(?!")([^\[\]]*---[^\[\]]*)\]'
)
# 规则 3: subgraph 标签含 ASCII () → 加引号包裹
_R_SUBGRAPH_PAREN = re.compile(
    r'^([ \t]*)(subgraph\s+\w+)\[(?!")([^\[\]]*\([^\)]*\)[^\[\]]*)\]'
)
# 规则 5: 矩形节点 label 含未引号 : → 整段加引号
_R_RECT_COLON = re.compile(
    r'^([ \t]*)(?!subgraph\b)(\w+)\[(?!")([^\[\]"]*:[^\[\]"]*)\]'
)
# 规则 6: subgraph ID 后挂括号（ASCII / 全角）
_R_SUBGRAPH_BRACKETED = re.compile(
    r"^([ \t]*subgraph\s+)([^()（）\[\]\s]+)([ \t]*)([（(][^()\]\[\"）\n]*[）)])"
)


def _wrap_label(m: re.Match, indent: str, ident: str, raw_label: str) -> str:
    """把已经匹配出的 label 内容用双引号包裹，构造 ID["..."]。"""
    return f'{indent}{ident}["{raw_label}"]'


def _fix_line_in_fc(line: str, block: MermaidBlock) -> str:
    """对 flowchart 块内的单行应用所有 fix 规则。返回（可能）已修复的行。"""
    # 规则 A (R14): flowchart 语句关键字被误大写 → 归一为小写
    for kw in ("STYLE", "LINKSTYLE", "CLASSDEF", "SUBGRAPH"):
        line = re.sub(rf"^([ \t]*){kw}\b", lambda m: f"{m.group(1)}{kw.lower()}", line)

    # 规则 B (R15): flowchart 内非法虚线箭头 "..>" → "-.->"
    line = re.sub(r"\s\.\.>\s", " -.-> ", line)

    # 规则 4: 仅 flowchart 块内把 "A --> B: text" 改写为 "A -->|text| B"
    # （允许节点带 [label]）
    line = re.sub(
        r"^([ \t]*)(\w+(?:\[[^\]]*\])?)\s+(-->|-.->|==>|---)\s+(\w+(?:\[[^\]]*\])?)\s*:\s+(.+?)(\s*)$",
        lambda m: f"{m.group(1)}{m.group(2)} {m.group(3)}|{m.group(5)}| {m.group(4)}{m.group(6)}",
        line,
    )

    # 规则 8 (R13): flowchart 边标签 |...| 内含裸双引号 → 转义为 &quot;
    def _escape_quotes_in_pipe(m: re.Match) -> str:
        inner = m.group(2).replace('"', "&quot;")
        return f"{m.group(1)}{inner}{m.group(3)}"
    line = re.sub(r"(\|)([^|\n]*)(\|)", _escape_quotes_in_pipe, line)

    # 规则 C (R16): 矩形 label 双重双引号 [""]x[""] → ["x"]
    line = re.sub(r'\[""([^"\]]*)""\]', r'["\1"]', line)

    # 规则 D (R17): 矩形 label 嵌套括号 [...] → 整段加引号
    # v1.1.1 改进：
    #   - 允许节点出现在箭头行中段（如 "INCLUDE --> H2[xxx]"）
    #   - 检测任意嵌套 []（不仅限于空括号），例如 OBJS[*.[o]]
    line = re.sub(
        r'^([ \t]*(?:\w+(?:\[[^\]]*\])?\s+(?:-->|-.->|==>|---)\s+)?)(\w+)\[(?!")([^\[\]]*\[[^\]]*\][^\]]*)\]',
        lambda m: f'{m.group(1)}{m.group(2)}["{m.group(3)}"]',
        line,
    )

    # 规则 E (R18): 矩形 label 含非 HTML 尖括号（含 "."，如 <stdbool.h>）→ 转义
    line = re.sub(r"<([^<>]*\.[^<>]*)>", r"&lt;\1&gt;", line)

    # 规则 F (R19): 矩形 label 含裸双引号 → 转义为 &quot;
    def _escape_inner_quotes(m: re.Match) -> str:
        label = m.group(3).replace('"', "&quot;")
        return f"{m.group(1)}{m.group(2)}[{label}]"
    line = re.sub(
        r'^([ \t]*)(\w+)\[(?!")([^\]]*"[^\]]*)\]',
        _escape_inner_quotes,
        line,
    )

    return line


def _fix_line_global(line: str) -> str:
    """对所有块都生效的规则。

    注意：每个 regex 用 3 个捕获组 —— (indent, ident, label)，再用 group(3)
    精确取出 label 文本，避免 group(0)（包含 indent 和 ident）导致重复拼接。
    """

    # 规则 1: 矩形节点含 ASCII () → 加引号包裹
    def _r1(m: re.Match) -> str:
        return f'{m.group(1)}{m.group(2)}["{m.group(3)}"]'
    line = _R_RECT_PAREN.sub(_r1, line)

    # 规则 2: 矩形节点含 --- → 加引号包裹
    line = _R_RECT_DASHES.sub(lambda m: f'{m.group(1)}{m.group(2)}["{m.group(3)}"]', line)

    # 规则 3: subgraph 标签含 ASCII () → 加引号包裹
    line = _R_SUBGRAPH_PAREN.sub(lambda m: f'{m.group(1)}{m.group(2)}["{m.group(3)}"]', line)

    # 规则 5: 矩形节点 label 含未引号 : → 整段加引号
    line = _R_RECT_COLON.sub(lambda m: f'{m.group(1)}{m.group(2)}["{m.group(3)}"]', line)

    return line


def _fix_line_in_subgraph(line: str) -> str:
    """规则 6: subgraph ID 后挂括号。"""
    def _r6(m: re.Match) -> str:
        return f'{m.group(1)}{m.group(2)}["{m.group(4)}"]'
    return _R_SUBGRAPH_BRACKETED.sub(_r6, line)


def _fix_line_in_sq(line: str) -> str:
    """规则 7 / R12: 序列图漏写 participant 关键字。"""
    # 合法形式: participant X / participant X as "Label"  跳过
    if re.match(r"^[ \t]*\bparticipant\b", line):
        return line
    return re.sub(
        r"^([ \t]*)((?!\bparticipant\b)\w+\s+as\b.*)$",
        lambda m: f"{m.group(1)}participant {m.group(2)}",
        line,
    )


def fix_blocks(file: Path) -> bool:
    """对单个文件应用所有可自动修复的规则。

    返回 True 表示文件被修改，False 表示未修改。
    """
    blocks = parse_blocks(file)
    if not blocks:
        return False

    # 把整个文件读成 lines（保留围栏）
    try:
        all_lines = file.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        all_lines = file.read_text(encoding="gbk", errors="replace").splitlines()

    modified = False
    block_iter = iter(blocks)
    current_block = next(block_iter, None)
    in_block = False

    for i, line in enumerate(all_lines):
        if not in_block:
            if _FENCE_OPEN.match(line):
                in_block = True
        else:
            if _FENCE_CLOSE.match(line):
                in_block = False
                current_block = next(block_iter, None)
            elif current_block is not None:
                new_line = line
                if current_block.block_type == BLOCK_FC:
                    new_line = _fix_line_in_fc(line, current_block)
                    new_line = _fix_line_in_subgraph(new_line)
                elif current_block.block_type == BLOCK_SQ:
                    new_line = _fix_line_in_sq(line)
                # 全局规则
                new_line = _fix_line_global(new_line)
                if new_line != line:
                    all_lines[i] = new_line
                    modified = True

    if modified:
        file.write_text("\n".join(all_lines) + "\n", encoding="utf-8")
    return modified


# ---------------------------------------------------------------------------
# 扫描规则（check 模式）
# ---------------------------------------------------------------------------
def scan_blocks(blocks: list[MermaidBlock]) -> list[Issue]:
    """对所有 mermaid 块执行 19 条扫描规则，返回 Issue 列表。"""
    issues: list[Issue] = []

    # 全局规则（所有块都查）
    _GLOBAL_RULES = [
        ("R1 菱形节点含方括号",
         re.compile(r"\{[^{}]*\[[^\]]*\][^{}]*\}"),
         None),
        ("R2 矩形节点含 ASCII ()",
         # v1.1.1 改进：允许节点出现在 "INCLUDE --> H2[xxx]" 等箭头行中段
         re.compile(r"^[ \t]*(?:\w+(?:\[[^\]]*\])?\s+(?:-->|-.->|==>|---)\s+)?(?!subgraph\b)\w+\s*\[(?!\")[^\]]*\([^\)]*\)[^\]]*\]"),
         None),
        ("R3 subgraph 标签含 ASCII ()",
         re.compile(r"subgraph\s+\w+\s*\[(?!\")[^\]]*\([^\)]*\)[^\]]*\]"),
         None),
        ("R4 矩形节点含 ---",
         re.compile(r"^[ \t]*(?!subgraph\b)\w+\s*\[(?!\")[^\]]*---[^\]]*\]"),
         None),
        ("R5 矩形节点 label 含未引号的 :",
         re.compile(r"^[ \t]*(?!subgraph\b)\w+\s*\[(?!\")[^\[\]\"]*:[^\[\]\"]*\]"),
         None),
        ("R6 subgraph ID 后挂括号",
         re.compile(r"^[ \t]*subgraph\s+[^()（）\[\]\s]+[ \t]*[（(][^()\]\[\"）\n]*[）)]"),
         None),
        ("R5b 节点/participant ID 含 . 或 -",
         re.compile(r"^[ \t]*(?:participant\s+)?(\w[\w]*[\.\-][\w\.\-]*)\s*[\[(]"),
         None),
        ("R6b 节点方括号跨行未闭合",
         re.compile(r"^[ \t]*\w+\s*\[(?:[^\]\n]*)$"),
         None),
        ("R7 可疑 <br> 标签位置（行首孤立 / 紧跟 ]）",
         re.compile(r"(?:^[ \t]*<br\b)|(?<=\])[ \t]*<\w+"),
         None),
    ]

    # 仅 flowchart / 序列图块专用规则
    _R9_RE = re.compile(
        r"^[ \t]*\w+(?:\[[^\]]*\])?\s+(?:-->|-.->|==>|---)\s+\w+(?:\[[^\]]*\])?\s*:\s+\S"
    )
    _R12_RE = re.compile(r"^[ \t]*(?!\bparticipant\b)\w+\s+as\s+\S")
    _R13_RE = re.compile(r"\|[^|\n]*\"[^|\n]*\|")
    _R14_RE = re.compile(r"^[ \t]*(?:STYLE|LINKSTYLE|CLASSDEF|SUBGRAPH)\b")
    _R15_RE = re.compile(r"(?:\s|^)\.\.>(?:\s|$)")
    _R16_RE = re.compile(r'\[""[^"\]]*""\]')
    _R17_RE = re.compile(r'^[ \t]*(?:\w+(?:\[[^\]]*\])?\s+(?:-->|-.->|==>|---)\s+)?\w+\[(?!")[^\[\]]*\[[^\]]*\][^\]]*\]')
    _R18_RE = re.compile(r'\[[^\]]*<[^<>]*\.[^<>]*>[^\]]*\]')
    _R19_RE = re.compile(r'^[ \t]*\w+\[(?!")[^\]]*"[^\]]*\]')

    _COLOR_RE = re.compile(r'(?:fill|stroke)\s*:\s*#([0-9a-fA-F]{3,6})\b')

    for blk in blocks:
        for raw_idx, raw_line in enumerate(blk.lines):
            lineno = blk.start_line + 1 + raw_idx
            bt = blk.block_type

            # R8: 颜色超 A.3 白名单
            for m in _COLOR_RE.finditer(raw_line):
                hex_str = m.group(1)
                if _normalize_hex(hex_str) not in ALLOWED_COLORS:
                    issues.append(Issue(
                        rule=f"R8 颜色超 A.3 白名单（#{hex_str}）",
                        file=blk.file, lineno=lineno, snippet=raw_line,
                    ))

            # R9: flowchart 块内误用序列图语法
            if bt == BLOCK_FC and _R9_RE.search(raw_line):
                issues.append(Issue(
                    rule="R9 flowchart 块内误用序列图语法（应改为 A -->|text| B）",
                    file=blk.file, lineno=lineno, snippet=raw_line,
                ))

            # R12: 序列图漏写 participant 关键字
            if bt == BLOCK_SQ and _R12_RE.search(raw_line):
                issues.append(Issue(
                    rule="R12 序列图漏写 participant 关键字",
                    file=blk.file, lineno=lineno, snippet=raw_line,
                ))

            # R13: flowchart 边标签内含裸双引号
            if bt == BLOCK_FC and _R13_RE.search(raw_line):
                issues.append(Issue(
                    rule="R13 flowchart 边标签 |..| 内含裸双引号（应转义为 &quot;）",
                    file=blk.file, lineno=lineno, snippet=raw_line,
                ))

            # R14-R19: flowchart 块专用
            if bt == BLOCK_FC:
                if _R14_RE.search(raw_line):
                    issues.append(Issue(
                        rule="R14 flowchart 关键字误大写（应小写，如 style/subgraph）",
                        file=blk.file, lineno=lineno, snippet=raw_line,
                    ))
                if _R15_RE.search(raw_line):
                    issues.append(Issue(
                        rule="R15 flowchart 非法虚线箭头 ..>（应改为 -.->）",
                        file=blk.file, lineno=lineno, snippet=raw_line,
                    ))
                if _R16_RE.search(raw_line):
                    issues.append(Issue(
                        rule='R16 flowchart 矩形 label 双重双引号 [""]（应改为 [""]）',
                        file=blk.file, lineno=lineno, snippet=raw_line,
                    ))
                if _R17_RE.search(raw_line):
                    issues.append(Issue(
                        rule="R17 flowchart 矩形 label 含嵌套空括号 []（应整段加引号）",
                        file=blk.file, lineno=lineno, snippet=raw_line,
                    ))
                if _R18_RE.search(raw_line):
                    issues.append(Issue(
                        rule="R18 flowchart 矩形 label 含非 HTML 尖括号（应转义 &lt; &gt;）",
                        file=blk.file, lineno=lineno, snippet=raw_line,
                    ))
                if _R19_RE.search(raw_line):
                    issues.append(Issue(
                        rule='R19 flowchart 矩形 label 含裸双引号（应转义为 &quot;）',
                        file=blk.file, lineno=lineno, snippet=raw_line,
                    ))

            # 全局规则
            for name, pat, _ in _GLOBAL_RULES:
                if pat.search(raw_line):
                    issues.append(Issue(
                        rule=name, file=blk.file, lineno=lineno, snippet=raw_line,
                    ))

    return issues


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="find_blocks.py",
        description="Mermaid 文本陷阱扫描器 / 自动修复器（Python 版）",
        epilog="退出码：0 = 干净 / 1 = 有陷阱",
    )
    parser.add_argument(
        "mode", choices=("check", "fix"),
        help="check: 仅扫描报告，不修改文件；fix: 原地自动修复常见陷阱",
    )
    parser.add_argument(
        "files", nargs="+", type=Path,
        help="待处理的 .md 文件列表",
    )
    args = parser.parse_args(argv)

    total_modified = 0
    total_issues = 0

    for file in args.files:
        if not file.exists():
            print(f"❌ 文件不存在：{file}", file=sys.stderr)
            total_issues += 1
            continue
        if not file.is_file():
            print(f"❌ 不是文件：{file}", file=sys.stderr)
            total_issues += 1
            continue

        if args.mode == "fix":
            modified = fix_blocks(file)
            if modified:
                total_modified += 1
                print(f"🔧 已修复：{file}")
        else:  # check
            blocks = parse_blocks(file)
            issues = scan_blocks(blocks)
            if issues:
                print(f"\n📄 {file}：发现 {len(issues)} 条陷阱")
                for iss in issues:
                    print(iss.format())
                total_issues += len(issues)

    # 兜底门禁：fix 后必须再做一次 check 确认
    if args.mode == "fix":
        # 重新扫描以确认 fix 真的把所有可修项都修掉了
        print("\n--- fix 后复扫 ---")
        remaining = 0
        for file in args.files:
            blocks = parse_blocks(file)
            issues = scan_blocks(blocks)
            if issues:
                remaining += len(issues)
                print(f"\n📄 {file}：仍有 {len(issues)} 条无法自动修复的陷阱")
                for iss in issues:
                    print(iss.format())
        if remaining:
            print(f"\n❌ fix 模式完成，但仍有 {remaining} 条陷阱（必须人工介入）")
            return 1
        if total_modified:
            print(f"\n✅ fix 模式成功，修复了 {total_modified} 个文件，0 残留陷阱")
        else:
            print("\n✅ fix 模式完成，0 个文件需要修改")
        return 0

    # check 模式收尾
    if total_issues:
        print(f"\n❌ 共发现 {total_issues} 条陷阱（必须修复后再宣告完成）")
        return 1
    print("\n✅ 所有文件干净，无陷阱")
    return 0


if __name__ == "__main__":
    sys.exit(main())