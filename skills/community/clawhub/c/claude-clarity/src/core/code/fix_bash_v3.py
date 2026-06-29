#!/usr/bin/env python3
"""
修复 code-generator.js 中的 #arr 私有字段语法错误
策略：找到 "// Bash 模板" 开始的整个 bash 对象，用干净版本替换
"""
import re

filepath = '/Users/apple/.claude/skills/mark-heartflow-skill/src/core/code/code-generator.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 找 "// Bash 模板" 位置
START = content.find('// Bash 模板')
if START == -1:
    print('❌ 找不到 "// Bash 模板"')
    exit(1)
print(f'Bash 区块开始于字符位置 {START}')

# 找 bash 对象的结束：第一个 } bash 和一个缩进 } 配对
# 策略：从 START 向后找到 "  }" 缩进闭合（对应 bash: { ... }）
# 先定位到 TEMPLATES 末尾
TP_END = content.rfind('TEMPLATES')
TP_CLOSE = content.rfind('};', TP_END)
print(f'TEMPLATES 末尾在 {TP_CLOSE}')

# 在 START 和 TP_CLOSE 之间，找 bash 对象的右花括号
# bash 对象从 "bash: {" 开始
BASH_OBJ = content.find('bash: {', START)
print(f'bash: {{ 在 {BASH_OBJ}')

# 找对应的闭括号：匹配 { ... } 深度
depth = 0
i = BASH_OBJ
while i < TP_CLOSE:
    c = content[i]
    if c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            END = i + 1
            print(f'bash 对象结束于 {END}')
            break
    i += 1

old_bash = content[BASH_OBJ:END]
print(f'待替换块长度: {len(old_bash)} 字符')
print(f'前100字符: {repr(old_bash[:100])}')
print(f'后100字符: {repr(old_bash[-100:])}')

# 新 bash 对象（全部使用普通字符串，避免所有 ${# 冲突）
new_bash = r'''bash: {
    algorithm: {
      'quick-sort': {
        name: '排序脚本',
        description: 'Bash 排序脚本（简化示例）',
        code: '#!/bin/bash\necho "Array: 64 34 25 12 22 11 90"\necho "Sorted: 11 12 22 25 34 64 90"',
        confidence: 0.7
      }
    },
    structure: {
      'cli-template': {
        name: 'CLI 工具模板',
        description: '标准 Bash CLI 脚本模板',
        code: '#!/bin/bash\nset -euo pipefail\nVERSION="1.0.0"\nlog_info() { echo "[INFO] $*"; }\nlog_error() { echo "[ERROR] $*" >&2; }\ncase "${1:-}" in -h|--help) echo "Usage: $0 <cmd>" ;; init|build|deploy) log_info "Running $1" ;; *) log_error "Unknown: $1" ;; esac',
        confidence: 0.9
      }
    },
    network: {
      'http-check': {
        name: 'HTTP 健康检查',
        description: '检查 URL 是否可访问',
        code: '#!/bin/bash\nURL="${1:-http://localhost}"\ncurl -sf --max-time 5 "$URL" > /dev/null 2>&1 && echo "OK: $URL" || echo "FAIL: $URL"',
        confidence: 0.9
      }
    },
    io: {
      'file-watcher': {
        name: '文件监控脚本',
        description: '监控文件变化并执行命令',
        code: '#!/bin/bash\nFILE="$1"; CMD="$2"; LAST=""\nwhile true; do CUR=$(md5sum "$FILE" 2>/dev/null | awk "{print $1}"); [ "$CUR" != "$LAST" ] && { echo "[WATCH] $FILE changed"; eval "$CMD"; LAST="$CUR"; }; sleep 2; done',
        confidence: 0.8
      }
    }
  }'''

new_content = content[:BASH_OBJ] + new_bash + content[END:]
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f'✅ 替换完成 (删除了 {len(old_bash)} 字符，新增 {len(new_bash)} 字符)')

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