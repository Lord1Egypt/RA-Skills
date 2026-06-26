#!/bin/bash
# apollo-workflow task-result-collector.sh
# 收集subagent结果到文件
# 用法: task-result-collector.sh <task_id> <result_file>

WORKFLOW_DIR="/root/.openclaw/workspace/.workflow"
TASK_RESULTS_DIR="$WORKFLOW_DIR/task-results"

TASK_ID="$1"
RESULT_FILE="$2"

if [ -z "$TASK_ID" ] || [ -z "$RESULT_FILE" ]; then
    echo "用法: task-result-collector.sh <task_id> <result_file>"
    echo "示例: task-result-collector.sh 01 /tmp/task-01-result.md"
    exit 1
fi

mkdir -p "$TASK_RESULTS_DIR"

DEST="$TASK_RESULTS_DIR/task-${TASK_ID}-result.json"

# 如果result_file是markdown，转为json摘要
if [[ "$RESULT_FILE" == *.md ]]; then
    python3 - <<EOF
import json
import sys

with open('$RESULT_FILE', 'r') as f:
    content = f.read()

# 提取摘要
lines = content.split('\n')[:20]  # 前20行
summary = '\n'.join(lines)

result = {
    "task_id": "$TASK_ID",
    "source_file": "$RESULT_FILE",
    "summary": summary,
    "collected_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}

with open('$DEST', 'w') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"✅ 结果已收集: $DEST")
EOF
elif [[ "$RESULT_FILE" == *.json ]]; then
    cp "$RESULT_FILE" "$DEST"
    echo "✅ JSON结果已复制: $DEST"
else
    # 原始文件
    cp "$RESULT_FILE" "$DEST"
    echo "✅ 结果已保存: $DEST"
fi

# 更新state.json中的completed_tasks
python3 - <<EOF
import json

state_file = "$WORKFLOW_DIR/state.json"
try:
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    completed = state.get('completed_tasks', [])
    if "$TASK_ID" not in completed:
        completed.append("$TASK_ID")
        state['completed_tasks'] = completed
        state['last_updated'] = "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    print(f"📊 state.json已更新: completed_tasks={completed}")
except Exception as e:
    print(f"⚠️  更新state.json失败: {e}")
EOF
