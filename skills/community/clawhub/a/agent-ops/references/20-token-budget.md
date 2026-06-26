# Pattern 20: Token Budget Per Subtask（子任务 token 预算）

## 问题

Agent 在处理复杂任务时，前半部分消耗了大量 context（读了太多文件），后半部分 context 不够用，被迫压缩丢失关键信息。没有机制在执行前预估和控制每个子任务的 context 消耗。

来源：Claude Code 官方文档 Context Window + Best Practices

## 原理

在 UserPromptSubmit hook 中估算当前 context 使用量，注入预算感知指令。当 context 接近阈值时，提醒 agent 使用 subagent 委托（subagent 有独立 context window）或触发主动压缩。

## Claude Code 官方建议

> "Claude's context window fills up fast, and performance degrades as it fills." 这是需要管理的最重要资源。

三个官方工具：
- `/context`：实时查看各类别的 context 占用
- `/compact`：手动触发压缩，用结构化摘要替换会话历史
- Subagent：每个有独立 context window，结果以摘要形式返回

## 实现

### UserPromptSubmit hook

```bash
# 从 hook 输入获取 transcript 路径（UserPromptSubmit hook 提供 transcript_path）
INPUT=$(cat)
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // ""')
if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
  # context-usage.sh 输出 "Input tokens: NNNNN"（原始 token 数，非百分比）
  # 因为 Claude Code 不在 transcript 中暴露 context_window_size
  INPUT_TOKENS=$(bash context-usage.sh "$TRANSCRIPT" | grep -o '[0-9]*$')
  if [ -n "$INPUT_TOKENS" ]; then
    # 粗略阈值：200K context window 的 80% ≈ 160K tokens
    if [ "$INPUT_TOKENS" -ge 160000 ]; then
      jq -n --arg ctx "WARNING: Input tokens at ${INPUT_TOKENS}. Context is heavily loaded. For remaining work: 1) Use subagents for file-heavy tasks 2) Avoid reading entire files, use targeted grep 3) Consider /compact if quality is degrading." \
        '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":$ctx}}'
    elif [ "$INPUT_TOKENS" -ge 120000 ]; then
      jq -n --arg ctx "Input tokens at ${INPUT_TOKENS}. Budget remaining work carefully — prefer grep over full file reads." \
        '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":$ctx}}'
    fi
  fi
fi
```

## 预算分配策略

| Context 使用率 | 策略 |
|---------------|------|
| < 40% | 自由读取，无限制 |
| 40-60% | 提醒 agent 注意读取量 |
| 60-80% | 注入"优先用 grep/subagent"指令 |
| 80-95% | 注入"必须用 subagent 委托，不要直接读大文件" |
| >= 95% | Ralph MUST 放行 stop（Pattern 1 安全阀） |

## 与 Pattern 5（Context 估算）的关系

Pattern 5 提供了底层的 context 使用量检测能力。Pattern 20 在此基础上做决策和干预——不只是"知道用了多少"，而是"根据用量调整行为"。

## Tradeoff

- 估算不精确——bytes/4 是粗估，实际 token 数可能偏差 20-30%
- 过早限制可能降低工作质量——agent 被迫用 grep 而不是读全文，可能遗漏上下文
- Subagent 委托引入延迟——每次委托需要额外的 API 调用
