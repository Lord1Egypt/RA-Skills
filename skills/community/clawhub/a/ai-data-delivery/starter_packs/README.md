# starter_packs/ — 冷启动本体模板包

建模不从白板开始：先选一个与业务最接近的包，把它的本体声明合并进模型，
再在补齐会话里确认、裁剪、扩展。包内实体带稳定 `uid`、证据来源示例与属性清单，
关系带落地方式（mapping）；投影到物理表的做法见 `references/contract.md`。

## 用法

```bash
python scripts/guide_model.py init --model partial.yaml --scope scope.yaml \
    --session session.json --pack starter_packs/general.yaml --pack starter_packs/traffic.yaml
```

- `--pack` 可重复；按顺序合并，**已存在的对象（按 uid/name/id 判定）不覆盖**，你的模型永远优先。
- 合并结果记入会话 `packs_applied`（来源可追溯），随后走正常补齐流程。

## 包清单

| 包 | 领域 | 规模 | 来源 |
| --- | --- | --- | --- |
| `general.yaml` | 通用（组织/人员/地点/时间） | 4 实体 3 关系 | 对齐 GB/T 48000.3 概念层与 schema.org |
| `traffic.yaml` | 道路交通安全 | 16 实体 18 关系 | 真实项目回迁脱敏（references/v0.0.6-validation.md） |
| `retail.yaml` | 零售电商 | 2 实体 1 关系 | mocks/retail 合成场景 |
| `finance.yaml` | 银行信贷风控 | 3 实体 2 关系 | mocks/finance 合成场景 |
| `government.yaml` | 政务民生服务 | 2 实体 1 关系 | mocks/government 合成场景 |
| `healthcare.yaml` | 医疗门诊运营 | 2 实体 1 关系 | mocks/healthcare 合成场景 |
| `manufacturing.yaml` | 制造设备与生产 | 2 实体 1 关系 | mocks/manufacturing 合成场景 |
| `higher_vocational_diagnostic.yaml` | 高职质量诊改 | 7 实体 5 语义关系 | 脱敏抽象的演示形态；状态机/政策/统计口径由项目方确认 |

高职质量诊改与本科审核评估属于不同的业务范围，应从分别核实适用要求开始，不合并其规则或评价口径。领域 starter pack 仅提供可审阅的候选实体和关系；没有键的关系默认 `semantic_only`，不会自动变成查询关联。

## 写自己的包

任意包含 `pack` 元信息与 `ontology.entities/relations` 的 YAML 都是合法包：
实体建议带 `uid`（重命名后 drift 可追踪）、`attributes`、`evidence.source`；
无键关系写 `mapping: weak/derived/semantic_only` 加 `note` 落地说明。
把你的行业包贡献回社区：提 PR 到 <https://github.com/franklinxkk/ai-data-delivery>。
