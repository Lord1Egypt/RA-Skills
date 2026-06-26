#!/usr/bin/env python3
"""修复 code-generator.js 中的 #arr 语法错误（私有字段冲突）"""

import re

filepath = '/Users/apple/.claude/skills/mark-heartflow-skill/src/core/code/code-generator.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 bash quick-sort 模板块（从 'code: `' 到下一个 `,）
# 替换为普通字符串（不用模板字符串，避免 # 解析问题）
old_pattern = r"(code: )`#!/bin/bash.*?`,\s+confidence: 0\.7"

replacement = r'''code: "#!/bin/bash\n# 快速排序实现（Bash版）\n# 使用数组和递归实现\n\narr=(64 34 25 12 22 11 90)\nn=${#arr[@]}\n\nquick_sort() {\n    local arr=(\"$@\")\n    local low=${arr[0]}\n    local high=${arr[-1]}\n\n    if [ \"$low\" -lt \"$high\" ]; then\n        pivot=${arr[$high]}\n        i=$((low - 1))\n\n        for ((j=low; j<high; j++)); do\n            if [ \"${arr[$j]}\" -le \"$pivot\" ]; then\n                ((i++))\n                tmp=${arr[$i]}\n                arr[$i]=${arr[$j]}\n                arr[$j]=$tmp\n            fi\n        done\n\n        tmp=${arr[$((i+1))]}\n        arr[$((i+1))]=${arr[$high]}\n        arr[$high]=$tmp\n\n        pivot_index=$((i+1))\n        echo \"${arr[@]}\"\n    fi\n}\n\necho \"原数组: ${arr[@]}\"\nsorted=($(quick_sort \"${arr[@]}\"))\necho \"排序后: ${sorted[@]}\",'''

new_content = re.sub(old_pattern, replacement, content, flags=re.DOTALL)

if new_content == content:
    print('❌ 未找到匹配的模式')
else:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('✅ 修复成功')

    # 验证（仅语法检查，不执行代码）
    try:
        import subprocess
        result = subprocess.run(['node', '--check', filepath],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print('✅ 语法检查通过')
        else:
            print('❌ 语法错误:', result.stderr[:200])
    except:
        print('⚠️  无法验证语法')