#!/usr/bin/env python3
"""修复 code-generator.js 中的 #arr 语法错误"""
# 注意：此脚本为一次性开发工具，非运行时模块

import re
import subprocess

filepath = '/Users/apple/.claude/skills/mark-heartflow-skill/src/core/code/code-generator.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 精确查找包含 #arr 的模板字符串位置
match = re.search(r'code: `#!/bin/bash', content)
if not match:
    print('❌ 未找到 code: `#!/bin/bash')
else:
    start = match.start()
    # 找到结束：反向找 'code: `' 然后向前找逗号+换行+confidence
    # 在 start 附近，code: 后面是模板字符串，结束是 `, 后面紧跟 confidence
    end_match = re.search(r'`,\s+confidence: 0\.7', content[start:])
    if end_match:
        end = start + end_match.end()
        old_block = content[start:end]
        print(f'找到块，从 {start} 到 {end}，长度 {len(old_block)}')
        print('前80字符:', repr(old_block[:80]))
        print('后80字符:', repr(old_block[-80:]))

        # 替换为普通双引号字符串（不触发 #arr 解析）
        new_code = (
            'code: "#!/bin/bash\\n'
            '# 快速排序实现（Bash版）\\n'
            '# 使用数组和递归实现\\n\\n'
            'arr=(64 34 25 12 22 11 90)\\n'
            'n=${#arr[@]}\\n\\n'
            'quick_sort() {\\n'
            '    local arr=(\\"$@\\")\\n'
            '    local low=${arr[0]}\\n'
            '    local high=${arr[-1]}\\n\\n'
            '    if [ \\"$low\\" -lt \\"$high\\" ]; then\\n'
            '        pivot=${arr[$high]}\\n'
            '        i=$((low - 1))\\n\\n'
            '        for ((j=low; j<high; j++)); do\\n'
            '            if [ \\"${arr[$j]}\\" -le \\"$pivot\\" ]; then\\n'
            '                ((i++))\\n'
            '                tmp=${arr[$i]}\\n'
            '                arr[$i]=${arr[$j]}\\n'
            '                arr[$j]=$tmp\\n'
            '            fi\\n'
            '        done\\n\\n'
            '        tmp=${arr[$((i+1))]}\\n'
            '        arr[$((i+1))]=${arr[$high]}\\n'
            '        arr[$high]=$tmp\\n\\n'
            '        pivot_index=$((i+1))\\n'
            '        echo \\"${arr[@]}\\"\\n'
            '    fi\\n'
            '}\\n\\n'
            'echo \\"原数组: ${arr[@]}\\"\\n'
            'sorted=($(quick_sort \\"${arr[@]}\\"))\\n'
            'echo \\"排序后: ${sorted[@]}\\"'
            '",'
        )
        new_content = content[:start] + new_code + content[end:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('✅ 修复成功')

        # 验证（仅语法检查，不执行代码）
        result = subprocess.run(['node', '--check', filepath],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print('✅ 语法检查通过')
        else:
            print('❌ 语法错误:', result.stderr[:300])
    else:
        print('❌ 未找到结束标记')