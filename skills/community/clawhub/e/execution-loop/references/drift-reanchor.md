# Drift Re-anchoring

## Problem

Agent 在长会话中逐渐偏离原始任务。第 1 轮还在做需求分析，第 5 轮开始"顺手"重构不相关代码，第 10 轮已经在优化 CI 配置。这种 drift 在 Ralph 持续执行中更严重——因为 agent 不停，drift 没有天然的修正点。

## Solution

Stop hook 每 N 轮（默认 10 轮）将原始任务描述重新注入对话，作为"锚点"。在 Ralph 持续执行模式中，每次 Stop hook 触发时计数 +1，每 N 次注入一次 re-anchor 消息。

## Implementation

1. 任务启动时将原始 prompt 存入 `sessions/<session-id>/reanchor.json`
2. Stop hook 每次触发时递增 turn_count
3. 当 `turn_count % REANCHOR_INTERVAL == 0` 时通过 additionalContext 注入原始任务提醒
4. 注入结构化消息包含：原始任务、当前迭代数、已完成项（从 .harness-tasks.json 读取）
5. Hook 返回 `{"continue":true}` 放行，re-anchor 通过 hookSpecificOutput 注入

```bash
# Stop hook — 每轮触发，每 N 轮注入 re-anchor
INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

STATE_FILE="sessions/${SESSION_ID}/reanchor.json"
[ -f "$STATE_FILE" ] || { jq -n '{"turn_count":1,"original_task":""}' > "$STATE_FILE"; echo '{"continue":true}'; exit 0; }

TURN_COUNT=$(( $(jq -r '.turn_count // 0' "$STATE_FILE") + 1 ))
ORIGINAL_TASK=$(jq -r '.original_task // ""' "$STATE_FILE")
jq -n --arg task "$ORIGINAL_TASK" --argjson count "$TURN_COUNT" \
  '{"original_task":$task,"turn_count":$count}' > "$STATE_FILE"

INTERVAL=${REANCHOR_INTERVAL:-10}
if [ $((TURN_COUNT % INTERVAL)) -eq 0 ] && [ -n "$ORIGINAL_TASK" ]; then
  jq -n --arg ctx "TASK REMINDER (turn ${TURN_COUNT}): ${ORIGINAL_TASK}" \
    '{"hookSpecificOutput":{"additionalContext":$ctx}}'
else
  echo '{"continue":true}'
fi
```

## Tradeoffs

- **Pro**: 低成本防 drift，不需要 LLM 判断
- **Pro**: 与 Ralph、Task Completion 正交——三者各管一个维度
- **Con**: 频率过高会浪费 context（N 太小），频率过低可能来不及纠偏（N 太大）
- **Con**: 对于合理的任务拆分变化（发现 A 前必须先做 B），re-anchor 可能产生误导

## Source

OMC 的多模式持续执行系统中的"任务重注入"机制。Anthropic 博客提到的 coordinator synthesis 原则——agent 需要定期对照原始目标。
