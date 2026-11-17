# v0.0.7 合同与可执行边界

`semantic.yaml` 延续 datasets/concepts/relationships/metrics，v0.0.6 新增可选 `ontology` 段；v0.0.7 新增可维护性字段（uid/evidence/domain，见下）。模型本身的 version 与 skill 版本分别管理。新增字段保持增量，但下游是否忽略/拒绝/正确执行要在实际消费者验证。

## 本体声明层与合同投影

`ontology` 段承载**业务世界本身**的声明：业务对象（可以还没有表）、对象属性、语义关系（谓词 + 落地方式）。它是声明式事实清单，不做 is-a 传递、子类继承或 OWL/SHACL 逻辑推理。同一显式关系可以反向查看和检查路径，不另维护一份逆关系；新增业务事实仍须有依据，反向一对多需重新判断聚合重复。已有表/关系的复用与 Agent 消费见[完整路径](metadata-to-consumption.md)。

```yaml
ontology:
  entities:
    - name: 借款人
      uid: ent_borrower            # v0.0.7：稳定身份，重命名后 drift 可追踪；缺省以 name 为身份（W12）
      domain: 信贷                  # v0.0.7：主题域，可视化按域过滤
      evidence: {source: user_provided}   # v0.0.7：证据来源 ∈ user_provided/data_observed/model_inferred/owner_confirmed
      attributes: [{name: 风险等级, value_type: enum, values: [低, 中, 高]}]
    - name: 担保人
      unprojected_reason: 担保台账未结构化，仅业务声明   # 未投影必须说明
  relations:
    - {id: rel_borrower_loan, from: 借款人, to: 贷款, predicate: 申请, mapping: equi_key}
    - {from: 担保人, to: 贷款, predicate: 担保, mapping: weak, note: 依赖人工台账}
```

- 实体：`name` 唯一；`uid` 是稳定身份（建议 `ent_xxx`，重命名不改 uid）；`is_a` 只能指向已声明实体且不得成环（环检测是结构检查，不是推理）。**`is_a` 仅做分类声明：无属性继承、无类型推导**——子类需要的属性必须显式写全，需要"子类必有父类属性"这类结论时请逐条声明，不要假设系统会继承；`attributes` 是业务属性（name/value_type/unit/values/note），不依赖具体表。
- 关系：`predicate`（语义谓词）是核心，`mapping ∈ equi_key/weak/derived/semantic_only` 是落地方式；**键只是落地方式之一**，`mapping≠equi_key` 必须写 `note`。建议显式 `id`（`rel_xxx`）使重命名后引用稳定。无键关系留在本体里，不得因为"没有外键"被移出。
- 投影：datasets/relationships 是本体在物理来源上的**合同投影**，用 `ontology_ref` 回指；回指关系时用其稳定 `id`。合同只承载 `equi_key` 关系；`ontology_ref` 指向无键关系是 ERROR（E15）。投影损失（本体有而合同表达不了的）必须留在本体侧并说明，不得静默丢弃。
- 兼容：无 `ontology` 段的模型不受新规则约束；声明了 `ontology_ref` 却无 `ontology` 段是 ERROR（E14）。

## 模型维护（v0.0.7）

- **drift 对比**：`check_model.py -f 当前.yaml --drift 基线.yaml` 输出新增/删除/变更/破坏四级分类。破坏 = 删除仍被引用的对象、主键/粒度变更、equi_key 关系降级、实体重命名但投影未跟随（uid 保住身份、引用要跟着改）。存在破坏即退出码 1。
- **质量历史**：`--history quality_history.jsonl` 每次追加一条 ERROR/WARN 记录；`visualize_model.py --history` 渲染趋势图。release 时各跑一次，WARN 应随版本收敛。
- **冷启动包**：`guide_model.py init --pack starter_packs/<领域>.yaml` 先把模板本体合并进模型（已有对象不覆盖），再走正常补齐；合并结果记入会话 `packs_applied`。

概念层同时扩充词表属性：`synonyms`（同义说法）、`forbidden`（禁用说法，不得与自身 term/synonyms 冲突）、`domain`（业务域，同域内 synonym 不得被两个概念认领）、`owner`、`valid_from/valid_to`（过期需复审）。概念仍需 `expand` 可执行展开才准发布；`is_a` 层级写在 ontology 实体上，概念保持词与宏的定位。

## 身份、来源、关联与粒度

dataset 使用 name 作本合同内稳定引用，metric 用 id，concept 用 term；有多个语义关系或左右异名键时显式给 relationship.id。物理 source 当前是 SQLite 表/视图名；字段以同名映射执行，没有任意跨库/列重命名映射执行器。需要重命名时建视图或在消费者侧实现并验证。

```yaml
relationships:
  - id: order_customer
    from: orders
    to: customers
    from_columns: [tenant_id, customer_ref]
    to_columns: [tenant_id, customer_id]
    cardinality: 'N:1'
    traversable: true
query_plans:
  - id: gmv_by_customer
    metric: gmv
    relationships: [order_customer]
```

同名键仍可写 `join_key: customer_id` 或列表。基数支持 `1:1/N:1/1:N/N:M`。验证双侧列存在，数据快照检查声明为“一”侧的复合键唯一且非空；没有 DB 时不声称已证明唯一。N:M 没有“一”侧，不能据此称关联安全。

query_plans 从 metric.dataset 的行粒度出发，按显式关系 ID 逐跳检查（可正向或反向）。走向多侧报告 fanout；走向一侧仍需唯一性证据。字段别名、自连接和回到已访问数据集的路径当前不支持。整个模型图存在环不自动报错；多条业务可选路径必须由当前 query_plan 明确选择，不自动择路。

图检查证明的是指定关联对原始粒度是否有重复风险，不证明 INNER JOIN 不丢数据、NULL 关联政策、特定指标可加性或跨表计算正确。引用覆盖另用 referential 约束；需要保持未匹配行时由业务确认 LEFT JOIN/缺省维度处理并做独立对拍。策略字段只是建议，不能消除风险状态。

## 数据约束

顶层 constraints 的每条规则需要唯一 id、kind、dataset、columns（单列可 field）和显式 null_policy。支持：

| kind | 参数 | 检查 |
| --- | --- | --- |
| unique | columns | 非 NULL 复合键的重复；按多出的记录计数 |
| not_null | columns；null_policy=forbid | 任一指定列为空 |
| allowed_values | 单 field + 非空 values | 值不在集合 |
| range | 单 field + min/max 至少一个 | 数字范围（闭区间）；文本值不当数字通过 |
| date_order | columns: [earlier,later] | SQLite julianday 可解析且先后成立 |
| referential | references: {dataset,columns} | 非 NULL 源键在目标表有匹配 |

null_policy：forbid 把 NULL 计入违规；ignore 明确排除 NULL；unknown 发现 NULL 后不能宣布通过。没有数据或没有规则不算验证成功。日期检查遵循 SQLite 的日期解析，不是严格 ISO 格式、时区或业务日历验证；需要更严格语义时应增加专用消费者检查。

报告统计整个一致快照，默认不导出任何数据行，避免在质量报告内泄露敏感样本。违反约束为 fail；缺定义/不支持为 unknown；SQL 执行失败为 error。父状态只有所有已声明约束 pass 才为 pass。未知数据类型、外部系统、新鲜度、权限规则本版不执行，不能当隐式已通过。

## 指标与评测

本地共享编译器只处理单 source，支持 expr 或 numerator/denominator、filters、extra_where。有分母的指标用 `on_zero_denominator` 显式声明除零策略：`null`（缺省，NULLIF 返回 NULL）、`zero`（COALESCE 归 0）、`error`（SQLite 除零不报错，编译为哨兵文本 `ZERO_DENOMINATOR`，数值比对必失败，除零无法静默通过）；缺声明 lint 告警（W11），非法值编译拒绝。任何策略下都不能宣称结果已验证。未知/跨表前缀、join_path、子查询、SQL 注释、多语句、分组/窗口等拒绝编译；字符串字面量不会被去前缀修改。它不是通用 SQL 解析器或安全执行平台，仅用于受控本地模型片段。

评测用例可附 `answer_must_not_contain: [禁用词…]`：答案值/行集/SQL 中命中任一禁用词即判失败（来源通常是概念 `forbidden`，用例需显式列出，评测器不自行从模型推导）。

全量检查通过也只代表已声明规则。业务口径正确性需要独立确认的期望；从同一生成器输出实际值和期望值的自证不足。原有 ratio 禁 AVG 的 lint 仍保留；确有行均值业务语义时应建独立指标类型并明确期望，不用强制把所有平均都改成加权比率。

## 明细查询模板（templates，v0.0.9）

真实项目实测约半数问数需求是"给我列出来"而非聚合数字——明细查询是一等资产，不挤进 metrics。顶层 `templates` 段逐条声明：

```yaml
templates:
  - id: refund_orders          # 稳定 id，drift 追踪身份
    name: 退款订单明细
    dataset: 订单              # 挂载数据集 name（必须已声明）
    columns: [order_id, customer_id, amount, stat_date]   # 物理列，必须存在于数据集字段
    extra_where: "status = '已退款'"   # 可选：固定过滤（同指标 extra_where 语义）
    time_field: stat_date      # 明细也必须时间围栏，缺省 lint 告警（W18）
    synonyms: [退款单列表, 哪些订单退款了]   # 命中路由，<3 告警（W18）
    note: 按 stat_date 倒序，默认最多 100 行
    status: 草案               # 草案|已发布|停用
```

lint 校验：id 重复、dataset 未声明、columns/time_field 引用不存在字段均为 ERROR（E18）；缺 time_field 或 synonyms<3 为 WARN（W18）。模板只声明"哪个数据集、哪些列、什么固定过滤"，执行层负责分页/排序/脱敏，模型不承载行级安全策略。promote_draft.py 把 list/rank 类盘点指标自动产出为本段草稿（`columns_raw` 待映射伪代码列，人审改成物理列后才算数）。

## 报告身份与交换

evidence 保存 created_at、mode、model_sha256、cases_sha256 和适用的 data_snapshot_sha256/actual_sha256/gold_results_sha256/multihop_sha256。哈希绑定内容而非宣告来源可信，不是电子签名或防篡改审计服务。角色与来源权限仍由操作者核对。

交换包包含模型、字典、用例、可选会话/报告/HTML 和 manifest；清单逐文件绑定 SHA256。HTML 可搜索、筛选、查看属性/来源与决策，所有输入通过 textContent 展示；失配或过期证据显示失效。它展示设计声明和已有验证结果，未采集作业、请求或运行事件。
