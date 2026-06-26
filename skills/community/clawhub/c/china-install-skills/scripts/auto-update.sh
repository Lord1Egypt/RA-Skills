#!/bin/bash
# 每周自动更新检查脚本
# 用法：./auto-update.sh [AGENT_WORKSPACE]
# 推荐 crontab: 0 3 * * 0 /path/to/auto-update.sh

set -e

AGENT_WORKSPACE="${1:-/Users/xubangbang/.openclaw/workspace}"
LOG_FILE="/tmp/clawhub-update-$(date +%Y%m%d).log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== 🕷️ ClawHub 技能更新检查 ===" | tee "$LOG_FILE"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "工作区：${AGENT_WORKSPACE}" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

UPDATE_AVAILABLE=0
SKILLS_CHECKED=0

# 遍历所有 agent 的 skills 目录
for agent_dir in ${AGENT_WORKSPACE}/agents/*/; do
  if [ ! -d "$agent_dir" ]; then
    continue
  fi
  
  AGENT_NAME=$(basename "$agent_dir")
  SKILLS_DIR="${agent_dir}skills"
  
  if [ ! -d "$SKILLS_DIR" ]; then
    continue
  fi
  
  echo "📂 检查 Agent: ${AGENT_NAME}" | tee -a "$LOG_FILE"
  echo "  路径：${SKILLS_DIR}" | tee -a "$LOG_FILE"
  
  # 遍历该 agent 的所有技能
  for skill_dir in ${SKILLS_DIR}/*/; do
    if [ ! -d "$skill_dir" ]; then
      continue
    fi
    
    SLUG=$(basename "$skill_dir")
    META_FILE="${skill_dir}_meta.json"
    
    # 跳过 clawhub-browser 自身
    if [ "$SLUG" = "clawhub-browser" ]; then
      continue
    fi
    
    SKILLS_CHECKED=$((SKILLS_CHECKED + 1))
    
    # 获取当前版本
    if [ -f "$META_FILE" ]; then
      CURRENT_VER=$(grep '"version"' "$META_FILE" | sed 's/.*"version"[^"]*"\([^"]*\)".*/\1/')
    else
      CURRENT_VER="unknown"
    fi
    
    echo "  🔍 ${SLUG} (v${CURRENT_VER})" | tee -a "$LOG_FILE"
    
    # 尝试获取最新版本（通过搜索页面）
    # 注意：这里简化处理，实际可能需要更复杂的解析
    LATEST_VER=$(curl -sL "https://clawhub.com/skills?q=${SLUG}" 2>/dev/null | \
      grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | \
      head -1 || echo "")
    
    if [ -n "$LATEST_VER" ] && [ "$LATEST_VER" != "$CURRENT_VER" ]; then
      echo "    ⚠️  可更新：${CURRENT_VER} → ${LATEST_VER}" | tee -a "$LOG_FILE"
      UPDATE_AVAILABLE=$((UPDATE_AVAILABLE + 1))
    elif [ -n "$LATEST_VER" ]; then
      echo "    ✅ 已是最新" | tee -a "$LOG_FILE"
    else
      echo "    ℹ️  无法检查远程版本（可能限流）" | tee -a "$LOG_FILE"
    fi
  done
  
  echo "" | tee -a "$LOG_FILE"
done

# 汇总报告
echo "=== 检查完成 ===" | tee -a "$LOG_FILE"
echo "检查技能数：${SKILLS_CHECKED}" | tee -a "$LOG_FILE"

if [ $UPDATE_AVAILABLE -gt 0 ]; then
  echo "" | tee -a "$LOG_FILE"
  echo "🔔 发现 ${UPDATE_AVAILABLE} 个技能可更新！" | tee -a "$LOG_FILE"
  echo "" | tee -a "$LOG_FILE"
  echo "运行以下命令更新：" | tee -a "$LOG_FILE"
  echo "  cd ${SCRIPT_DIR}" | tee -a "$LOG_FILE"
  echo "  ./download.sh <技能名>" | tee -a "$LOG_FILE"
  echo "  ./install.sh <技能名> <目标目录> --force" | tee -a "$LOG_FILE"
else
  echo "" | tee -a "$LOG_FILE"
  echo "✅ 所有技能都是最新版本" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "日志：${LOG_FILE}" | tee -a "$LOG_FILE"
echo "---" | tee -a "$LOG_FILE"

# 如果有更新，可以发送邮件或通知（可选）
# if [ $UPDATE_AVAILABLE -gt 0 ]; then
#   echo "发现技能更新" | mail -s "ClawHub 更新通知" user@example.com
# fi

exit 0
