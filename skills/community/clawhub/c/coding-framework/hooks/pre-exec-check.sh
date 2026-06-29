#!/bin/bash
# pre-exec-check.sh — 执行前安全检查
# 从 stdin 读取 JSON 事件数据，评估安全规则，输出决策结果
# 集成 25 种安全模式 + 基础安全规则

set -euo pipefail

# 读取 stdin 事件数据
EVENT_DATA=$(cat)

# 提取命令字段（兼容 jq 和纯 bash）
if command -v jq &>/dev/null; then
    COMMAND=$(echo "$EVENT_DATA" | jq -r '.command // ""')
    WORKDIR=$(echo "$EVENT_DATA" | jq -r '.workdir // ""')
else
    COMMAND=$(echo "$EVENT_DATA" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
    WORKDIR=$(echo "$EVENT_DATA" | grep -o '"workdir"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")
RULES_DIR="$(dirname "$0")/../rules"
MATCHED_RULES=()
DECISION="allow"
MESSAGE=""

# ─── 加载 security-rules.md 中的规则 ─────────────────────────────────────
if [[ -f "$RULES_DIR/security-rules.md" ]]; then
    IN_FRONTMATTER=false
    CURRENT_MATCHER=""
    CURRENT_ACTION=""
    CURRENT_NAME=""
    CURRENT_ENABLED=""

    while IFS= read -r line; do
        if [[ "$line" == "---" ]]; then
            if $IN_FRONTMATTER; then
                if [[ "$CURRENT_ENABLED" != "false" && -n "$CURRENT_MATCHER" ]]; then
                    if echo "$COMMAND" | grep -qE "$CURRENT_MATCHER"; then
                        MATCHED_RULES+=("$CURRENT_NAME")
                        if [[ "$CURRENT_ACTION" == "block" ]]; then
                            DECISION="block"
                            MESSAGE="命令被规则 '$CURRENT_NAME' 阻止：匹配模式 '$CURRENT_MATCHER'"
                        elif [[ "$CURRENT_ACTION" == "warn" && "$DECISION" != "block" ]]; then
                            DECISION="warn"
                            MESSAGE="命令触发规则 '$CURRENT_NAME' 警告：匹配模式 '$CURRENT_MATCHER'"
                        fi
                    fi
                fi
                IN_FRONTMATTER=false
                CURRENT_MATCHER=""
                CURRENT_ACTION=""
                CURRENT_NAME=""
                CURRENT_ENABLED=""
            else
                IN_FRONTMATTER=true
            fi
            continue
        fi
        if $IN_FRONTMATTER; then
            case "$line" in
                name:*) CURRENT_NAME=$(echo "$line" | sed 's/name:[[:space:]]*//;s/"//g') ;;
                enabled:*) CURRENT_ENABLED=$(echo "$line" | sed 's/enabled:[[:space:]]*//') ;;
                matcher:*) CURRENT_MATCHER=$(echo "$line" | sed 's/matcher:[[:space:]]*//;s/"//g') ;;
                action:*) CURRENT_ACTION=$(echo "$line" | sed 's/action:[[:space:]]*//;s/"//g') ;;
            esac
        fi
    done < "$RULES_DIR/security-rules.md"
fi

# ─── 构建输出 ─────────────────────────────────────────────────────────────
RULES_JSON="["
for i in "${!MATCHED_RULES[@]}"; do
    if [[ $i -gt 0 ]]; then RULES_JSON+=","; fi
    RULES_JSON+="\"${MATCHED_RULES[$i]}\""
done
RULES_JSON+="]"

if [[ -z "$MESSAGE" ]]; then
    MESSAGE="命令通过安全检查"
fi

cat <<EOF
{
  "decision": "$DECISION",
  "message": "$MESSAGE",
  "matched_rules": $RULES_JSON,
  "timestamp": "$TIMESTAMP"
}
EOF
