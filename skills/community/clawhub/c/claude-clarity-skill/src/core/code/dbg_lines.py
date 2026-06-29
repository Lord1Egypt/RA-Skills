#!/usr/bin/env python3
"""修复 code-generator.js 中的 #arr 语法错误"""

filepath = '/Users/apple/.claude/skills/mark-heartflow-skill/src/core/code/code-generator.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 找第989-991行附近的内容
lines = content.split('\n')
for i, line in enumerate(lines):
    if '排序后' in line:
        print(f'行 {i+1}: {repr(line)}')
        print(f'行 {i+2}: {repr(lines[i+1] if i+1 < len(lines) else "N/A")}')
        print(f'行 {i+3}: {repr(lines[i+2] if i+2 < len(lines) else "N/A")}')
        # 找这个模板块的开始
        for j in range(i, max(0, i-50), -1):
            if "code: `" in lines[j]:
                print(f'模板开始于行 {j+1}: {repr(lines[j])}')
                break
        break

# 直接替换行 989-991（从 ` 开头到 ` 结尾）
# 把 ``..${#arr[@]}..`` 改成普通的 "" 字符串
new_lines = []
skip_until_end = False
i = 0
while i < len(lines):
    line = lines[i]
    if 'sorted=($(quick_sort "${arr[@]}"))' in line and lines[i-1].strip() == '`':
        # 这是模板字符串的结束行，但我们需要把整个模板变成普通字符串
        # 找到模板开始行（行 i-1 是结束 `，行 i-2 是内容，行 i-3 是内容...）
        # 实际上，因为这个模板跨越多行，最简单的方案是：
        # 把整段从 'code: `' 到这个 '`,' 之间的内容替换
        print(f'发现结束行 {i+1}: {repr(line)}')
        print(f'前一行 {i}: {repr(lines[i-1])}')
        i += 1
        continue
    new_lines.append(line)
    i += 1

# 更简单：直接替换那几行的内容
# 行 989: `echo "原数组: ${arr[@]}"
# 行 990: sorted=($(quick_sort "${arr[@]}"))
# 行 991: echo "排序后: ${sorted[@]}"`,
# 行 954-955: const HASH = '#'; const CODE_BASH_QS = `#!/bin/bash
# 行 960: n=${#arr[@]}  # 这是有问题的行

# 找到包含 ${#arr 的行并修复
for i in range(len(new_lines)):
    if '${#arr[@]}' in new_lines[i]:
        print(f'行 {i+1} 包含 ${#arr}: {repr(new_lines[i])}')

print(f'总行数: {len(new_lines)}')