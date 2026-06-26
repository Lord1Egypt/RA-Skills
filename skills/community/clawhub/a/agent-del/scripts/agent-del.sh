#!/usr/bin/env bash
# agent-del.sh — 删除指定的 agent(s)，移到回收站并记录 history
# 用法: agent-del.sh <agentId1> [agentId2] [agentId3] ...
# 兼容 Bash 3.2（macOS 默认）— 不使用 declare -A

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: agent-del.sh <agentId1> [agentId2] ..."
    exit 1
fi

AGENT_IDS=("$@")
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TRASH_DIR="${SKILL_DIR}/.trash"
HISTORY_FILE="${SKILL_DIR}/history/history.md"

echo "=== [0/5] 开始删除 agent(s): ${AGENT_IDS[*]} ==="

# 确保回收站目录存在
mkdir -p "$TRASH_DIR"
echo "  回收站: $TRASH_DIR"

# ---------- 1. 获取 agent 信息并确认存在 ----------
echo ""
echo "=== [1/5] 验证 agent 是否存在 ==="
LIST_JSON=$(openclaw agents list --json 2>/dev/null)

# 用临时文件代替关联数组（兼容 Bash 3.2）
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

for aid in "${AGENT_IDS[@]}"; do
    INFO=$(echo "$LIST_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for a in data:
    if a.get('id','') == '${aid}':
        ws = a.get('workspace','')
        ad = a.get('agentDir','')
        nm = a.get('identityName', a.get('name', ''))
        em = a.get('identityEmoji', '')
        print(ws)
        print(ad)
        print(nm)
        print(em)
        break
" 2>/dev/null)

    WS=$(echo "$INFO" | sed -n '1p')
    AD=$(echo "$INFO" | sed -n '2p')
    NM=$(echo "$INFO" | sed -n '3p')
    EM=$(echo "$INFO" | sed -n '4p')

    # 写入临时文件代替关联数组
    echo "$WS"  > "$TMP_DIR/${aid}.ws"
    echo "$AD"  > "$TMP_DIR/${aid}.ad"
    echo "$NM"  > "$TMP_DIR/${aid}.nm"
    echo "$EM"  > "$TMP_DIR/${aid}.em"

    if [ -n "$WS" ]; then
        echo "  ✅ ${aid}${EM:+ (${EM})} — 存在，待删除"
    else
        echo "  ⚠️  ${aid} — 已不存在（可能已被删除）"
    fi
done

# ---------- 2. 先移到回收站（再执行 delete，避免数据丢失）----------
echo ""
echo "=== [2/5] 移到回收站（先备份再删除）==="

ADD_TIME="$(date '+%Y-%m-%d %H:%M:%S %Z')"

for aid in "${AGENT_IDS[@]}"; do
    WS=$(cat "$TMP_DIR/${aid}.ws" 2>/dev/null)
    NM=$(cat "$TMP_DIR/${aid}.nm" 2>/dev/null)
    EM=$(cat "$TMP_DIR/${aid}.em" 2>/dev/null)

    # 回收站子目录名: agent-{id}-{timestamp}
    TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
    TRASH_SUBDIR="agent-${aid}-${TIMESTAMP}"

    # 移到回收站: workspace（先 mv 再 delete，保证数据完整）
    TW=""
    if [ -n "$WS" ] && [ -d "$WS" ]; then
        TRASH_WS="${TRASH_DIR}/${TRASH_SUBDIR}-workspace"
        mkdir -p "$TRASH_DIR"
        mv "$WS" "$TRASH_WS" 2>/dev/null && {
            echo "  🗑️  workspace → ${TRASH_WS}"
            TW="$TRASH_WS"
        } || echo "  ⚠️  workspace ${WS} 移动失败"
    fi
    echo "$TW" > "$TMP_DIR/${aid}.tw"

    # 移到回收站: agent dir (~/.openclaw/agents/<id>/)
    AGENT_ROOT="${STATE_DIR}/agents/${aid}"
    TA=""
    if [ -d "$AGENT_ROOT" ]; then
        TRASH_AGENT="${TRASH_DIR}/${TRASH_SUBDIR}-agentdir"
        mv "$AGENT_ROOT" "$TRASH_AGENT" 2>/dev/null && {
            echo "  🗑️  agent dir → ${TRASH_AGENT}"
            TA="$TRASH_AGENT"
        } || echo "  ⚠️  agent dir ${AGENT_ROOT} 移动失败"
    fi
    echo "$TA" > "$TMP_DIR/${aid}.ta"
done

# ---------- 3. 执行 openclaw agents delete（数据已备份到回收站）----------
echo ""
echo "=== [3/5] 执行删除命令 ==="
for aid in "${AGENT_IDS[@]}"; do
    echo ""
    echo "> openclaw agents delete ${aid} --force"
    openclaw agents delete "${aid}" --force 2>&1 || true
done

# ---------- 3b. 清理残留目录（已知 bug：CLI 可能提前 return，留下空壳）----------
echo ""
echo "=== [3b/5] 清理残留目录 ==="
for aid in "${AGENT_IDS[@]}"; do
    AGENT_ROOT="${STATE_DIR}/agents/${aid}"
    if [ -d "$AGENT_ROOT" ]; then
        # 数据已在回收站，安全删除残留
        rm -rf "$AGENT_ROOT" 2>/dev/null && {
            echo "  🧹 清理残留目录: ${AGENT_ROOT}"
        } || echo "  ⚠️  残留目录 ${AGENT_ROOT} 清理失败"
    fi
done

# ---------- 4. 记录到 history ----------
mkdir -p "$(dirname "$HISTORY_FILE")"

# 如果 history.md 不存在、为空、或只有空白内容，初始化头部
if [ ! -s "$HISTORY_FILE" ] || ! grep -q '# Agent 删除记录' "$HISTORY_FILE" 2>/dev/null; then
    printf '%s\n' '# Agent 删除记录' > "$HISTORY_FILE"
fi

for aid in "${AGENT_IDS[@]}"; do
    WS=$(cat "$TMP_DIR/${aid}.ws" 2>/dev/null)
    NM=$(cat "$TMP_DIR/${aid}.nm" 2>/dev/null)
    EM=$(cat "$TMP_DIR/${aid}.em" 2>/dev/null)
    TW=$(cat "$TMP_DIR/${aid}.tw" 2>/dev/null)
    TA=$(cat "$TMP_DIR/${aid}.ta" 2>/dev/null)
    AGENT_ROOT="${STATE_DIR}/agents/${aid}"

    cat >> "$HISTORY_FILE" << ENTRY

## ${aid}${EM:+ (${EM})}

- **删除时间:** ${ADD_TIME}
- **Agent ID:** ${aid}
- **显示名称:** ${NM:-(无)}
- **原 Workspace:** ${WS:-(无)}
- **原 Agent 目录:** ${AGENT_ROOT:-(无)}
- **回收站 workspace:** ${TW:-(已不存在)}
- **回收站 agent dir:** ${TA:-(已不存在)}
ENTRY

done

echo "  📝 已记录到 ${HISTORY_FILE}"

# ---------- 5. 最终验证 ----------
echo ""
echo "=== [4/5] 最终验证 ==="

# 确认 agent 外层目录已不存在
for aid in "${AGENT_IDS[@]}"; do
    AGENT_ROOT="${STATE_DIR}/agents/${aid}"
    if [ -d "$AGENT_ROOT" ]; then
        echo "  ⚠️  ${aid}: 目录仍存在 ${AGENT_ROOT}（清理可能不完整）"
    else
        echo "  ✅ ${aid}: 目录已清理"
    fi
done

echo ""
openclaw agents list

echo ""
echo "=== [5/5] 删除完成 ==="
echo ""
echo "CHECKLIST（五步全部出现才算成功）："
echo "  [1/5] 验证 agent 是否存在"
echo "  [2/5] 移到回收站"
echo "  [3/5] 执行删除命令"
echo "  [3b/5] 清理残留目录"
echo "  [4/5] 最终验证"
echo "  [5/5] 删除完成"
echo "已删除的 agent: ${AGENT_IDS[*]}"
echo "回收站位置: ${TRASH_DIR}/agent-*"
echo ""
echo "注意事项："
echo "  1. 原数据已移到回收站 ${TRASH_DIR}/，如需恢复可手动移回"
echo "  2. 如果这些 agent 之前绑定了 channel，请检查 openclaw.json 中的 bindings"
echo "  3. 如需立即生效，运行: openclaw gateway restart"
