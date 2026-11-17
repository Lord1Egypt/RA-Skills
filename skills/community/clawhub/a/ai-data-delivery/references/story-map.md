# 新领域落地 · 历史项目故事地图

> 历史案例的方法记录，按任务裁剪；不是首次使用流程、固定阶段或工期承诺。早期可先有业务定义草案，无物理数据时不声称完成投影和数值验收。

> 基于两个真实项目复盘（交通安全监管 16 实体 18 关系 94 指标；运智管家企业 Agent 31 数据集 86 盘点指标），2026-09 校准。
> 这张地图回答一个问题：**我（FDE / 产品经理 / 信息中心）在一个全新领域，从这个 skill 能得到什么、每一步做什么、产出什么价值。**

```
备货        划域         冷启动        首链          提升           收口        验证        运营
原材料盘点 → 子系统切分 → 骨架建模 → 3表打通链路 → 指标可执行化 → 网关护栏 → 上线门禁 → 持续质量
 0.5天       0.5天       1天          2-3天        1-2周(主战场)   并行        2-3天      持续
```

案例中采用的三条方法（按当前任务判断）：
1. **先物理后声明**——ingest_ddl/profile_db 的事实在前，语义声明必须投影回物理层被 lint 对账；允许从需求文档形成有来源的候选，不能把候选当成已核实物理事实
2. **先 3 张表打通，再扩展**——从当前用例所需的小范围验证效果，再决定是否扩展；历史实验不证明所有项目收益相同
3. **影响业务含义的提升要有明确依据**——发现字典不一致时先核实映射；不把批量操作本身当作确认

---

## Stage 0 · 备货：原材料盘点（0.5 天）

**我是谁**：FDE 或数据产品经理。我手里有：业务系统 mysqldump、既有指标库导出（Excel/JSON）、（最好有）真实库只读快照。

```bash
python scripts/ingest_ddl.py --ddl 数仓.sql --out inventory/              # 物理事实
python scripts/harvest_metrics.py --metrics 指标库.json --out inventory/  # 指标资产三分
python scripts/profile_db.py --db 快照.db --out inventory/profile.yaml    # 值域事实（有真实库时）
```

| 我得到 | 价值 |
| --- | --- |
| inventory：N 张表/M 字段、命名前缀聚类、parse_failures 台账 | 第一天知道家底：几个子系统混在一起、表命名规范程度 |
| metrics_raw：可执行候选/需改写/无来源 三分 | 指标库真实可执行率（经验值：约 20% 是常态，不是异常） |
| **gaps.yaml 数据缺口台账** | 直接甩给信息中心闭环——"这些指标没有数据源"是第一天就该亮的牌 |

## Stage 1 · 划域：多子系统切分（0.5 天）

多产品公司必然面对：一个库里多个产品的表。决定"一个 semantic.yaml 覆盖谁"。

- 每个子系统一个模型文件，**共享概念层**（组织/人员/时间/地点从 starter_packs/general 来）
- 原则：问数场景跨子系统的才合并，否则分开——模型宁可小而活
- ingest_ddl 的命名前缀聚类直接产出切分建议

| 我得到 | 价值 |
| --- | --- |
| scope.yaml × N + 共享概念层 | 避免"几百张表 6 个产品揉一个模型"的后期纠缠 |

## Stage 2 · 冷启动：骨架建模（1 天）

```bash
python scripts/guide_model.py init --model semantic.yaml --scope scope.yaml \
    --session session.json --pack starter_packs/general.yaml
```

- **先业务后物理**：先把业务对象（本体实体）、业务属性、对象间谓词声明下来——没有物理表也行，W14 让"纯本体草案"成为合法中间态，lint 照样过
- 引导会话按角色分工提问，每个问题带**候选项+依据**（候选由 Agent 生成、脚本存证），可回"按候选确认"
- 每个答案带 actor/依据/修订记录，补丁应用前必须审阅

| 我得到 | 价值 |
| --- | --- |
| semantic.yaml 骨架（业务语言层） | 团队对"这个领域有哪些对象、怎么称呼"达成一致——所有后续工作的语义地基 |
| 未清零缺口清单 | 哪些业务问题还没人答，一目了然，不会悄悄漏掉 |

## Stage 3 · 首链：3 张宽表打通链路（2-3 天）

选**用户问得最多的 3 个主题**（如：企业档案/隐患台账/报警明细）。

```bash
python scripts/propose_dws.py --inventory inventory/ --out dws_draft.yaml  # 宽表建议
# 建 meta：grain/pk/time/血缘/「可回答·不可回答」边界
python scripts/check_model.py -f semantic.yaml                             # 0 ERROR 才算通
python scripts/check_join_graph.py --model semantic.yaml --db 快照.db      # 有真实库就跑
```

- 快照宽表时间字段默认 `stat_date`；tenant_field 从第一张表就标——事后补是全量返工

| 我得到 | 价值 |
| --- | --- |
| 最小可用语义层（0 ERROR）+ 第一张语义图 | 端到端跑通"提问→指标→SQL→结果"，给甲方的第一公里演示 |
| 宽表 meta 的血缘与问答边界 | NL2SQL 兜底路径的选表依据，也是培训材料 |

## Stage 4 · 提升：指标可执行化（1-2 周，主战场）

这是新领域落地的**主战场**——运智管家实测 86 个指标只有约 17% 可直接执行，别指望批量导入。

```bash
python scripts/promote_draft.py --raw inventory/metrics_raw.yaml --from-meta meta/ \
    --model semantic.yaml --out promote/     # 逐条生成提升草稿（四分：✅/🔶/⛔/📋）
```

每条草稿自带：目标数据集、字段翻译（中文→物理列）、枚举值对齐提议、比率分子分母拆分（SUM/SUM 加权，禁行级平均）、**待决项标记**。然后开业务审阅会，按 提升清单.md 逐条拍板：

```bash
python scripts/patch_model.py -f semantic.yaml batch promote/ops.yaml --db 快照.db   # 批量一次写入+验算
```

- list/rank 类进**明细查询模板**（templates 段，一等资产），路由"要清单还是要数字"先分流
- 每条指标 synonyms ≥ 3 由 lint 门禁强制（W17）——这是指标命中路由的生命线
- ⚠️ 表名未映射的指标单独可见，不会掉进"有来源但没映射"的缝里

| 我得到 | 价值 |
| --- | --- |
| 以原始盘点为基准记录提升后的可执行比例 | 需实际统计分母、支持范围与拒绝项，不预先承诺覆盖率 |
| 审阅留痕：每条口径谁拍的、依据什么 | 甲方信息中心接手时能看懂每个数字的来历——ToG 交付的硬通货 |
| 明细模板库 | 清单类问题不再挤占指标路由，也不被错误聚合 |

## Stage 5 · 收口：网关护栏（与 Stage 4 并行）

- tenant_field 全量标注（patch 批量），命名统一
- 敏感字段：`profile_db` 候选扫描 → 逐表确认 → 导出拒绝在网关落地
- 时间围栏：每张表记录"数据新鲜到哪天"，"今天/本月"的回答先对围栏

| 我得到 | 价值 |
| --- | --- |
| 明确租户/时间/敏感范围，交由目标网关执行 | 必须验证实际请求与越权反例；模型声明本身不提供安全隔离 |

## Stage 6 · 验证：上线门禁（2-3 天）

```bash
python scripts/run_eval.py --model semantic.yaml --endpoint $ENGINE --cases cases.json  # live 模式
python scripts/release_gate.py --profile validated --model semantic.yaml \
    --cases cases.json --db 快照.db --eval-report eval.json --out gate.json
```

- 评测必须在**正式 LLM 链路**上跑（教训：前端规则引擎的 92.6% 不能当上线依据，证据分级只能标 mock）
- 门禁 not_ready 时逐 gate 给 actionable 提示

| 我得到 | 价值 |
| --- | --- |
| 带证据分级（live）的准确率数字 | 敢上线，也敢向甲方汇报 |
| release_log 留痕 | 每次放行的技术证据可审计 |

## Stage 7 · 运营：持续质量（长期）

```bash
python scripts/check_model.py -f semantic.yaml --drift 上一版.yaml     # 变更四级分类接 CI
python scripts/check_model.py -f semantic.yaml --history quality_history.jsonl
python scripts/visualize_model.py -f semantic.yaml --history quality_history.jsonl --out model.html
```

- drift 分新增/删除/变更/破坏四级，**破坏级变更 CI 直接拦**
- 质量趋势图给甲方信息中心：ERROR 恒零、WARN 收敛，是"数据智能持续产生价值"的可视化证明
- 新规则发布后在存量模型上扫出的 WARN（如 W15/W16 曾在交通生产模型抓出 7 条真实口径风险）= 持续的资产体检

---

## 角色泳道（谁在哪段做什么）

| 阶段 | FDE | 产品经理 | 业务专家 | 信息中心 |
| --- | --- | --- | --- | --- |
| 0 备货 | 跑盘点三件套 | 提供指标库导出 | — | 提供 DDL/快照，认领 gaps.yaml |
| 1 划域 | 提切分建议 | 拍板模型边界 | — | — |
| 2 冷启动 | 驱动引导会话 | 答业务问题 | 确认候选/拍板口径 | — |
| 3 首链 | 建宽表+meta | 选 3 个高频主题 | 确认问答边界 | 确认抽取周期 |
| 4 提升 | 生成草稿+执行补丁 | 组织审阅会 | **逐条拍板** | 确认数据源 |
| 5 收口 | 标租户/敏感 | 定导出策略 | — | 定租户映射 |
| 6 验证 | 跑评测门禁 | 判接受度 | 抽验答案 | — |
| 7 运营 | 巡检+drift | 看趋势图 | — | 看趋势图 |

## 边界声明（防过曝）

- 自然语言理解、SQL 生成是**问数引擎**的事——本 skill 产出让引擎答得对的语义资产与验证证据，不替引擎答题
- 不做 OWL/形式推理（配置化本体，可移交可审计优先）
- 业务口径拍板不代办——工具只把"必须人审的位置"标出来并留痕
- 知识库（法规/制度）走 RAG 路线，不进语义模型；只在网关层统一权限/租户

## 时间账本（真实项目实测校准）

| 阶段 | 工期 | 关键路径 |
| --- | --- | --- |
| 0+1+2 | 约 2 天 | 工具自动为主 |
| 3 首链 | 2-3 天 | 宽表 ETL（本 skill 之外） |
| **4 提升** | **1-2 周** | **业务审阅会的排期与拍板速度** |
| 5+6 | 3-5 天 | 真实库接入与正式引擎就绪 |
| 合计 | 案例估算约3–4周，非承诺 | 实际工期取决于资料、实现、业务决定和验证条件，按当前项目估算 |
