#!/usr/bin/env python3
"""修复 code-knowledge.js 中有问题的正则表达式（纯文件操作，无进程调用）"""

import os

filepath = '/Users/apple/.claude/skills/mark-heartflow-skill/src/core/code/code-knowledge.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换有问题的 patterns 对象
old_patterns = '''const patterns = {
      javascript: /(?:async\\s+)?(?:function\\s+(\\w+)|(\\w+)\\s*\\(|const\\s+(\\w+)\\s*=\\s*(?:async\\s+)?\\(|(\\w+)\\s*:\\s*(?:async\\s+)?\\([^)]*\\)\\s*=>/g,
      typescript: /(?:async\\s+)?(?:function\\s+(\\w+)|(\\w+)\\s*\\(|const\\s+(\\w+)\\s*=\\s*(?:async\\s+)?\\(|(\\w+)\\s*:\\s*(?:async\\s+)?\\([^)]*\\)\\s*=>)/g,'''

new_patterns = '''const patterns = {
      javascript: /(?:async\\s+)?(?:function\\s+(\\w+)|([\\w$]+)\\s*\\(|const\\s+([\\w$]+)\\s*=\\s*(?:async\\s+)?\\(|([\\w$]+)\\s*:\\s*(?:async\\s+)?\\([^)]*\\)\\s*=>/g,
      typescript: /(?:async\\s+)?(?:function\\s+(\\w+)|([\\w$]+)\\s*\\(|const\\s+([\\w$]+)\\s*=\\s*(?:async\\s+)?\\(|([\\w$]+)\\s*:\\s*(?:async\\s+)?\\([^)]*\\)\\s*=>)/g,'''

if old_patterns in content:
    new_content = content.replace(old_patterns, new_patterns)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('✅ 替换成功')
else:
    print('❌ 未找到匹配')

    # 尝试直接替换第1702-1703行
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if i in (1701, 1702) and 'javascript:' in line:
            print(f'行 {i+1}: {repr(line)}')

# 验证（极简结构检查，不调用外部进程）
def _quick_js_check(fp):
    """纯 Python JS 结构校验：匹配大括号数"""
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            c = f.read()
        depth = 0
        for ch in c:
            if ch == '{': depth += 1
            if ch == '}': depth -= 1
            if depth < 0:
                print('⚠️  可能的 JS 语法问题：多余的闭合大括号')
                return False
        if depth > 0:
            print('⚠️  可能的 JS 语法问题：缺少闭合大括号')
            return False
        print('✅ 基本结构检查通过')
        return True
    except Exception as e:
        print(f'⚠️  无法读取文件: {e}')
        return False

_quick_js_check(filepath)