#!/bin/bash
#
# OpenClaw 命令自动记录包装器
#
# 使用方法：
# 1. 在 OpenClaw 配置中启用此包装器
# 2. 或在执行命令前通过此脚本
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_DB="$HOME/.openclaw/audit.db"

# 记录命令执行
log_command() {
    local tool_name="$1"
    local action="$2"
    local command="$3"
    local start_time=$(date +%s%3N)

    # 检查权限
    local check_result=$(python3 - <<EOF
import sqlite3
import fnmatch

conn = sqlite3.connect("$AUDIT_DB")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM permission_rules ORDER BY priority DESC")
rules = cursor.fetchall()

for rule in rules:
    tool_match = fnmatch.fnmatch("$tool_name", rule["tool_pattern"])
    action_match = fnmatch.fnmatch("$action", rule["action_pattern"])

    if tool_match and action_match:
        print(f"{rule['allowed']}|{rule['rule_name']}")
        break
else:
    print("true|default")

conn.close()
EOF
)

    local allowed=$(echo "$check_result" | cut -d'|' -f1)
    local rule_name=$(echo "$check_result" | cut -d'|' -f2)

    if [ "$allowed" != "True" ]; then
        echo "❌ 权限被拒绝: $rule_name"
        return 1
    fi

    # 执行命令
    eval "$command"
    local exit_code=$?

    # 计算耗时
    local end_time=$(date +%s%3N)
    local duration=$((end_time - start_time))

    # 记录到数据库
    python3 - <<EOF
import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect("$AUDIT_DB")
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO operations
    (tool_name, action, parameters, result, success, duration_ms, user, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "$tool_name",
    "$action",
    json.dumps({"command": "$command"}),
    "exit_code: $exit_code",
    $exit_code == 0,
    $duration,
    "$USER",
    datetime.now().isoformat()
))

conn.commit()
conn.close()
EOF

    return $exit_code
}

# 如果直接运行此脚本
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    if [ $# -lt 1 ]; then
        echo "使用方法: $0 <command>"
        echo "示例: $0 'rm -rf ~/Desktop/截图'"
        exit 1
    fi

    log_command "exec" "run_command" "$*"
fi
