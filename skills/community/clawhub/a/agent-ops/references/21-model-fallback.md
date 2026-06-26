# Pattern 21: Auto Model Fallback（自动模型降级/升级）

## 问题

Agent 使用的模型可能因为各种原因反复失败——API 容量不足（529）、模型能力不匹配（任务对 Haiku 太难）、或 token 限制。当前没有机制在失败后自动切换到更合适的模型。

来源：Claude Code 内部 `withRetry` 机制 + 官方文档 Sub-agents model field + StopFailure hook

## Claude Code 内部实现

Claude Code 的 `withRetry` 已经包含了模型 fallback：
- 429 错误：指数退避（500ms base, 32s max）
- 529 错误（容量不足）：前台任务重试，后台任务立即放弃（避免放大容量风暴）
- **3 次连续 529 后**：触发 `FallbackTriggeredError`，切换到备选模型

切换时的清理工作：
- 对孤立的 assistant 消息做 tombstone 标记
- 清除模型特定的 thinking signatures
- 重置 token 计数

## 实现

### StopFailure hook

> 注意：StopFailure 事件出现在 Claude Code 官方文档的 hook 事件列表中（"When the turn ends due to an API error"），但部分旧版 SDK type definitions 中可能未包含此事件。请在使用前用 `claude --help` 或官方文档确认当前版本是否支持。此外，hook 脚本**无法实际切换模型**——只能在 additionalContext 中建议 agent 使用不同模型（agent 可能不遵守）。

```bash
INPUT=$(cat)
ERROR=$(echo "$INPUT" | jq -r '.error // ""')
TRACKER="sessions/${SESSION_ID}/failure-tracker.json"

# 初始化或读取 tracker
if [ -f "$TRACKER" ]; then
  COUNT=$(jq -r '.consecutive_failures // 0' "$TRACKER")
  CURRENT_MODEL=$(jq -r '.current_model // "sonnet"' "$TRACKER")
else
  COUNT=0
  CURRENT_MODEL="sonnet"
fi

# 递增失败计数
COUNT=$((COUNT + 1))

# 模型升级链
NEXT_MODEL="$CURRENT_MODEL"
if [ "$COUNT" -ge 3 ]; then
  case "$CURRENT_MODEL" in
    haiku)  NEXT_MODEL="sonnet" ;;
    sonnet) NEXT_MODEL="opus" ;;
    opus)   NEXT_MODEL="opus" ;; # 已经是最高，无法升级
  esac
  if [ "$NEXT_MODEL" != "$CURRENT_MODEL" ]; then
    COUNT=0  # 重置计数
    echo "{\"hookSpecificOutput\":{\"additionalContext\":\"Model upgraded from $CURRENT_MODEL to $NEXT_MODEL after 3 consecutive failures.\"}}"
  fi
fi

# 写入 tracker
jq -n --argjson count "$COUNT" --arg model "$NEXT_MODEL" \
  '{consecutive_failures: $count, current_model: $model}' > "${TRACKER}.tmp"
mv "${TRACKER}.tmp" "$TRACKER"
```

### Subagent 级别的 fallback

在 subagent 定义中指定模型，失败后用更高级模型的 subagent 重试：

```markdown
---
name: analyzer-haiku
model: haiku
---
快速分析任务

---
name: analyzer-sonnet
model: sonnet
---
深度分析任务（haiku fallback）
```

Coordinator 先用 `analyzer-haiku`，失败后自动切换到 `analyzer-sonnet`。

## 模型选择策略

| 模型 | 适用场景 | Token 成本 |
|------|---------|-----------|
| Haiku | 快速搜索、简单读取、格式转换 | 最低 |
| Sonnet | 日常编码、bug 修复、代码审查 | 中等 |
| Opus | 复杂架构、安全分析、多文件重构 | 最高 |

## 与 Pattern 16（Adaptive Complexity）的关系

Pattern 16 在任务开始前根据复杂度选择执行模式。Pattern 21 在执行过程中根据失败反馈动态切换模型。两者互补：Pattern 16 做预判，Pattern 21 做运行时调整。

## Tradeoff

- 自动升级模型会增加成本——Opus 是 Haiku 的 ~60 倍价格
- 频繁切换模型可能导致风格不一致
- 需要区分"模型能力不足"和"任务本身有问题"——后者升级模型没用
