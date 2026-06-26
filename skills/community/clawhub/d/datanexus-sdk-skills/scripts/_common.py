# -*- coding: utf-8 -*-
"""
_common.py — 能力7/8 脚本的公共工具

设计原则：
  - 仅放**真正被 2 个及以上脚本共用**的逻辑，避免过度抽象
  - 保持纯标准库，不引入第三方依赖
  - 以"小工具"粒度提供，不做配置/框架化

当前抽取的内容：
  - _strip_line_comment: 粗粒度剔除 // 和 /* ... */ 注释
"""
from __future__ import annotations

import re


def strip_line_comment(line: str) -> str:
    """
    粗粒度剔除单行注释，仅适用于 // 风格 + 同一行内的 /* ... */
    覆盖语言：JS / TS / Java / Kotlin / Swift / ObjC / ArkTS

    保守策略：若 // 出现在字符串字面量（单/双/反引号）里则不剔除，
    避免把 "https://api.xxx.com" 这种 URL 当注释截断。

    限制：
      - 不处理跨行 /* ... */（只剔除同一行内闭合的）
      - 不识别 Python # 风格（本 SDK 场景不涉及 Python 源码扫描）
      - 不识别 Shell # 风格（同上）

    返回：剔除注释后的行内容；若整行都是注释则返回空串。
    """
    # 先处理同一行闭合的 /* ... */
    line = re.sub(r"/\*.*?\*/", "", line)

    # 扫描 // 注释起点，但要跳过字符串字面量里的 //
    in_single = False       # '...'
    in_double = False       # "..."
    in_backtick = False     # `...` (JS/TS template literal)
    i = 0
    n = len(line)
    while i < n - 1:
        ch = line[i]
        # 转义字符
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif ch == "`" and not in_single and not in_double:
            in_backtick = not in_backtick
        elif ch == "/" and line[i + 1] == "/" and not (in_single or in_double or in_backtick):
            return line[:i]
        i += 1
    return line
