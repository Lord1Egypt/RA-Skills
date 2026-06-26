# Session-Scoped State Layout

所有状态统一在一个 session 目录下，清理只需 `rm -rf` 一个目录。

## 目录结构

```
sessions/<session-id>/
  ralph.json              ← 1.1 Ralph persistent loop
  cancel.json             ← 1.1 Cancel signal (30s TTL)
  reanchor.json           ← 1.5 Drift re-anchoring
  handoffs/               ← 3.1/3.2 Handoff 文档
    stage-1-plan.md
    pre-compact-*.md
  tool-errors.json        ← 2.1 Tool error escalation
  denials.json            ← 2.2 Denial circuit breaker
  bracket.json            ← 6.3 Hook pair bracket
  compaction-extract.json ← 3.2 Compaction extract counter
  .doubt-gate-fired       ← 1.2 Doubt gate one-shot guard
  .harness-tasks.json     ← 1.4 Task completion checklist
```

## 设计原则

1. **清理简单**：一个 `rm -rf` 搞定
2. **无跨 session 污染**：不可能读到其他 session 的状态
3. **Crash 恢复简单**：检查目录是否存在就知道有没有残留状态
4. **Staleness 检查**：目录的 mtime 反映最后活动时间

建议严格 session-scoped，不做 fallback。
