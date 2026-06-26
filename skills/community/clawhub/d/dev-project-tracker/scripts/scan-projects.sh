#!/bin/bash
# scan-projects.sh - 扫描项目目录，输出各需求的状态
# 用法: bash scan-projects.sh <projects-root>
# 示例: bash scan-projects.sh /Users/tal/.openclaw/workspace-xxx/projects

PROJECTS_ROOT="${1:-.}"

if [ ! -d "$PROJECTS_ROOT" ]; then
  echo "❌ 目录不存在: $PROJECTS_ROOT"
  exit 1
fi

echo "📋 项目状态扫描 - $(date '+%Y-%m-%d %H:%M')"
echo "=================================="

find "$PROJECTS_ROOT" -name "README.md" -mindepth 2 -maxdepth 4 | sort | while read readme; do
  dir=$(dirname "$readme")
  rel_path="${dir#$PROJECTS_ROOT/}"
  
  # 提取状态
  status=$(grep -E "^\| 状态" "$readme" 2>/dev/null | head -1 | sed 's/.*| *\(.*\) *|$/\1/' | xargs)
  
  # 提取实际上线时间
  online_date=$(grep -E "^\| 实际上线" "$readme" 2>/dev/null | head -1 | sed 's/.*| *\(.*\) *|$/\1/' | xargs)
  
  # 提取需求名称
  name=$(head -1 "$readme" | sed 's/^# *//')
  
  if [ -n "$status" ]; then
    echo ""
    echo "📂 $rel_path"
    echo "   名称: $name"
    echo "   状态: $status"
    echo "   上线: ${online_date:--}"
    
    # 检查是否需要蒸馏/归档
    if [ "$online_date" != "-" ] && [ "$online_date" != "" ]; then
      online_ts=$(date -j -f "%Y-%m-%d" "$online_date" "+%s" 2>/dev/null)
      now_ts=$(date "+%s")
      if [ -n "$online_ts" ]; then
        days_since=$(( (now_ts - online_ts) / 86400 ))
        if [ $days_since -ge 90 ]; then
          echo "   ⚠️  上线已 ${days_since} 天，建议归档"
        elif [ $days_since -ge 14 ]; then
          echo "   ⚠️  上线已 ${days_since} 天，建议蒸馏"
        fi
      fi
    fi
  fi
done

echo ""
echo "=================================="
echo "扫描完成"
