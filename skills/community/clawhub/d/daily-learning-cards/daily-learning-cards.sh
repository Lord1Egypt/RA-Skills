#!/bin/bash
set -eo pipefail

# ==============================================
# 学习卡片自动生成（每日 10:00 执行）
# 功能：读取记忆文件 → 提取结构化数据 → 生成学习卡片 → 输出摘要
# 注意：使用 stdout 输出，OpenClaw --announce 会自动投递到配置好的渠道
# ==============================================

# ==================== 配置项 ====================
readonly WORKSPACE_DIR="/home/admin/.openclaw/workspace"
readonly SKILL_DIR="${WORKSPACE_DIR}/skills/daily-learning-cards"
readonly LEARNING_CARDS_DIR="${WORKSPACE_DIR}/memory/learning-cards"
readonly LOG_DIR="${WORKSPACE_DIR}/logs"
readonly LOG_FILE="${LOG_DIR}/learning-cards-cron.log"

# 读取用户配置（如果存在）
CONFIG_FILE="${SKILL_DIR}/config.json"
FEISHU_TARGET="oc_961ed2e84e1c196a9598dc6414d92ea6"  # 默认值
if [ -f "$CONFIG_FILE" ]; then
  FEISHU_TARGET=$(jq -r '.feishu.target // empty' "$CONFIG_FILE") || true
  if [ -z "$FEISHU_TARGET" ]; then
    FEISHU_TARGET="oc_961ed2e84e1c196a9598dc6414d92ea6"
  fi
fi

# ==================== 初始化 ====================
init() {
  mkdir -p "${LEARNING_CARDS_DIR}" "${LOG_DIR}"
}

# ==================== 日志函数 ====================
log() {
  local level="$1"
  local msg="$2"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] ${msg}" >> "${LOG_FILE}"
}

# ==================== 主流程 ====================
main() {
  log "INFO" "任务启动"

  # 1. 获取昨天日期
  local yesterday=$(date -d "yesterday" '+%Y-%m-%d')
  local card_file="${LEARNING_CARDS_DIR}/${yesterday}.md"

  # 2. 检查是否已生成（通过检查文件是否存在且包含发送标记）
  if [ -f "${card_file}" ] && grep -q "自动发送：${yesterday}.*✅ 已发送" "${card_file}" 2>/dev/null; then
    log "INFO" "已发送，跳过"
    # 输出空内容表示跳过
    exit 0
  fi

  # 3. 提取数据
  local json_data
  json_data=$(cd "${SKILL_DIR}" && node scripts/extract.js "${yesterday}" 2>&1)
  
  # 检查是否有内容
  if echo "${json_data}" | grep -q '"hasContent": false'; then
    log "INFO" "无内容，跳过"
    exit 0
  fi
  
  # 4. 生成学习卡片（保存到文件）
  if ! echo "${json_data}" | (cd "${SKILL_DIR}" && node scripts/generate-card.js >/dev/null 2>&1); then
    log "ERROR" "卡片生成失败"
    exit 1
  fi
  
  log "INFO" "卡片生成成功：${card_file}"

  # 5. 生成并输出摘要（stdout，供 OpenClaw --announce 投递）
  local topic_count=$(echo "${json_data}" | jq -r '.stats.topics // 0')
  local decision_count=$(echo "${json_data}" | jq -r '.stats.decisions // 0')
  local pitfall_count=$(echo "${json_data}" | jq -r '.stats.pitfalls // 0')
  local concept_count=$(echo "${json_data}" | jq -r '.stats.concepts // 0')
  
  # 提取主题列表
  local topics=$(echo "${json_data}" | jq -r 'reduce (try .channels[] // [] | .topics[]? | .title) as $t (""; . + ($t // "") + "\n")' | head -5)
  
  # 提取金句
  local insights=$(echo "${json_data}" | (cd "${SKILL_DIR}" && node scripts/extract-insights.js 2>/dev/null))
  
  # 提取踩坑记录
  local pitfalls=$(echo "${json_data}" | (cd "${SKILL_DIR}" && node scripts/extract-pitfalls.js 2>/dev/null))
  
  # 提取新概念
  local concepts=$(echo "${json_data}" | (cd "${SKILL_DIR}" && node scripts/extract-concepts.js 2>/dev/null))

  # 构建主题列表（无emoji）
  local topic_list=""
  local topic_num=0
  while IFS= read -r line; do
    if [ -n "$line" ]; then
      topic_num=$((topic_num + 1))
      topic_list+="   ├─ 主题${topic_num}：${line}
"
    fi
  done <<< "${topics}"
  # 修正最后一个主题的连接符
  topic_list=$(echo "${topic_list}" | sed '$s/├─/└─/')

  # 构建金句列表（emoji改为💬）
  local insight_list=""
  while IFS= read -r line; do
    [ -n "$line" ] && insight_list+="   └─ \"${line}\"
      —— 来源
"
  done <<< "${insights}"
  
  # 构建踩坑列表（emoji改为⚠️）
  local pitfall_list=""
  local pitfall_num=0
  while IFS= read -r line; do
    if [ -n "$line" ]; then
      pitfall_num=$((pitfall_num + 1))
      pitfall_list+="   ├─ 问题${pitfall_num}：${line}
"
    fi
  done <<< "${pitfalls}"
  # 修正最后一个问题的连接符
  pitfall_list=$(echo "${pitfall_list}" | sed '$s/├─/└─/')
  
  # 构建新概念列表（无emoji）
  local concept_list=""
  local concept_num=0
  while IFS= read -r line; do
    if [ -n "$line" ]; then
      concept_num=$((concept_num + 1))
      concept_list+="   ├─ 概念${concept_num}：${line}
"
    fi
  done <<< "${concepts}"
  # 修正最后一个概念的连接符
  concept_list=$(echo "${concept_list}" | sed '$s/├─/└─/')

    # 输出摘要到 stdout（OpenClaw --announce 会自动投递）
  cat << EOF
📝 昨日学习卡片 · ${yesterday}

╔════════════════════════════════════╗
║  📊 学习概览                        ║
╠════════════════════════════════════╣
║  📚 主题：${topic_count:-0} 个                      ║
║  📋 决策：${decision_count:-0} 个                      ║
║  ⚠️ 踩坑：${pitfall_count:-0} 个                      ║
║  🧠 概念：${concept_count:-0} 个                      ║
╚════════════════════════════════════╝

🔥 今日亮点
   └─ 值得回顾的学习内容

📚 核心主题（${topic_count:-0}个）
${topic_list:-   └─ 暂无}

💬 金句摘录（${insights:+1}${insights:-0}条）
${insight_list:-   └─ 暂无}

⚠️ 踩坑记录（${pitfall_count:-0}个）
${pitfall_list:-   └─ 暂无}

🧠 新概念（${concept_count:-0}个）
${concept_list:-   └─ 暂无}

📎 完整卡片：memory/learning-cards/${yesterday}.md

---
💃 金银 Planet · 自我提升部
EOF

  # 6. 发送飞书消息
  local summary="📝 昨日学习卡片 · ${yesterday}

╔════════════════════════════════════╗
║  📊 学习概览                        ║
╠════════════════════════════════════╣
║  📚 主题：${topic_count:-0} 个                      ║
║  📋 决策：${decision_count:-0} 个                      ║
║  ⚠️ 踩坑：${pitfall_count:-0} 个                      ║
║  🧠 概念：${concept_count:-0} 个                      ║
╚════════════════════════════════════╝

📚 核心主题（${topic_count:-0}个）
${topic_list:-   └─ 暂无}

💬 金句摘录（${insights:+1}${insights:-0}条）
${insight_list:-   └─ 暂无}

⚠️ 踩坑记录（${pitfall_count:-0}个）
${pitfall_list:-   └─ 暂无}

🧠 新概念（${concept_count:-0}个）
${concept_list:-   └─ 暂无}

📎 完整卡片：memory/learning-cards/${yesterday}.md

---
💃 金银 Planet · 自我提升部"

  # 使用 openclaw message send 发送飞书消息
  if command -v openclaw &> /dev/null; then
    openclaw message send --channel=feishu --target="${FEISHU_TARGET}" --message="${summary}" 2>&1 | tee -a "${LOG_FILE}"
    SEND_STATUS=${PIPESTATUS[0]}
    if [ $SEND_STATUS -eq 0 ]; then
      log "INFO" "飞书消息已发送到 ${FEISHU_TARGET}"
    else
      log "ERROR" "飞书消息发送失败 (状态码: $SEND_STATUS)"
    fi
  else
    log "WARN" "openclaw 命令不可用，消息未发送"
  fi

  # 7. 标记已发送
  echo -e "\n**自动发送：** $(date '+%Y-%m-%d %H:%M') ✅ 已发送" >> "${card_file}"
  log "INFO" "完成：卡片已生成+发送+标记"
}

# 启动
init
main
exit 0
