# Progress Scoring and Weak-Point Memory

Use this reference to keep scoring stable and weak-point memory actionable.

## 1) Weak-Point Priority Formula

Compute priority score:

`Priority = 0.4 * frequency_7d + 0.4 * severity + 0.2 * recency_weight`

- `frequency_7d`: number of occurrences in last 7 days
- `severity`: 1-5 (red-line errors = 5)
- `recency_weight`: 1-3 (today=3, 2-3 days=2, 4-7 days=1)

Priority tiers:

- `>= 4.0`: 高
- `>= 2.5 and < 4.0`: 中
- `< 2.5`: 低

## 2) State Transition

1. New weak point -> `未修复`
2. One targeted correction + one pass retest -> `修复中`
3. Two consecutive pass retests -> `已稳定`
4. Any recurrence after stabilization -> revert to `未修复`

## 3) Weekly Review Output

```text
| 薄弱点 | 频次(7d) | 严重度 | 优先级分数 | 状态 | 本周动作 |
|---|---:|---:|---:|---|---|
```

## 4) Session-End Contract

After each test, always output three tables in order:

1. Single-test score table
2. Weak-point memory table
3. Progress trend table
