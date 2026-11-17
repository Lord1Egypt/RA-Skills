# 从部分材料到可审阅的语义合同

自动发现缺字段只能覆盖一部分语义问题。Agent 需要先阅读当前用例和材料，给出“我理解的实体/粒度/计算规则、依据、尚不确定的点”，再生成会话。业务关键答案不能由语言模型自己确认。

## 入口与状态

只有 DDL 时，`ingest_ddl --model-out partial.yaml` 可生成部分模型。当前解析器覆盖常见 MySQL/SQLite CREATE TABLE（单行/多行字段、内联或复合主键、常见字段类型），不执行 DDL，不推断外键关系或业务粒度。复杂方言、schema 限定名、ALTER TABLE、转义等需人工核对解析台账，不能默认完整导入。

已有模型直接复用。scope 只引用当前用例用到的数据集和指标，不把缺少全企业覆盖视为阻塞。示例：

```yaml
id: loan_current_overdue
question: 当前逾期贷款有多少笔？
datasets: [loans]
metrics: [overdue_count]
time_requirement: current
required:
  - object: metric:overdue_count
    property: caliber.note
    question: 逾期按当前状态还是曾经逾期判断？关闭/核销贷款是否包含？
    owner_role: business_owner
    candidate: 当前状态为逾期且未核销
    evidence_refs: [访谈记录-01, 字典-status]
```

自动补齐项包括 scoped 数据集的 grain/primary_key/fields/source/temporal.kind，以及 scoped 指标的 dataset/caliber.note/unit/time_field/expr。已有非空属性原样保留，不等于程序重新验证了业务正确性。已有但有争议的内容放到 `required`，成为带证据的候选等待确认。

**复用事实后补业务缺口**：已有表、字段和关系可先用 [derive_ontology](metadata-to-consumption.md) 补语义候选，不必从空白重录。模型含 `ontology` 段时，业务问题排在物理问题之前——数据集缺 `ontology_ref` 先问"该数据集承载哪个业务对象"（fde）；对应实体缺 `attributes` 再问"该业务对象的关键业务属性（不依赖具体表）有哪些"（business_owner）；然后才是粒度/主键/字段/来源/时态。这是缺口核对顺序，不要求丢掉已有数据图谱或重新确认有效决定。无 `ontology` 段的模型不产生本体类缺口，行为与 v0.0.5 一致。

scope.required 支持 object：`model`（顶层合同）、`scope`、`dataset:<name>`、`metric:<id>`、`relationship:<id>`、`concept:<term>`、`ontology_entity:<name>`、`ontology_relation:<id>`。property 是对象内的点分路径；列表属性以整体值提交，例如 fields/constraints/attributes；禁止通过回答修改对象 identity。模型中的企业自定义属性可保留，但不意味着执行器支持它们。

```bash
python scripts/guide_model.py init --model partial.yaml --scope scope.yaml --session session.json
python scripts/guide_model.py init --model partial.yaml --scope scope.yaml --session session.json \
    --pack starter_packs/general.yaml --pack starter_packs/traffic.yaml   # v0.0.7 冷启动
python scripts/guide_model.py status --session session.json
```

**冷启动模板包**（v0.0.7）：不从白板开始建模。`--pack` 把 `starter_packs/` 的本体声明（实体含 uid/属性/证据来源，关系含 mapping）合并进模型，已存在的对象不覆盖——你的模型永远优先。合并结果记入会话 `packs_applied` 可追溯。领域包清单与自定义写法见 `starter_packs/README.md`。

**提问与采纳协议**（v0.0.7）：只问现有材料不能回答、会改变当前行为的问题，不按固定题量补访谈；每个问题给出**候选项（suggestion.value）+ 依据 + 备选**——候选项由使用本 skill 的 Agent 基于材料推断生成（脚本只存证、不调用模型），用户可直接回"按候选确认"——落成 decision 即 `state=confirmed、value=候选值`，actor/basis 如实填写（脚本不认证角色身份，采纳仍由人确认）。status/export 的 gap 带三态标签：`[待确认]`（无候选）、`[候选·推断]`（Agent 推断候选）、`[候选·来自材料]`（材料里已有）、`[已确认]`/`[暂缓]`/`[已否决]`。`clearance` 是待确认清零报告：outstanding（pending+candidate）清零且无阻断项才 ready_for_validation——发布前先清零。

会话单文件包含 model、scope、revision、gaps、decisions；JSON 是权威状态，Markdown/HTML 是展示。gap ID 由 scope/object/property 生成，与问题措辞、数组顺序无关。session 是串行文件工作流，不支持多用户并发编辑/事务合并；同时编辑前先合并意见，再生成一个补丁。

## 回答与审阅补丁

读取 status 返回的真实 gap_id，不手造 ID。回答必须来自用户或已授权的责任人；脚本不认证角色身份。

> **answers.json 的两个易错点**：① `session_revision` 必须等于 `status` 返回的当前 `revision`（每 apply 一次 +1，过期会被拒并提示当前值）；② `decisions` 按 `gap_id` 组织——`examples/onboarding/decisions.yaml` 那种按 `对象/属性` 组织的是**回答素材**，不是 answers 文件（run_demo.py 演示了怎么把它包装成 answers）。

```json
{
  "session_revision": 0,
  "decisions": [{
    "gap_id": "G-从实际status复制",
    "state": "confirmed",
    "value": "一行一笔合同项下的贷款",
    "actor": "实际确认人",
    "role": "business_owner",
    "basis": "实际需求决议或用户本次明确回答",
    "evidence_refs": ["会议纪要或字段字典引用"]
  }]
}
```

`state` 可为 confirmed/deferred/rejected；deferred/rejected 不写入候选值，继续阻断关联用例。待补数据可用 deferred 并在 basis 中记录缺何数据及责任；互相冲突的解释保留为候选和证据，责任人裁决后再 confirmed。需要修改已确认答案时，填 `supersedes_revision` 对应 gap 的 decision_revision，日志保留旧决定。

```bash
python scripts/guide_model.py propose --session session.json --answers answers.json --patch review.json
# 检查 changes 中 before/after、remaining_blockers 和回答依据
python scripts/guide_model.py apply --session session.json --patch review.json
python scripts/guide_model.py export --session session.json --out draft
```

propose 不改变会话；apply 校验会话摘要、回答版本和补丁内容，原子替换单个会话文件。重复应用已应用的同一补丁不重复决策；旧补丁遇到其他修改必须重新 propose。导出新目录中的模型、scope、session、gap-report 和 manifest 始终标 draft；“ready_for_validation”只表示声明的阻断项已经解决。

## 数据不足和持续补齐

历史时点用例指定 `time_requirement: historical_as_of`。相关数据集需要 `temporal.kind: event|snapshot` 和字段清单内的 `temporal.as_of_field`。这仍是能力声明，不自动证明事件完整、快照周期/时区正确；把这些事项放入 required，补充源数据与独立期望。

若当前模型没有需要的对象，先以受控模型变更新增草案，再用新 session 引用；本工具不从自由文本自动建新表或补造数据。新增/改范围后重建 session 并保留旧会话为历史，不能把未确认属性抹成“无需回答”。

应用答案后重新执行 `check_model`，再按需要检查约束、关联、独立结果、受影响回归；旧报告的模型哈希会失效。将当前 session 传给 release_gate/visualize_model，使缺口状态与报告显示一致。没有 DB 可先交 draft，但不能进入 validated 门禁。

当前状态统计若已明确 `scope.time_requirement: current`，不强迫补指标 time_field；历史或未明确时仍询问时间依据。实体投影同时支持稳定 uid 和 name。
