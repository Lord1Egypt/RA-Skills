#!/bin/bash
# ============================================
# 码虫日报补课脚本 (Catch-Up Daily Report)
# 基于 Hermes Agent 学习循环思路
#
# 功能：
# 1. 检测漏发的工作日
# 2. 为漏发日生成补录报告
# 3. 更新索引记录
# 4. 记录到 Hermes 反思文件
#
# 注意：此脚本被 exec 预检拦截时，需使用绝对路径调用：
#   python3 /home/colbert/.openclaw/workspace-coding-advisor/skills/daily-report-catchup/catch-up.py
# ============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="/home/colbert/.openclaw/workspace-coding-advisor"

# 调用 Python 版本（更可靠的日期处理）
exec python3 "$SCRIPT_DIR/catch-up.py" "$@"
