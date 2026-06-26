# Pattern 6.3: Hook Pair Bracket（每轮测量框架）

## 问题

无法知道每一轮 agent 交互消耗了多少 context、用了多长时间、调用了哪些工具。

## 原理

用 UserPromptSubmit + Stop 两个 hook 构成一个测量"括号"，在每轮前后采集数据。来自 claude-howto 的 context-tracker 示例——用 session-id 为 key 的临时文件在两个 hook 之间共享状态。

## 实现

**UserPromptSubmit hook（"before"）**：
```bash
# 记录轮次开始状态
# 注意：Claude Code 不提供 CONTEXT_USAGE 环境变量
# 需要通过 transcript 尾部读取获取（见 agent-ops/context-usage.sh）
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // ""')
# context-usage.sh 输出 "Input tokens: NNNNN"（无百分比——context_window_size 不可用）
CTX=$(bash context-usage.sh "$TRANSCRIPT" 2>/dev/null | grep -o '[0-9]*$' || echo "0")
jq -n --arg ts "$(date +%s)" --arg ctx "$CTX" --arg sid "$SESSION_ID" \
  '{start_ts: $ts, start_ctx: $ctx, session_id: $sid}' > "$TMPDIR/bracket-${SESSION_ID}.json"
```

**Stop hook（"after"）**：
```bash
# 读取开始状态，计算本轮增量
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // ""')
BRACKET_FILE="$TMPDIR/bracket-${SESSION_ID}.json"
[ -f "$BRACKET_FILE" ] || exit 0
START=$(cat "$BRACKET_FILE")
ELAPSED=$(( $(date +%s) - $(echo "$START" | jq -r '.start_ts') ))
# context-usage.sh 输出 "Input tokens: NNNNN"
CUR_CTX=$(bash context-usage.sh "$TRANSCRIPT" 2>/dev/null | grep -o '[0-9]*$' || echo "0")
START_CTX=$(echo "$START" | jq -r '.start_ctx')
CTX_DELTA=$(( CUR_CTX - START_CTX ))
echo "Turn: ${ELAPSED}s, context delta: ${CTX_DELTA} tokens"
```

## 用途

- **Context 预算**：当单轮 context 增量 > 阈值时告警（"这一轮用了 30K token，可能有大文件被读入"）
- **工具统计**：哪些工具被频繁使用/失败
- **进度追踪**：第 N 轮，已用 X% context
- **与 Ralph 叠加**：先 bracket 记录数据，再 ralph 决定是否 block

## 与 Ralph 的关系

Ralph 的 Stop hook 决定"是否阻止停止"。Hook pair bracket 不阻止，只测量和记录。两者可叠加——在 settings.json 的 Stop hooks 数组中，bracket 在前（记录数据），ralph 在后（决定是否 block）。

## 状态文件

临时文件 `$TMPDIR/bracket-${SESSION_ID}.json`（不在 sessions/ 下，因为这是轮次级别的瞬态数据）。

聚合统计可以写入 `sessions/<session-id>/bracket.json`（累计数据，供外部监控读取）。
