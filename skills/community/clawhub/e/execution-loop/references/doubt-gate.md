# Pattern 1.2: Doubt Gate（投机检测断路器）

## 问题

Agent 声称任务完成，但回答中包含投机性语言——"可能是"、"我认为"、"大概"——没有提供具体证据。这和 Pattern 2.2（权限否决追踪）解决的是相反的问题：Pattern 2.2 处理 agent 被拒绝后换表述重试，Doubt Gate 处理 agent 以不确定的态度"完成"任务。

来源：`johnlindquist/plugin-doubt-gate`

## 原理

Stop hook 在 agent 尝试结束时，strip 代码块和引用块后扫描剩余文本中的 hedging 关键词（"likely"、"maybe"、"might"、"probably"、"not sure"、"I think"、"I believe"、"可能"、"大概"、"也许"、"应该是"）。如果匹配到，返回 `{"decision":"block"}`，强制 agent 回到活跃状态，必须提供具体证据（日志、断言、测试运行结果）才能再次尝试停止。

### 防止无限循环

设置 `stop_hook_active` 守卫标志。如果本轮已经触发过一次 doubt gate，下次 stop 无条件放行。防止 agent 永远无法停止。

## 实现

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "bash scripts/doubt-gate.sh"
      }]
    }]
  }
}
```

```bash
# doubt-gate.sh — 核心逻辑
INPUT=$(cat)
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""')
# Strip code blocks and blockquotes
PROSE=$(echo "$LAST_MSG" | sed '/^```/,/^```/d; /^>/d')
# Check for hedging keywords
if echo "$PROSE" | grep -qiE 'likely|maybe|might|probably|not sure|I think|I believe|可能|大概|也许|应该是'; then
  # Check guard: already fired this turn?
  GUARD_FILE="$TMPDIR/doubt-gate-${SESSION_ID}"
  if [ -f "$GUARD_FILE" ]; then
    rm -f "$GUARD_FILE"
    echo '{"continue":true}'
  else
    touch "$GUARD_FILE"
    echo '{"decision":"block","reason":"Your response contains speculative language. Provide concrete evidence (logs, test results, or code verification) before completing."}'
  fi
else
  echo '{"continue":true}'
fi
```

## 与 Ralph 的关系

Ralph 阻止 agent 过早停止（基于迭代计数）。Doubt Gate 阻止 agent 以不确定的方式停止（基于内容分析）。两者可叠加：Ralph 在前（决定是否继续迭代），Doubt Gate 在后（即使 Ralph 允许停止，如果内容有投机语言也会 block）。

## Tradeoff

- 可能误报——agent 在解释可能性时使用"可能"是合理的
- 需要 strip 代码块，否则代码注释中的 hedging 词会误触发
- 守卫标志防止无限循环，但意味着 agent 第二次尝试时即使仍然投机也会被放行
