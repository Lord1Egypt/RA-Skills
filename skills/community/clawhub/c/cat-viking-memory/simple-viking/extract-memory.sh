#!/usr/bin/env bash
# SimpleViking Extract Memory - 从会话记录提取长期记忆
# 用法: sv_extract_memory --session /path/to/session.jsonl

source "$(dirname "$0")/lib.sh"

# 默认配置
workspace="${SV_WORKSPACE}"
user_mem_dir="$workspace/user/memories"
agent_mem_dir="$workspace/agent/memories"
resources_dir="$workspace/resources"

# 解析参数
session_file=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --session)
      session_file="$2"
      shift 2
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$session_file" ]]; then
  echo "用法: sv_extract_memory --session /path/to/session.jsonl"
  exit 1
fi

if [[ ! -f "$session_file" ]]; then
  echo "错误: 会话文件不存在: $session_file"
  exit 1
fi

sv_log INFO "开始从会话提取记忆: $session_file"

# 1. 提取用户偏好（简化：根据 assistant 回复推断）
# 这里需要一个模型来总结，为了简化，我们假设外部已处理，直接追加到 preferences 日志
user_pref_file="$user_mem_dir/preferences.log"
sv_ensure_dir "$(dirname "$user_pref_file")"

# 扫描对话中是否有明确的偏好声明（如"我喜欢..."、"不要..."）
grep -E '"role":"user"|"role":"assistant"' "$session_file" | \
  python3 -c "
import sys, json, re
prefs = []
for line in sys.stdin:
  try:
    msg = json.loads(line)
    role = msg.get('role')
    content = msg.get('content', '')
    # 简单关键词匹配（实际应用应该调用模型）
    if '我喜欢' in content or '我偏好' in content or '不要' in content or '请勿' in content:
      prefs.append(f'[{role}] {content[:200]}')
  except:
    pass
if prefs:
  print('\n'.join(prefs))
" >> "$user_pref_file" 2>/dev/null || true

# 2. 提取 Agent 经验教训
agent_exp_file="$agent_mem_dir/lessons.log"
sv_ensure_dir "$(dirname "$agent_exp_file")"

# 从 tool 调用结果中提取成功/失败模式
grep -E '"role":"assistant"|"tool_result"' "$session_file" | \
  python3 -c "
import sys, json
lessons = []
for line in sys.stdin:
  try:
    msg = json.loads(line)
    if 'tool_calls' in msg:
      # 记录使用的工具
      for call in msg.get('tool_calls', []):
        lessons.append(f\"工具调用: {call.get('name')} - 参数: {call.get('arguments')}\")
    if 'tool_result' in msg:
      # 记录工具结果状态
      status = '成功' if msg.get('status') == 'ok' else '失败'
      lessons.append(f\"工具结果: {status} - {msg.get('content','')[:100]}\")
  except:
    pass
if lessons:
  print('\n'.join(lessons))
" >> "$agent_exp_file" 2>/dev/null || true

# 3. 会话摘要写入 resources/sessions/
session_date=$(date +%Y-%m-%d)
session_id=$(basename "$session_file" .jsonl)
session_res_dir="$resources_dir/sessions/$session_date"
sv_ensure_dir "$session_res_dir"

# 生成会话摘要文件（简化版）
echo "# 会话摘要\n" > "$session_res_dir/${session_id}.md"
echo "时间: $(date -r "$session_file" 2>/dev/null || echo 'unknown')" >> "$session_res_dir/${session_id}.md"
echo "文件: $session_file" >> "$session_res_dir/${session_id}.md"
echo "" >> "$session_res_dir/${session_id}.md"

# 提取关键对话片段
python3 -c "
import sys, json
snippets = []
count = 0
for line in open('$session_file', 'r', encoding='utf-8', errors='ignore'):
  try:
    msg = json.loads(line)
    role = msg.get('role')
    content = msg.get('content', '')
    if role in ('user', 'assistant') and content.strip():
      snippets.append(f'**{role}**: {content[:150]}...')
      count += 1
      if count >= 5:
        break
  except:
    pass
print('\n'.join(snippets))
" >> "$session_res_dir/${session_id}.md"

# 4. 更新相关目录的层级
sv_update_tree_layers "$session_res_dir"

sv_log INFO "记忆提取完成"
echo "已更新:"
echo "  - 用户偏好: $user_pref_file"
echo "  - Agent 经验: $agent_exp_file"
echo "  - 会话摘要: $session_res_dir/${session_id}.md"