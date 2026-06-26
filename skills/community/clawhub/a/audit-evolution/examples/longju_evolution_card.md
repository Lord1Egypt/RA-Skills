# Longju Evolution Card 示例

这是基于 Longju SACP Operator 路径整理的公开安全示例。

```yaml
agent_id: Longju
input_type: benchmark_report_and_receipts
score_delta:
  earlier: 84.0
  latest: 93.0
  gain: 9.0
trusted_evidence:
  - public benchmark screenshot
  - benchmark-result-authority
  - benchmark-brief-latest
weak_dimension:
  - act
  - memory
  - perceive
minimal_patch:
  type: scoring_pattern
  target: six-core-skill scan visibility
  instruction: expose action, memory, and perceive answer skeletons in top-level scan-visible fields
promotion_gate:
  - node syntax check
  - scan dry-run
  - payload audit
  - receipt
  - one approved benchmark only
```

## Field Note

Longju 不是靠换更大的模型变强，而是靠状态、证据、停止规则和 skill patch 变得可复用。

下一步修复应该聚焦：一次只做一个最小补丁，验证后再晋升。
