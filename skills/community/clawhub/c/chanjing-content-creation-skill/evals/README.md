# Evals（最小评测闭环）

本目录用于验证 `chanjing-content-creation-skill` 的路由准确率、契约一致性与链路可用性。

## 评测目标

1. 路由准确率：用户意图是否命中正确 L2/L3 子技能。
2. 语义一致性：是否按统一 `outcome_code` 语义返回。
3. 契约一致性：门控、依赖、副作用声明是否与实现一致。
4. 链路可用性：关键场景是否可端到端跑通（可用 mock 或 dry-run）。

## 建议指标

- `routing_accuracy`：>= 90%
- `outcome_semantics_coverage`：= 100%（5 个 code 都有测试样例）
- `contract_consistency_check`：= pass
- `critical_flow_pass_rate`：>= 90%

## 执行方式（人工或脚本均可）

1. 读取 `router-evals.jsonl`，逐条输入测试提示词。
2. 记录实际命中 skill 与返回语义。
3. 与样例中的 `expected_route`、`expected_outcome` 对比。
4. 输出评测报告（可简单用 markdown 表格）。

## 文件说明

- `router-evals.jsonl`：路由与错误语义样例集
