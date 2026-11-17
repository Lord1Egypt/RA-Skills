# 分阶段交付、证据门禁与 v0.0.5 迁移

阶段由目标与当前可得证据决定。小范围用例可独立完成；不必先补完整个企业模型。用户已有交付要求和授权优先，不机械增加固定用例数量或签署流程。

| 阶段 | 最小充分交付 | 完成判断 |
| --- | --- | --- |
| S0 | 目标问题、消费者、输入与边界 | 相关人知道本次要回答/支持什么 |
| S1 | 来源、候选解释、缺口、确认记录 | 阻断本用例的语义决定已有依据；未知项明确 |
| S2 | 模型、映射、约束、预期 | 结构可检查；业务可审阅；无法执行的部分明确 |
| S3 | 模型/用例/快照绑定的检查与回归 | 已验证范围可复跑；失败与未知不混入成功 |
| S4 | 字典、模型、用例、证据、manifest | 目标消费者能读入并达到约定行为，转换损失说明 |
| S5 | 上游差异、影响候选、重新确认与回归 | 当前结论仍绑定有效版本，不沿用失效证据 |

业务负责人决定业务口径，PM 组织澄清与验收（有授权才代定）；信息中心负责来源、结构、时效和访问规则；FDE 实现映射与检查。技术报告不能自行转移业务责任。`impact_analysis` 的文本依赖匹配属于影响候选，需核对真实消费者。

## 门禁 profile

| Profile | 必需证据 | 结论范围 |
| --- | --- | --- |
| static | 模型 lint、gold lint；如提供 session 则检查匹配与阻断项 | static_ready；未执行数据验证 |
| validated（默认） | static 检查 + 完整评测报告 + 当前 SQLite 快照 + 非空约束集 + 关系/查询路径检查 | validated_mock / validated_offline / validated_live |
| production | validated + 同一 endpoint 的 live 报告 + 当前端点计划稳定抽查 | 生产技术门禁结果；不等于业务或上线验收 |

`pass`、`waived`、`not_applicable`、`unknown`、`fail` 分别统计。未提供必需项时为 not_ready，不能计算成“全部通过”。约束和查询报告中的 error/not_ready 也阻断门禁。默认报告最长有效时间为 24 小时，可用 `--max-age-hours` 明确调整；时间范围之外、文件哈希变化、快照变化必须重验。

`--min-acc` 默认 1.0；如明确调整阈值，门禁仍要求用例逐条有判定、覆盖完整，拒答用例全过。SQL-only 用例没有期望行时为 unknown。`--multihop`/`--results` 必须与生成评测报告时相同。开启补齐流程的项目应持续传 `--session`，避免语义阻断项被遗漏。

`--db` 的指纹包含 SQLite 一致快照（包含已提交 WAL 数据）。它绑定测试输入，但无法自行证明远端服务当时用了同一份数据库；生产需另有数据来源与部署版本证据。快照在内存复制，面向可放入内存的本地验证库；大型库应使用受控快照与专门的数据引擎。

## v0.0.4 迁移

1. 原 `datasets/concepts/relationships/metrics` 和同名 `join_key` 继续读取。复合或异名键改用 `from_columns`/`to_columns`；消费者是否支持新字段需分别验证。
2. 老评测报告没有 evidence 绑定时，保留作历史记录，不能用于 v0.0.5 验证门禁。重跑 `run_eval --model ... --db ...`；离线报告现在也包含统一 summary/evidence，仍保留旧顶层计数字段。
3. 原来缺 `--eval-report` / `--endpoint` 也可能输出“通过”。现在缺报告默认失败；仅做静态检查应显式 `--profile static`。这不是生产兼容保证。
4. `declared_conflict` 需要 ref、note、owner、expires_on、case_ids。无效或过期声明不再移出失败分母。有效豁免只接受当前具体用例，门禁显示 with_waivers；拒答失败不能豁免。
5. 跨表/未知前缀不会再被编译器去掉。为多表指标提供经验证的单表/视图 source 或交给目标引擎；不能将编译拒绝解释为模型必然错误。
6. SQL 错误、不支持编译、NULL 未定义、空指标集会使直算检查非零退出；×100 量纲差异需要确认后重验，不自动视为语义一致。无 endpoint 的 computed_only 仍不是双路一致。
7. 交换目录必须为空，避免混入旧文件。YAML 用例保留 `.yaml` 后缀；旧消费者若写死 `cases.json` 需迁移。

有效豁免示例（期限和责任主体必须来自实际决定，不要照抄）：

```yaml
declared_conflict:
  ref: DECISION-123
  note: 已确认的暂存差异及影响
  owner: 已获授权的责任人
  expires_on: '2026-10-15'
  case_ids: [CASE-123]
```

`mocks/finance` 使用长期限合成声明只用于演示，不是生产豁免政策。没有真实决议时不要给旧声明补一个虚构 owner 或未来期限来消除失败。

## 交换与巡检

`export_exchange` 输出模型、字典、可选用例/会话/证据/视图与 SHA256 清单，报告必须绑定当前模型且未过期。报告失败也可以作为事实交付；manifest 的 exported_not_certified 不把“成功导出”升级为“验证通过”。HTML 是附属视图，审阅应以模型、证据和 manifest 为准。

结构巡检用 `check_consistency`；数据规则重跑 `check_constraints`；关系/粒度重跑 `check_join_graph`；结果用独立预期对拍，再生成当前视图。语义图和物理 source 映射不代表实际作业运行，实时链路需要后续接入运行事件。
