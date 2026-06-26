# Jobs Evolution Card 示例

这是基于 Jobs 跑分路径整理的公开安全示例。

```yaml
agent_id: Jobs
input_type: benchmark_history
score_delta:
  first: 76.4
  second: 78.8
  best: 88.8
  total_gain: 12.4
trusted_evidence:
  - public benchmark screenshot
  - local benchmark guide
weak_dimension:
  - act_config
  - autonomy_config
minimal_patch:
  type: answer_pattern
  target: act and autonomy config visibility
  instruction: add explicit idempotency, monitoring thresholds, degraded mode, RTO/RPO, and human escalation triggers
promotion_gate:
  - dry_run answer JSON parse
  - field note
  - one approved benchmark only
```

## Field Note

Jobs 从 `76.4` 提升到 `88.8`。关键不是继续堆很多 skill，而是把 benchmark feedback 转成结构化答题范式。

下一步修复应该聚焦：让 act / autonomy 的装备能力更可见、更可测试。
