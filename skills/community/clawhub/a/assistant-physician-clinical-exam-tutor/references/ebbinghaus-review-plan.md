# Ebbinghaus Rolling Review Plan

Use this for countdown-based rolling revision.

## Inputs

1. 距考试天数
2. 错题池知识点与近7天错误频次
3. 每日可学习时长

## Output Table

```text
| 知识点 | D0 | D1 | D3 | D7 | D14 | D30 | 当前掌握度 | 下次优先级 |
|---|---|---|---|---|---|---|---:|---|
| 心衰分型与用药 | 精学45m | 快速回顾20m | 题组训练20m | 混合复盘15m | 错题回放15m | 终局压缩10m | 58% | 高 |
```

## Scheduling Rules

1. 距考试 <= 30天: compress cadence to D0/D1/D3/D7.
2. 距考试 <= 14天: daily mixed review, prioritize high-risk errors.
3. Any red-line error repeats next day regardless of cadence.
4. Daily first block always assigned to highest-priority weak node.
