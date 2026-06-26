#!/bin/bash
# Weekly Distill - 定期提炼
# 将 daily notes 中的重要内容提炼到 MEMORY.md
# 用法: weekly-distill.sh <agent_id>

AGENT_ID="${1:-main}"
WORKSPACE="$HOME/.openclaw/workspaces/$AGENT_ID"

if [ "$AGENT_ID" = "main" ]; then
    WORKSPACE="$HOME/.openclaw/workspace"
fi

MEMORY_DIR="$WORKSPACE/memory"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
LEARNINGS_FILE="$WORKSPACE/.learnings/LEARNINGS.md"

echo "🧪 提炼长期记忆..."

# 获取最近 7 天的日志
RECENT_LOGS=$(find "$MEMORY_DIR" -name "*.md" -mtime -7 2>/dev/null | sort)

if [ -z "$RECENT_LOGS" ]; then
    echo "ℹ️ 没有最近 7 天的日志"
    exit 0
fi

# 用 Python 提炼关键信息
python3 - << PYEOF
import os
import re
from datetime import datetime, timedelta
from collections import Counter

memory_dir = "$MEMORY_DIR"
output_file = "$MEMORY_FILE"
learnings_file = "$LEARNINGS_FILE"

# 收集最近 7 天的关键信息
all_keywords = []
all_projects = set()
all_decisions = []

# 遍历最近日志
for filename in os.listdir(memory_dir):
    if not filename.endswith('.md'):
        continue
    
    filepath = os.path.join(memory_dir, filename)
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except:
        continue
    
    # 提取项目名
    projects = re.findall(r'项目[：:]\s*([^\n,，]+)', content)
    all_projects.update(projects)
    
    # 提取关键词
    keywords = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
    all_keywords.extend(keywords)
    
    # 提取决策（包含"决定"、"方案"等）
    decisions = re.findall(r'([^\n。]+(?:决定|方案|结论)[^\n。]*)', content)
    all_decisions.extend(decisions)

# 统计关键词
keyword_freq = Counter(all_keywords)
top_keywords = [k for k, _ in keyword_freq.most_common(20) if len(k) >= 2]

# 生成提炼内容
distill_content = f"""
---

## 📊 周报提炼 ({datetime.now().strftime('%Y-%m-%d')})

### 活跃项目
{chr(10).join(f'- {p}' for p in list(all_projects)[:5]) if all_projects else '- 无'}

### 高频关键词
{', '.join(top_keywords[:10]) if top_keywords else '无'}

### 重要决策
{chr(10).join(f'- {d[:50]}...' if len(d) > 50 else f'- {d}' for d in all_decisions[:5]) if all_decisions else '- 无'}

---
"""

# 检查是否已有本周提炼
if os.path.exists(output_file):
    with open(output_file, 'r') as f:
        existing = f.read()
    
    week_str = datetime.now().strftime('%Y-%m-%d')
    if f"周报提炼 ({week_str})" not in existing:
        with open(output_file, 'a') as f:
            f.write(distill_content)
        print(f"✅ 已提炼: {len(all_projects)} 项目, {len(top_keywords)} 关键词")
    else:
        print("ℹ️ 本周已提炼")
else:
    with open(output_file, 'w') as f:
        f.write(f"# MEMORY.md - 长期记忆\n\n{distill_content}")
    print("✅ 已创建 MEMORY.md")
PYEOF
