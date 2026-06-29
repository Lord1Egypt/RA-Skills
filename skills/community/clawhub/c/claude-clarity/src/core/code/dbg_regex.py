#!/usr/bin/env python3
"""修复 code-knowledge.js 中有问题的正则表达式"""

filepath = '/Users/apple/.claude/skills/mark-heartflow-skill/src/core/code/code-knowledge.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 精确替换（Python字符串中的\\s代表正则中的\s）
# 原文本中应该是 \\s+，被某次编辑错误替换了
# 检查当前状态
lines = content.split('\n')
for i in range(1700, 1706):
    if i < len(lines):
        print(f'行 {i+1}: {lines[i][:100]}')

# 直接修复：把 javascript/typescript pattern 中的 s+ 改回 \s+
# 但先确认是否真的是 s+ 而不是 \s+
print()
print('检查 s+ 出现位置:')
for i in range(1700, 1706):
    if i < len(lines) and 'javascript:' in lines[i]:
        print(f'行 {i+1} 包含:', repr(lines[i][50:100]))