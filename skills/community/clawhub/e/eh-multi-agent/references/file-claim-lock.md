# File Claim Lock

## Problem

多个 agent 同时编辑同一文件会产生冲突——agent A 读取文件，agent B 修改并保存，agent A 基于过期内容覆写。Git merge conflict 在 agent 场景下更难解决，因为 agent 不擅长处理 conflict marker。

## Solution

编辑文件前在 `.claims/` 目录创建 lock 文件，宣告对该文件的独占编辑权。其他 agent 的 PreToolUse hook 检测到 lock 存在时拒绝编辑操作。Lock 文件包含持有者信息和超时时间，防止 crash 后的死锁。

## Implementation

1. PreToolUse hook 在 Write/Edit 工具调用前检查 lock

```bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
echo "$TOOL" | grep -qE '^(Write|Edit)$' || exit 0

FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // ""')
[ -z "$FILE" ] && exit 0

# 生成 claim 文件名（路径中的 / 替换为 _）
CLAIM_NAME=$(echo "$FILE" | sed 's|/|_|g')
CLAIM_FILE=".claims/${CLAIM_NAME}.lock"

if [ -f "$CLAIM_FILE" ]; then
  OWNER=$(jq -r '.session_id' "$CLAIM_FILE")
  EXPIRES=$(jq -r '.expires_at' "$CLAIM_FILE")
  NOW=$(date +%s)
  
  # 检查是否过期（默认 10 分钟）
  if [ "$NOW" -lt "$EXPIRES" ] && [ "$OWNER" != "$SESSION_ID" ]; then
    echo "{\"decision\":\"deny\",\"reason\":\"文件 ${FILE} 已被 session ${OWNER} 锁定，请等待释放或处理其他任务。\"}"
    exit 0
  fi
fi

# 创建或更新 claim
mkdir -p .claims
EXPIRES_AT=$(( $(date +%s) + 600 ))  # 10 分钟过期
jq -n --arg sid "$SESSION_ID" --arg file "$FILE" --argjson exp "$EXPIRES_AT" \
  '{session_id: $sid, file: $file, claimed_at: now | todate, expires_at: $exp}' \
  > "$CLAIM_FILE"
```

2. 编辑完成后释放 lock（PostToolUse hook 或 agent 手动删除）

```bash
rm -f "$CLAIM_FILE"
```

3. 定期清理过期 lock（cron 或 daemon）

```bash
find .claims -name "*.lock" -mmin +15 -delete
```

## Tradeoffs

- **Pro**: 防止并发编辑冲突，简单有效
- **Pro**: 超时机制防止 crash 导致的永久死锁
- **Con**: 粒度是整个文件——两个 agent 改同一文件的不同部分也会冲突
- **Con**: Agent 可能长时间持有 lock（在做复杂修改时），阻塞其他 agent

## Source

OMC Swarm 的文件锁定机制。经典的 advisory file locking 模式，适配到 agent 场景。
