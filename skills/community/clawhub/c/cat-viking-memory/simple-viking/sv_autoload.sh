#!/usr/bin/env bash
# Viking Auto-Load Script
# 会话开始时自动加载上下文到 system prompt
# 用法: sv_autoload.sh [agent_name]
# 输出: 格式化的上下文文本

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/lib.sh"

# 默认 Agent
AGENT_NAME="${1:-maojingli}"
SV_WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking-$AGENT_NAME}"

echo "=== Viking Auto-Load: $AGENT_NAME ==="
echo ""

# ===== 1. 加载核心配置 =====
echo "📋 加载配置..."
CONFIG_FILE="$SV_WORKSPACE/agent/memories/config/config.md"
if [[ -f "$CONFIG_FILE" ]]; then
  echo "--- CONFIG ---"
  cat "$CONFIG_FILE"
  echo ""
else
  echo "[配置不存在: $CONFIG_FILE]"
  echo ""
fi

# ===== 2. 加载 hot/ 目录（7天内文件） =====
echo "🔥 加载热点记忆 (7天内)..."
HOT_DIR="$SV_WORKSPACE/agent/memories/hot"
if [[ -d "$HOT_DIR" ]]; then
  # 找出7天内的文件，排除 . 开头的隐藏文件和目录
  find "$HOT_DIR" -name "*.md" -type f -mtime -7 2>/dev/null | grep -v "/\." | head -5 | while read -r file; do
    echo "--- $(basename "$file") ---"
    head -c 2000 "$file"  # 限制长度，避免超过 token 限制
    echo ""
  done
else
  echo "[热点目录不存在: $HOT_DIR]"
  echo ""
fi

# ===== 3. 加载 warm/ 目录（30天内文件） =====
echo "🌡️ 加载近期记忆 (30天内)..."
WARM_DIR="$SV_WORKSPACE/agent/memories/warm"
if [[ -d "$WARM_DIR" ]]; then
  find "$WARM_DIR" -name "*.md" -type f -mtime -30 2>/dev/null | while read -r file; do
    echo "--- $(basename "$file") ---"
    head -c 1000 "$file"  # 限制长度
    echo ""
  done
fi
echo ""

# ===== 4. 搜索最近任务/待办 =====
echo "📌 搜索待办任务..."
# 搜索包含 TODO 或任务关键词的文件（排除 important 和压缩目录）
TODO_FILES=$(find "$SV_WORKSPACE/agent/memories/hot" "$SV_WORKSPACE/agent/memories/warm" \
  -name "*.md" -type f -mtime -7 2>/dev/null | grep -v "/important/" | grep -v "/.compressed/")
if [[ -n "$TODO_FILES" ]]; then
  echo "$TODO_FILES" | xargs grep -l -E "(TODO|待办|任务|\[\s\])" 2>/dev/null | head -5 | while read -r file; do
    rel_path="${file#$SV_WORKSPACE/}"
    echo "--- $rel_path ---"
    grep -n -E "(TODO|待办|任务|\[\s\])" "$file" 2>/dev/null | head -10
    echo ""
  done
fi

# ===== 5. 搜索最近决策 =====
echo "⚡ 搜索最近决策..."
if [[ -d "$SV_WORKSPACE/resources" ]]; then
  DECISION_FILES=$(find "$SV_WORKSPACE/resources" -name "*.md" -type f -mtime -30 2>/dev/null)
  if [[ -n "$DECISION_FILES" ]]; then
    echo "$DECISION_FILES" | xargs grep -l -i -E "(决策|decision|决定)" 2>/dev/null | head -3 | while read -r file; do
      rel_path="${file#$SV_WORKSPACE/}"
      echo "--- $rel_path ---"
      head -c 500 "$file"
      echo ""
    done
  fi
fi

# ===== 6. 全局 Viking 关键信息 =====
echo "🌐 加载全局上下文..."
GLOBAL_WORKSPACE="$HOME/.openclaw/viking-global"
if [[ -d "$GLOBAL_WORKSPACE" ]]; then
  # 加载董事长偏好
  if [[ -f "$GLOBAL_WORKSPACE/boss/preferences.md" ]]; then
    echo "--- 董事长偏好 ---"
    head -c 500 "$GLOBAL_WORKSPACE/boss/preferences.md"
    echo ""
  fi
  
  # 加载团队信息
  if [[ -f "$GLOBAL_WORKSPACE/team/members.md" ]]; then
    echo "--- 团队成员 ---"
    head -c 300 "$GLOBAL_WORKSPACE/team/members.md"
    echo ""
  fi
fi

echo "=== 加载完成 ==="
