#!/usr/bin/env bash
# agents-add.sh — 按照用户确认后的信息，通过 openclaw CLI 创建新 agent
# 用法: agents-add.sh <agentId> <agentName> <workspacePath> [model] [description] [emoji]
#   agentId      : agent 的唯一标识（小写字母/数字/连字符）
#   agentName    : agent 的显示名称（用于 identity.name）
#   workspacePath: workspace 绝对路径
#   model        : (可选) 模型 id，如 r740-llama/qwen-aggr-nothink-normal
#   description  : (可选) agent 的定位描述
#   emoji        : (可选) agent 的图标 emoji

set -euo pipefail

AGENT_ID="${1:?Usage: agents-add.sh <agentId> <name> <workspace> [model] [description] [emoji]}"
AGENT_NAME="${2:?Agent name required}"
WORKSPACE="${3:?Workspace path required}"
MODEL="${4:-}"
DESCRIPTION="${5:-}"
EMOJI="${6:-}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HISTORY_DIR="${SKILL_DIR}/history"
HISTORY_FILE="${HISTORY_DIR}/history.md"

echo "=== 开始创建 agent: ${AGENT_ID} ==="
echo "  名称: ${AGENT_NAME}"
echo "  Workspace: ${WORKSPACE}"
[ -n "$MODEL" ] && echo "  Model: ${MODEL}"
[ -n "$DESCRIPTION" ] && echo "  定位: ${DESCRIPTION}"
[ -n "$EMOJI" ] && echo "  图标: ${EMOJI}"

# ---------- 1. 执行 openclaw agents add ----------
# 使用数组构建命令，避免 eval 和未加引号的变量展开
CMD=(openclaw agents add "${AGENT_ID}" --workspace "${WORKSPACE}" --non-interactive)
if [ -n "$MODEL" ]; then
    CMD+=(--model "${MODEL}")
fi

echo ""
echo "> ${CMD[*]}"
"${CMD[@]}"

# ---------- 2. 验证是否添加成功 ----------
echo ""
echo "=== 验证 agent 列表 ==="
openclaw agents list

# 检查 agent 是否在列表中
if openclaw agents list --json 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
ids = [a.get('id','') for a in data]
sys.exit(0 if '${AGENT_ID}' in ids else 1)
" 2>/dev/null; then
    echo ""
    echo "✅ agent '${AGENT_ID}' 添加成功"
else
    # 兼容文本模式检查
    if openclaw agents list 2>/dev/null | grep -q "${AGENT_ID}"; then
        echo ""
        echo "✅ agent '${AGENT_ID}' 添加成功"
    else
        echo ""
        echo "⚠️  agent '${AGENT_ID}' 可能未添加成功，请手动检查"
    fi
fi

# ---------- 3. 检查 workspace 中的 .md 文件 ----------
echo ""
echo "=== 检查 workspace 文件 ==="

REQUIRED_MD_FILES=("AGENTS.md" "SOUL.md" "IDENTITY.md" "USER.md" "TOOLS.md" "HEARTBEAT.md")

MISSING=()
for f in "${REQUIRED_MD_FILES[@]}"; do
    if [ -f "${WORKSPACE}/${f}" ]; then
        echo "  ✅ ${f}"
    else
        echo "  ⚠️  ${f} (缺失)"
        MISSING+=("$f")
    fi
done

# ---------- 4. 从 main workspace 复制缺失的模板文件 ----------
# main workspace 就是 defaults.workspace，从 openclaw.json 读取
MAIN_WORKSPACE=$(python3 -c "
import json, sys
try:
    with open('/root/.openclaw/openclaw.json') as f:
        c = json.load(f)
    ws = c.get('agents',{}).get('defaults',{}).get('workspace','~/.openclaw/workspace')
    from pathlib import Path
    print(str(Path(ws).expanduser().resolve()))
except:
    print('/data1/.openclaw/workspace')
")
if [ ${#MISSING[@]} -gt 0 ] && [ -d "$MAIN_WORKSPACE" ]; then
    echo ""
    echo "=== 从 main workspace 补充缺失文件 ==="
    for f in "${MISSING[@]}"; do
        if [ -f "${MAIN_WORKSPACE}/${f}" ]; then
            cp "${MAIN_WORKSPACE}/${f}" "${WORKSPACE}/${f}"
            echo "  📋 ${f} ← 已从 main workspace 复制"
        else
            # 创建最小占位文件
            echo "# ${f}" > "${WORKSPACE}/${f}"
            echo "  📝 ${f} ← 已创建空文件（main workspace 也没有）"
        fi
    done
fi

# ---------- 5. 记录到 history ----------
echo ""
echo "=== 记录到 history ==="

AGENT_DIR_REL="agents/${AGENT_ID}"
ADD_TIME="$(date '+%Y-%m-%d %H:%M:%S %Z')"

mkdir -p "$HISTORY_DIR"

if [ ! -f "$HISTORY_FILE" ]; then
    echo "# Agent 添加记录\n" > "$HISTORY_FILE"
fi

# 追加一条记录
cat >> "$HISTORY_FILE" << ENTRY

## ${AGENT_NAME} ${EMOJI:+${EMOJI}}

- **添加时间:** ${ADD_TIME}
- **Agent ID:** ${AGENT_ID}
- **显示名称:** ${AGENT_NAME}
- **定位描述:** ${DESCRIPTION:-(无)}
- **图标 emoji:** ${EMOJI:-(无)}
- **模型:** ${MODEL:-(默认)}
- **Workspace:** ${WORKSPACE}
- **Agent 目录相对路径:** ~/.openclaw/${AGENT_DIR_REL}
ENTRY

echo "  📝 已记录到 ${HISTORY_FILE}"

echo ""
echo "=== 完成 ==="
echo "新 agent '${AGENT_NAME}' (${AGENT_ID}) 已创建。"
echo "Workspace: ${WORKSPACE}"
echo ""
echo "是否需要重启 gateway 生效？运行:"
echo "  openclaw gateway restart"
