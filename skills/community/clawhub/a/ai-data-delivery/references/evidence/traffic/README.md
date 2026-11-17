# 交通安全真实项目回迁证据（结构级）

本目录是 README 与验证记录中"交通安全真实项目回迁"主张的**可审计证据**，对应
`references/v0.0.7-validation.md` 中的 offline 级结论。

## 文件与来源

| 文件 | 内容 | 生成命令（在项目环境内运行） |
| --- | --- | --- |
| `join_graph.json` | 16 条合同关系的键与扇出检查，全部 pass（含唯一性实证：行数/空值/重复组） | `check_join_graph.py --model semantic.yaml --db physical.db --out join_graph.json` |
| `constraints.json` | 17 条 SQLite 全量快照约束，全部 pass（unique/not_null 等，含 NULL 策略与全量扫描标记） | `check_constraints.py --model semantic.yaml --db physical.db --out constraints.json` |
| `quality_history.jsonl` | `check_model.py --history` 的质量趋势记录（0 ERROR / 12 WARN 时刻快照） | `check_model.py -f semantic.yaml --history quality_history.jsonl` |

## 脱敏说明

- 表名/键名与 `starter_packs/traffic.yaml` 公开的本体声明一致，无新增暴露面。
- 文件只含结构检查与行数统计，**不含任何业务记录内容**。
- 完整 `semantic.yaml`（94 个指标的业务口径）属项目方资产，未公开；
  本体声明部分以 starter pack 形式公开（16 实体 / 18 关系）。
- 若需复核完整证据链，请联系作者安排受控查阅。

## 证据级别

offline（离线快照实证）。不证明：生产环境实时血缘、在线问数引擎行为、国标符合性。
