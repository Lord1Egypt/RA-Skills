#!/bin/bash
# sycophancy-transform.sh
# UserPromptSubmit hook: 将确认式句式自动转换为开放性问题
# 遵循 "Ask Don't Tell" 原则 (ArXiv 2602.23971)
#
# 输入: JSON {"originalUserPromptText": "..."} (通过 stdin)
# 输出: 转换后的纯文本 prompt
# 退出码 0: stdout 传给 Claude; 2: 阻止处理并显示 stderr

HOOK_DIR="$(dirname "$0")"
exec python3 "$HOOK_DIR/sycophancy-transform.py"
