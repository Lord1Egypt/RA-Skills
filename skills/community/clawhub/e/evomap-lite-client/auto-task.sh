#!/bin/bash
# EvoMap 自动任务执行脚本 - 每 2 小时执行一次
# 流程：获取任务 → 认领任务 → 发布解决方案 → 完成任务
# 日志文件：/tmp/evomap-task.log

LOG_FILE="/tmp/evomap-task.log"
SKILL_DIR="$HOME/.openclaw/workspace/skills/evomap-lite-client"
NODE_ID="node_70e247c67b06eec9"
NODE_PATH="/root/.nvm/versions/node/v22.22.0/bin/node"
NOTIFY_SCRIPT="$SKILL_DIR/notify.sh"
MAX_RETRIES=8  # 增加重试次数

echo "========================================" >> $LOG_FILE
echo "执行时间：$(date)" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

cd $SKILL_DIR

export A2A_NODE_ID=$NODE_ID
export PATH="$NODE_PATH:$PATH"

# 步骤 1：获取任务（增强重试）
echo "【步骤 1】获取任务... (最大重试：$MAX_RETRIES)" >> $LOG_FILE

# 手动实现增强重试逻辑，避免 rate limit
for i in $(seq 1 $MAX_RETRIES); do
    echo "尝试第 $i 次获取任务..." >> $LOG_FILE
    result=$($NODE_PATH index.js fetch 2>&1)
    echo "$result" >> $LOG_FILE
    
    # 检查是否获取到任务
    if echo "$result" | grep -q "获取到 [1-9]"; then
        echo "✅ 成功获取到任务" >> $LOG_FILE
        break
    fi
    
    # 如果是 server_busy 或 rate_limited，等待后重试
    if echo "$result" | grep -q "server_busy\|rate_limited"; then
        wait_time=$((3000 + i * 1000))  # 递增等待时间
        echo "⏳ 服务器繁忙，等待 ${wait_time}ms 后重试..." >> $LOG_FILE
        sleep $(echo "scale=3; $wait_time/1000" | bc)
    else
        # 无任务或其他错误，退出循环
        break
    fi
done

# 检查是否有任务
if echo "$result" | grep -q "获取到 0 个任务"; then
    echo "⏳ 暂无可用任务，等待下次执行" >> $LOG_FILE
    echo "STATUS: NO_TASKS" >> $LOG_FILE
    echo "" >> $LOG_FILE
    # 无任务时不通知
    exit 0
fi

# 提取任务 ID（假设只有一个任务）
TASK_ID=$(echo "$result" | grep -o '"task_id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$TASK_ID" ]; then
    echo "⚠️  无法提取任务 ID" >> $LOG_FILE
    echo "STATUS: NO_TASK_ID" >> $LOG_FILE
    echo "" >> $LOG_FILE
    # bash "$NOTIFY_SCRIPT" "ERROR" "无法提取任务 ID"  # 通知功能已禁用
    exit 0
fi

echo "📋 获取到任务：$TASK_ID" >> $LOG_FILE

# 步骤 2：认领任务
echo "" >> $LOG_FILE
echo "【步骤 2】认领任务 $TASK_ID..." >> $LOG_FILE
claim_result=$(curl -s -X POST "https://evomap.ai/a2a/task/claim" \
    -H "Content-Type: application/json" \
    -d "{\"task_id\":\"$TASK_ID\",\"node_id\":\"$NODE_ID\"}" 2>&1)
echo "$claim_result" >> $LOG_FILE

if echo "$claim_result" | grep -q '"error"'; then
    echo "⚠️  认领任务失败" >> $LOG_FILE
    echo "STATUS: CLAIM_FAILED" >> $LOG_FILE
    echo "" >> $LOG_FILE
    bash "$NOTIFY_SCRIPT" "CLAIM_FAILED" "$TASK_ID"
    exit 0
fi

echo "✅ 任务认领成功" >> $LOG_FILE

# 步骤 3：发布解决方案（使用已有的资产）
echo "" >> $LOG_FILE
echo "【步骤 3】发布解决方案..." >> $LOG_FILE
publish_result=$($NODE_PATH publish-asset-v2.js 2>&1)
echo "$publish_result" >> $LOG_FILE

# 检查发布是否成功（包括 duplicate_asset 也算成功）
if echo "$publish_result" | grep -q "发布成功\|published\|duplicate_asset"; then
    echo "✅ 解决方案发布成功" >> $LOG_FILE
    
    # 提取资产 ID
    ASSET_ID=$(echo "$publish_result" | grep -o 'sha256:[a-f0-9]\{64\}' | head -1)
    
    if [ -z "$ASSET_ID" ]; then
        # 如果是 duplicate_asset，使用已存在的资产 ID
        ASSET_ID=$(echo "$publish_result" | grep -o '"target_asset_id":"sha256:[^"]*"' | cut -d'"' -f4)
    fi
    
    echo "📦 资产 ID: $ASSET_ID" >> $LOG_FILE
    
    # 步骤 4：完成任务
    echo "" >> $LOG_FILE
    echo "【步骤 4】完成任务..." >> $LOG_FILE
    complete_result=$(curl -s -X POST "https://evomap.ai/a2a/task/complete" \
        -H "Content-Type: application/json" \
        -d "{\"task_id\":\"$TASK_ID\",\"asset_id\":\"$ASSET_ID\",\"node_id\":\"$NODE_ID\"}" 2>&1)
    echo "$complete_result" >> $LOG_FILE
    
    if echo "$complete_result" | grep -q '"error"'; then
        echo "⚠️  完成任务失败" >> $LOG_FILE
        echo "STATUS: COMPLETE_FAILED" >> $LOG_FILE
        bash "$NOTIFY_SCRIPT" "COMPLETE_FAILED" "$TASK_ID"
    else
        echo "✅ 任务完成成功！" >> $LOG_FILE
        echo "STATUS: SUCCESS" >> $LOG_FILE
        bash "$NOTIFY_SCRIPT" "SUCCESS" "$TASK_ID"
    fi
else
    echo "⚠️  发布解决方案失败" >> $LOG_FILE
    echo "STATUS: PUBLISH_FAILED" >> $LOG_FILE
    bash "$NOTIFY_SCRIPT" "PUBLISH_FAILED" "$TASK_ID"
fi

echo "" >> $LOG_FILE
