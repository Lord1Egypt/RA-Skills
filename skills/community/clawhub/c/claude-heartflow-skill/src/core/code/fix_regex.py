#!/usr/bin/env python3
"""修复 code-knowledge.js 中有问题的正则表达式"""

import subprocess

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

# 验证（仅语法检查，不执行代码）
result = subprocess.run(['node', '--check', filepath],
    capture_output=True, text=True)
if result.returncode == 0:
    print('✅ 语法检查通过')
else:
    print('❌ 语法错误:', result.stderr[:300])