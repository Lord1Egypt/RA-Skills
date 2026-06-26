#!/usr/bin/env bash
# 跨会话记忆规则配置脚本
# 运行方法：bash setup.sh

set -e

# 路径
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SOUL_FILE="$WORKSPACE/SOUL.md"
AGENTS_FILE="$WORKSPACE/AGENTS.md"

echo "=== 跨会话记忆配置 ==="
echo "工作目录: $WORKSPACE"

# --- SOUL.md ---

SOUL_RULE='## 跨会话记忆规则
- 群聊和私聊是独立 session，短期记忆不共享
- 但 `memory/*.md` 和 `MEMORY.md` 是全局共享的
- **群聊里学到的重要信息、用户偏好、决策、上下文 → 必须写到 `memory/YYYY-MM-DD.md`**
- 不要依赖"记住"，写文件才是真正的记忆
- 私聊时先查 `memory_search`，可能需要的群聊上下文在那里'

if [ -f "$SOUL_FILE" ]; then
    if grep -q "跨会话记忆规则" "$SOUL_FILE"; then
        echo -e "\033[33m[跳过]\033[0m SOUL.md 已包含跨会话记忆规则"
    else
        if grep -q "## Behavior Rules" "$SOUL_FILE"; then
            # 在 Behavior Rules 段落之后插入
            sed -i '/## Behavior Rules/,/^## /{ /^## /i\
'"$SOUL_RULE"'
}' "$SOUL_FILE"
        else
            # 追加到文件末尾
            printf '\n\n%s\n' "$SOUL_RULE" >> "$SOUL_FILE"
        fi
        echo -e "\033[32m[已注入]\033[0m SOUL.md 已添加跨会话记忆规则"
    fi
else
    cat > "$SOUL_FILE" << EOF
# SOUL.md

$SOUL_RULE
EOF
    echo -e "\033[32m[已创建]\033[0m SOUL.md 已新建并注入规则"
fi

# --- AGENTS.md ---

AGENTS_RULE='
## 🔗 跨会话记忆
- 群聊和私聊是 **独立 session**，短期记忆（对话上下文）不共享
- 但 `memory/*.md` 和 `MEMORY.md` 是**全局共享的**
- **群聊里学到的重要信息、用户偏好、决策、上下文 → 必须写到 `memory/YYYY-MM-DD.md`**
- 不要依赖"记住"，写文件才是真正的记忆
- 私聊时先 `memory_search`，可能需要的群聊上下文在那里
- **为什么重要：** 你在群里和私聊里是两个独立的"你"，但记忆文件是同一个大脑。不写下来 = 那个 session 里的经历就丢了。
'

if [ -f "$AGENTS_FILE" ]; then
    if grep -q "跨会话记忆" "$AGENTS_FILE"; then
        echo -e "\033[33m[跳过]\033[0m AGENTS.md 已包含跨会话记忆规则"
    else
        if grep -q "## 💓 Heartbeats" "$AGENTS_FILE"; then
            # 在 Heartbeats 之前插入
            sed -i '/## 💓 Heartbeats/i\
'"$AGENTS_RULE"'
' "$AGENTS_FILE"
        else
            printf '\n%s\n' "$AGENTS_RULE" >> "$AGENTS_FILE"
        fi
        echo -e "\033[32m[已注入]\033[0m AGENTS.md 已添加跨会话记忆规则"
    fi
else
    echo -e "\033[31m[警告]\033[0m AGENTS.md 不存在，请确保 OpenClaw 已初始化"
fi

echo ""
echo "=== 配置完成 ==="
echo "建议：重新启动 OpenClaw Gateway 使配置生效"
echo "命令：openclaw gateway restart"
