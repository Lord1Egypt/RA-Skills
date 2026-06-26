#!/usr/bin/env python3
"""
ANSI 颜色码剥离工具

读取 stdin，移除 ANSI 转义序列后输出
用于 cron 任务中将带颜色的脚本输出转为纯文本

用法：
  python3 rebalance.py | python3 strip_color.py
  python3 recommend.py  | python3 strip_color.py
"""
import sys
import re

ANSI_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')

for line in sys.stdin:
    sys.stdout.write(ANSI_RE.sub('', line))
