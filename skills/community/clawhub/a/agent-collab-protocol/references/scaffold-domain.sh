#!/bin/bash
# Agent 业务域脚手架 v1.0
# 用法: ./scaffold-domain.sh <domain> <manager_name> "specialist1:角色1 specialist2:角色2 ..."
# 示例: ./scaffold-domain.sh fintech 金融产品经理 "fintech-analyzer:金融分析师 fintech-trader:交易策略师"

set -e

DOMAIN="$1"; MANAGER_NAME="$2"; shift 2; SPECS=("$@")

if [ -z "$DOMAIN" ] || [ -z "$MANAGER_NAME" ] || [ ${#SPECS[@]} -eq 0 ]; then
    echo "用法: $0 <domain> <manager_name> \"speci1:角色1 speci2:角色2 ...\""
    exit 1
fi

ROOT="${HOME}/.openclaw/workspace/${DOMAIN}"
TPL="${HOME}/.openclaw/protocol"
MID="${DOMAIN}-manager"

mkdir -p "${ROOT}/manager"

# --- Template fill helper ---
fill() {
    local file="$1" out="$2"
    shift 2
    cp "$file" "$out"
    while [ $# -ge 2 ]; do
        sed -i "s|$1|$2|g" "$out"
        shift 2
    done
}

# --- Manager ---
echo "Manager: ${MID} (${MANAGER_NAME})"

fill "${TPL}/TEMPLATE_IDENTITY.md"  "${ROOT}/manager/IDENTITY.md" \
    "{AGENT_ID}"   "${MID}" \
    "{AGENT_NAME}" "${MANAGER_NAME}" \
    "L_LEVEL_"     "L1" \
    "{层级描述}"   "业务 Manager 层" \
    "{UPSTREAM}"   "main（总调度）" \
    "{DOWNSTREAM}" "各 Specialist" \
    "{MODEL}"      "deepseek/deepseek-v4-flash"

fill "${TPL}/TEMPLATE_SOUL.md"  "${ROOT}/manager/SOUL.md" \
    "{AGENT_NAME}" "${MANAGER_NAME}"

fill "${TPL}/TEMPLATE_USER.md"  "${ROOT}/manager/USER.md" \
    "{AGENT_NAME}"     "${MANAGER_NAME}" \
    "{UPSTREAM_NAME}"  "总调度" \
    "{说明}"           "转发用户的 ${DOMAIN} 域需求"

fill "${TPL}/TEMPLATE_AGENTS.md" "${ROOT}/manager/AGENTS.md" \
    "{AGENT_NAME}" "${MANAGER_NAME}" \
    "L_LEVEL_"     "L1" \
    "{层级说明}"   "接收 L0 任务，分发给 L2 Specialist"

# --- Specialists ---
SPEC_JSON=""
for sd in "${SPECS[@]}"; do
    SID="${sd%%:*}"; SNAME="${sd##*:}"
    mkdir -p "${ROOT}/${SID}"
    echo "Specialist: ${SID} (${SNAME})"

    fill "${TPL}/TEMPLATE_IDENTITY.md" "${ROOT}/${SID}/IDENTITY.md" \
        "{AGENT_ID}"   "${SID}" \
        "{AGENT_NAME}" "${SNAME}" \
        "L_LEVEL_"     "L2" \
        "{层级描述}"   "执行 Specialist" \
        "{UPSTREAM}"   "${MID}" \
        "{DOWNSTREAM}" "无" \
        "{MODEL}"      "deepseek/deepseek-v4-flash"

    fill "${TPL}/TEMPLATE_SOUL.md" "${ROOT}/${SID}/SOUL.md" \
        "{AGENT_NAME}" "${SNAME}"

    fill "${TPL}/TEMPLATE_USER.md" "${ROOT}/${SID}/USER.md" \
        "{AGENT_NAME}"    "${SNAME}" \
        "{UPSTREAM_NAME}" "${MANAGER_NAME}" \
        "{说明}"          "下发 ${SNAME} 相关任务"

    fill "${TPL}/TEMPLATE_AGENTS.md" "${ROOT}/${SID}/AGENTS.md" \
        "{AGENT_NAME}" "${SNAME}" \
        "L_LEVEL_"     "L2" \
        "{层级说明}"   "纯执行层，不调其他 agent"

    [ -n "$SPEC_JSON" ] && SPEC_JSON+=", "
    SPEC_JSON+="\"${SID}\""
done

# --- Output config snippet ---
cat << JSONEOF
============================================================
📁 文件已生成: ${ROOT}
============================================================

⚠️ 复制以下内容到 ~/.openclaw/openclaw.json:

【1】agents.defaults.subagents.allowAgents 中添加:
   "${MID}"${SPEC_JSON:+, ${SPEC_JSON}}

【2】agents.list 中添加 Manager:
   {
     "id": "${MID}",
     "name": "${MANAGER_NAME}",
     "workspace": "~/.openclaw/workspace/${DOMAIN}/manager",
     "agentDir": "~/.openclaw/agents/${DOMAIN}/manager",
     "systemPromptOverride": "你是${MANAGER_NAME}(${MID})，按AGENTS.md操作手册执行任务。用户指令优先级最高。",
     "model": { "primary": "deepseek/deepseek-v4-flash" },
     "skills": ["subagents", "sessions-spawn", "summarize", "session-logs", "task-planner"],
     "subagents": { "allowAgents": [${SPEC_JSON}] }
   }
JSONEOF

for sd in "${SPECS[@]}"; do
    SID="${sd%%:*}"; SNAME="${sd##*:}"
cat << JSONEOF
   {
     "id": "${SID}",
     "name": "${SNAME}",
     "workspace": "~/.openclaw/workspace/${DOMAIN}/${SID}",
     "agentDir": "~/.openclaw/agents/${DOMAIN}/${SID}",
     "systemPromptOverride": "你是${SNAME}(${SID})，按AGENTS.md操作手册执行任务。",
     "model": { "primary": "deepseek/deepseek-v4-flash" },
     "skills": ["summarize", "session-logs"],
     "subagents": { "allowAgents": [] }
   }
JSONEOF
done

cat << END
【3】创建 sessions 目录:
END
echo "  mkdir -p ~/.openclaw/agents/${DOMAIN}/manager/sessions"
for sd in "${SPECS[@]}"; do
    echo "  mkdir -p ~/.openclaw/agents/${DOMAIN}/${sd%%:*}/sessions"
done

cat << END
【4】编辑各文件中的业务特定占位符（核心信条、工作流程等）
【5】重启 Gateway
============================================================
END
