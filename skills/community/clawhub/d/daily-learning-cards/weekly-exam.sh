#!/bin/bash
set -eo pipefail

# ==============================================
# 每周学习测试生成（每周一 11:30 执行）
# 功能：扫描上周学习卡片（周一到周日）→ 生成考题 → 推送飞书
# 模式：规则生成（调用 generate-exam.js）
# ==============================================

readonly WORKSPACE_DIR="/home/admin/.openclaw/workspace"
readonly SKILL_DIR="${WORKSPACE_DIR}/skills/daily-learning-cards"
readonly EXAMS_DIR="${WORKSPACE_DIR}/memory/exam-questions"
readonly LOG_DIR="${WORKSPACE_DIR}/logs"
readonly LOG_FILE="${LOG_DIR}/weekly-exam-cron.log"

init() { mkdir -p "${EXAMS_DIR}" "${LOG_DIR}"; }

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${1}] ${2}" >> "${LOG_FILE}"; }

main() {
  log "INFO" "每周考题生成任务启动"
  
  # 规则生成模式
  log "INFO" "调用 generate-exam.js..."
  
  local exam_content
  if ! exam_content=$(cd "${SKILL_DIR}" && node "scripts/generate-exam.js" 2>&1); then
    log "ERROR" "考题生成失败：${exam_content}"
    exit 1
  fi
  
  if echo "${exam_content}" | grep -q "上周没有学习记录"; then
    log "INFO" "上周无学习记录，跳过"
    exit 0
  fi
  
  log "INFO" "考题生成成功"
  echo "${exam_content}"
  
  # 发送到飞书
  FEISHU_TARGET="oc_961ed2e84e1c196a9598dc6414d92ea6"
  openclaw message send --channel=feishu --target="${FEISHU_TARGET}" --message="${exam_content}" 2>&1
  log "INFO" "考题已推送到飞书 ${FEISHU_TARGET}"
  echo "✅ 考试题目已发送到飞书"
}

init
main
exit 0
