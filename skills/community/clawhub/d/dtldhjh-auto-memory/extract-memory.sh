#!/bin/bash
# Auto Memory v1.3.0 - 自动记忆更新
# 功能：提取对话、清理过期、优先级过滤、跨Agent共享、智能摘要、增量索引、定期提炼
# 用法: extract-memory.sh <agent_id>

AGENT_ID="${1:-main}"
WORKSPACE="$HOME/.openclaw/workspaces/$AGENT_ID"
SESSIONS_DIR="$HOME/.openclaw/agents/$AGENT_ID/sessions"
SHARED_LEARNINGS="$HOME/.openclaw/workspace/.learnings/shared"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +%H:%M)
DAYS_TO_KEEP=30

# 处理 main agent 的特殊路径
if [ "$AGENT_ID" = "main" ]; then
    WORKSPACE="$HOME/.openclaw/workspace"
fi

# 确保目录存在
mkdir -p "$WORKSPACE/memory"
mkdir -p "$WORKSPACE/.learnings"
mkdir -p "$WORKSPACE/.openclaw"
mkdir -p "$SHARED_LEARNINGS"

MEMORY_FILE="$WORKSPACE/memory/$TODAY.md"
LEARNINGS_FILE="$WORKSPACE/.learnings/LEARNINGS.md"
ERRORS_FILE="$WORKSPACE/.learnings/ERRORS.md"
SHARED_ERRORS="$SHARED_LEARNINGS/common-errors.md"
SHARED_BEST_PRACTICES="$SHARED_LEARNINGS/best-practices.md"
INDEX_STATE="$WORKSPACE/.openclaw/.index-state.json"

# =====================
# Part 1: 自动过期清理
# =====================

echo "🧹 检查过期文件..."

EXPIRED_FILES=$(find "$WORKSPACE/memory" -name "*.md" -mtime +$DAYS_TO_KEEP 2>/dev/null)
if [ -n "$EXPIRED_FILES" ]; then
    mkdir -p "$WORKSPACE/memory/archive"
    echo "$EXPIRED_FILES" | while read f; do
        [ -n "$f" ] && mv "$f" "$WORKSPACE/memory/archive/" 2>/dev/null
    done
    echo "   📦 已归档过期日志"
fi

# =====================
# Part 2: 主动加载学习经验（优先级过滤）
# =====================

echo "📚 加载学习经验..."

count_high() {
    local file="$1"
    if [ -f "$file" ]; then
        grep -E "Priority: (critical|high)" "$file" 2>/dev/null | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

LEARN_HIGH=$(count_high "$LEARNINGS_FILE")
ERR_HIGH=$(count_high "$ERRORS_FILE")
SHARED_ERR=$(count_high "$SHARED_ERRORS")
SHARED_BEST=$(count_high "$SHARED_BEST_PRACTICES")

[ "$LEARN_HIGH" != "0" ] && echo "   ⚠️ 学习经验: $LEARN_HIGH 条高优先级"
[ "$ERR_HIGH" != "0" ] && echo "   🔴 错误记录: $ERR_HIGH 条高优先级"
[ "$SHARED_ERR" != "0" ] && echo "   🌐 共享错误: $SHARED_ERR 条"
[ "$SHARED_BEST" != "0" ] && echo "   💡 共享最佳实践: $SHARED_BEST 条"

# =====================
# Part 3: 提取 session 对话
# =====================

RECENT_SESSION=$(find "$SESSIONS_DIR" -name "*.jsonl" -mmin -360 2>/dev/null | head -1)

if [ -n "$RECENT_SESSION" ]; then
    echo "📄 分析 session: $(basename $RECENT_SESSION)"

    # 导出环境变量供 Python 使用
    export RECENT_SESSION MEMORY_FILE LEARNINGS_FILE ERRORS_FILE SHARED_ERRORS SHARED_BEST_PRACTICES AGENT_ID NOW

    python3 << 'PYEOF'
import json
import sys
import os
import re
from datetime import datetime
from collections import Counter

# 从环境变量读取
session_file = os.environ.get('RECENT_SESSION', '')
output_file = os.environ.get('MEMORY_FILE', '')
learnings_file = os.environ.get('LEARNINGS_FILE', '')
errors_file = os.environ.get('ERRORS_FILE', '')
shared_errors = os.environ.get('SHARED_ERRORS', '')
shared_best = os.environ.get('SHARED_BEST_PRACTICES', '')
agent_id = os.environ.get('AGENT_ID', 'main')
now = os.environ.get('NOW', '')

if not session_file or not os.path.exists(session_file):
    print("ℹ️ session 文件不存在")
    sys.exit(0)

# 读取 session
messages = []
seen_content = set()

try:
    with open(session_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get('type') == 'message':
                    msg = data.get('message', {})
                    role = msg.get('role', '')
                    content = msg.get('content', '')
                    
                    if isinstance(content, list):
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text = item.get('text', '')
                                if not text.startswith('System: [') and not text.startswith('Read HEARTBEAT'):
                                    text_parts.append(text)
                        content = '\n'.join(text_parts)
                    
                    if role in ['user', 'assistant'] and content:
                        if content.startswith('System: [') or content.startswith('Read HEARTBEAT'):
                            continue
                        if content in seen_content:
                            continue
                        seen_content.add(content)
                        messages.append({'role': role, 'content': content[:400]})
            except:
                continue
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# 检测规则
important_keywords = ['项目', '问题', '需要', '帮我', '怎么', '为什么', '方案', '设计', '待办']
error_keywords = ['错误', '失败', '报错', 'error', 'failed', 'exception', 'bug', '崩溃']
correction_keywords = ['不对', '错了', '应该', '其实', '实际上', '不是']
best_practice_keywords = ['最佳', '推荐', '建议', '最好', '优化']

filtered = []
learnings_to_add = []
errors_to_add = []
best_practices_to_add = []
all_keywords = []

for i, msg in enumerate(messages):
    if msg['role'] == 'user':
        content_lower = msg['content'].lower()
        
        # 收集关键词
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,}', msg['content'])
        all_keywords.extend(keywords)
        
        # 检测重要对话
        if any(kw in content_lower for kw in important_keywords) or len(msg['content']) > 20:
            filtered.append(msg)
            if i + 1 < len(messages) and messages[i + 1]['role'] == 'assistant':
                filtered.append(messages[i + 1])
        
        # 检测错误
        if any(kw in content_lower for kw in error_keywords):
            priority = 'critical' if any(kw in content_lower for kw in ['崩溃', 'critical', '严重']) else 'high'
            errors_to_add.append({
                'user': msg['content'][:150],
                'priority': priority,
                'shared': any(kw in content_lower for kw in ['API', '网络', '配置', '权限'])
            })
        
        # 检测纠正
        if any(kw in content_lower for kw in correction_keywords):
            learnings_to_add.append({
                'type': 'correction',
                'priority': 'high',
                'content': msg['content'][:150]
            })
        
        # 检测最佳实践
        if any(kw in content_lower for kw in best_practice_keywords):
            best_practices_to_add.append({
                'content': msg['content'][:150],
                'shared': True
            })

# 智能摘要生成
if filtered:
    keyword_freq = Counter(all_keywords)
    top_keywords = [k for k, _ in keyword_freq.most_common(5) if len(k) >= 2]
    keyword_summary = f"关键词: {', '.join(top_keywords)}" if top_keywords else ""
    
    with open(output_file, 'a') as f:
        f.write(f"\n---\n\n## Session 自动提取 ({now})\n\n")
        if keyword_summary:
            f.write(f"📝 {keyword_summary}\n\n")
        for msg in filtered[:16]:
            role_label = "👤" if msg['role'] == 'user' else "🤖"
            content = msg['content'].replace('\n', ' ').strip()
            if len(content) > 200:
                content = content[:200] + "..."
            f.write(f"**{role_label}**: {content}\n\n")
    print(f"✅ 已更新 memory: {len(filtered)} 条消息")
    if top_keywords:
        print(f"   📝 摘要: {', '.join(top_keywords[:3])}")

# 写入 learnings
if learnings_to_add:
    with open(learnings_file, 'a') as f:
        for l in learnings_to_add:
            f.write(f"\n## [LRN-{datetime.now().strftime('%Y%m%d%H%M')}] {l['type']}\n\n")
            f.write(f"**Logged**: {datetime.now().isoformat()}\n")
            f.write(f"**Priority**: {l['priority']}\n")
            f.write(f"**Status**: pending\n\n")
            f.write(f"### Summary\n{l['content']}\n\n---\n")
    print(f"✅ 已记录学习: {len(learnings_to_add)} 条")

# 写入 errors
if errors_to_add:
    with open(errors_file, 'a') as f:
        for e in errors_to_add:
            f.write(f"\n## [ERR-{datetime.now().strftime('%Y%m%d%H%M')}]\n\n")
            f.write(f"**Logged**: {datetime.now().isoformat()}\n")
            f.write(f"**Priority**: {e['priority']}\n")
            f.write(f"**Status**: pending\n\n")
            f.write(f"### Context\n{e['user']}\n\n---\n")
    
    shared = [e for e in errors_to_add if e.get('shared')]
    if shared:
        with open(shared_errors, 'a') as f:
            for e in shared:
                f.write(f"\n## [SHARED-ERR-{datetime.now().strftime('%Y%m%d%H%M')}]\n\n")
                f.write(f"**Source**: {agent_id}\n")
                f.write(f"**Priority**: {e['priority']}\n\n")
                f.write(f"### Context\n{e['user']}\n\n---\n")
        print(f"📤 已共享错误: {len(shared)} 条")
    
    print(f"✅ 已记录错误: {len(errors_to_add)} 条")

# 写入最佳实践
if best_practices_to_add:
    with open(shared_best, 'a') as f:
        for b in best_practices_to_add:
            f.write(f"\n## [BEST-{datetime.now().strftime('%Y%m%d%H%M')}]\n\n")
            f.write(f"**Source**: {agent_id}\n")
            f.write(f"**Logged**: {datetime.now().isoformat()}\n\n")
            f.write(f"### Content\n{b['content']}\n\n---\n")
    print(f"💡 已记录最佳实践: {len(best_practices_to_add)} 条")

if not filtered and not learnings_to_add and not errors_to_add:
    print("ℹ️ 没有发现重要内容")
PYEOF
else
    echo "ℹ️ 没有最近6小时的 session 文件"
fi

# =====================
# Part 5: 增量索引
# =====================

echo "🔄 更新向量索引..."

NEED_INDEX=0
if [ -f "$INDEX_STATE" ]; then
    CHANGED=$(find "$WORKSPACE/memory" "$WORKSPACE/.learnings" -name "*.md" -newer "$INDEX_STATE" 2>/dev/null | wc -l)
    if [ "$CHANGED" -gt 0 ]; then
        NEED_INDEX=1
    fi
else
    NEED_INDEX=1
fi

if [ "$NEED_INDEX" = "1" ]; then
    openclaw memory index --agent "$AGENT_ID" 2>/dev/null
    date +%s > "$INDEX_STATE"
    echo "✅ 索引已更新"
else
    echo "ℹ️ 无变更，跳过索引"
fi

# =====================
# Part 6: 周报提炼（每周日执行）
# =====================

WEEKDAY=$(date +%u)
if [ "$WEEKDAY" = "7" ]; then
    echo "📊 执行周报提炼..."
    if [ -x ~/.openclaw/scripts/weekly-distill.sh ]; then
        ~/.openclaw/scripts/weekly-distill.sh "$AGENT_ID"
    fi
fi
