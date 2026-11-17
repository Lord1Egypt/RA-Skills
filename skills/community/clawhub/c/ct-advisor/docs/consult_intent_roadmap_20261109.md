# ct-advisor「咨询型问答 vs 执行型调用」能力分层扩充方案

日期：2026-11-09 · 状态：**用户已拍板 P0+P1 同批实施，进行中**
适用版本：v1.3.39（含当日 handoff / 回程汇总 / 中文抽参改造）

> **用户裁定（2026-11-09 晚间）**：① P0+P1 同批做；② 产物涉及涉密数据时
> **允许脱敏数值摘要外发**（L3 增强版）；③ 知识库**由 ct-advisor 技能产出内容，
> 但必须上传到 Coze 端点统一维护，本地不放 KB 资产**。
> §3.2 已按此重写；§6 的待拍板项据此结案。

---

## 1. 问题定义

兄弟技能是**执行型**能力：`ct-samplesize` 做计算、`ct-registry` 做检索、
`ct-safety` 做不相称性统计、`ct-literature` 做文献检索。它们不负责回答
「为什么」「怎么理解」「依据是什么」。

而临床研发中大量的高价值问题是**咨询型**的：

- 样本量：非劣效界值如何确定、α 消耗函数与期中分析的关系、把握度与效应量
  假设的取舍、ICH E9(R1) estimand 五属性对估算的影响
- 安全性：PRR / ROR / IC / EBGM 的差异、为什么 EBGM 要贝叶斯收缩、
  95%CI 如何解释、信号评分的局限
- 注册：CT.gov 的 `Phase 1/Phase 2` 复合分期字段语义、状态枚举、登记与公示时限

这些必须由 ct-advisor 自己的 **Coze 知识库 + 权威锚点**回答。现在的路由是
「关键词 / 实体触发」，没有区分意图，导致把方法学问答误派给计算/检索技能。

### 1.1 实测证据（本轮，本地 `route_tool.predict` + 云端 `tool_router_node` 同时跑）

| 问句 | 应归属 | 本地判定 | 云端判定 | 结论 |
|---|---|---|---|---|
| 非劣效试验的界值应该怎么确定？ | 咨询 | `None` | `None` | ✓ 碰巧正确 |
| 样本量计算里 α 消耗函数与期中分析的关系是什么？ | 咨询 | `ct-samplesize` | `ct-samplesize` | ✗ **误派** |
| PRR 和 ROR 有什么区别，为什么 EBGM 要做贝叶斯收缩？ | 咨询 | 软建议 `ct-safety` | `None` | △ 靠「有什么区别」护栏碰巧拦住 |
| FAERS 不相称性分析的 95%CI 应该怎么解释？ | 咨询 | `ct-safety` | `ct-safety` | ✗ **误派** |
| ICH E9(R1) estimand 的五个属性如何影响样本量估算？ | 咨询 | `ct-samplesize` | `ct-samplesize` | ✗ **误派** |
| ClinicalTrials.gov 的 Phase 字段为什么有的是 Phase 1/Phase 2？ | 咨询 | `ct-registry` | `ct-registry` | ✗ **误派** |
| Why does a non-inferiority margin need both statistical and clinical justification? | 咨询 | `None` | `None` | ✓ |
| What is the difference between PRR and ROR…? | 咨询 | 软建议 `ct-safety` | `None` | △ 碰巧 |
| 帮我算下样本量，ORR 30% vs 45% | 执行 | `ct-samplesize` | `ct-samplesize` | ✓ 正确 |
| 拉一下司美格鲁肽在 2 型糖尿病的注册试验 | 执行 | `ct-registry` | `ct-registry` | ✓ 正确 |
| 解释一下非劣效界值怎么定，并帮我算一下样本量 | **混合** | `ct-samplesize` | `ct-samplesize` | ✗ 原理部分被吞 |
| 先说明 PRR 的原理，再查一下阿司匹林肝损伤的 FAERS 信号 | **混合** | `ct-safety` | `ct-safety` | ✗ 原理部分被吞 |

**8 条咨询问句中 4 条被误派为执行**；另 2 条只是恰好命中「有什么区别」护栏，
并非系统理解了「技术细节」意图。两条混合意图都被当成纯执行。

### 1.2 三个根因

1. **护栏词表太浅**：本地 `route_tool.METHOD/DEF/DOC` 与云端
   `tool_router_node._CONSULT_*` 只覆盖「是什么 / 怎么做 / 要模板」，
   没有「原理 / 依据 / 参数语义 / 统计解释 / 方法选择」这一层。
   且 `RETRIEVAL` 里含裸词「统计」，中文「统计方法」会被当成取数动作让位。
2. **域提示没进主链路**：`scope_guard.classify_domains` 对上述问句能正确命中
   `stats` / `design` / `compliance`，但 `entry.py` 只在 **超范围** 时注入
   `scope_hint`（`if not _in_scope and _tag`），正常在范围内的问题恒为空串，
   Coze 端因此拿不到 `stats` / `methodology` 这类 domain，无法定向检索知识库锚点。
3. **两套规则表独立**：本地 `route_tool.py` 与云端 `tool_router_node.py` 同义但
   各自实现，`scripts/check_route_drift.py` 只检测漂移、不自动统一。
   任何单边改动都会造成「本地不预判、云端仍委托」的不一致。

---

## 2. 目标能力模型（三层）

| 层 | 用户意图 | 由谁完成 | 交付形态 |
|---|---|---|---|
| **L1 咨询 / 方法学** | 原理、参数含义、方法选择、结果解读、法规依据 | ct-advisor + Coze KB + 权威锚点 | 带来源标注的方法学答案；末尾可选 `@skill:` 软建议 |
| **L2 执行 / 取数** | 算样本量、检索注册库、跑 FAERS、找文献 | 兄弟技能（handoff，客户端直调） | `@skill:` 卡片 + 参数 + 交付物说明 |
| **L3 结果解读（新增）** | 技能结果拿回后「这个 PRR 意味着什么」「n=190 够不够」 | advisor KB + **脱敏**数值摘要 | 解释性答案；受 F33 严格约束 |

**判据不是「有没有技能关键词」，而是「有没有执行动词 + 可计算/可检索的输入」。**
`PRR` 出现在问句里不代表要跑 FAERS；`样本量` 出现也不代表要算 n。

---

## 3. 具体改动清单

### 3.1 意图判定层（核心，本地 + 云端必须同步）

新增 `CONSULT_DEPTH` 受控词表，与既有 `EXEC_INTENT` 组成决策表：

| 咨询深度词 | 执行动词 | 判定 | 动作 |
|---|---|---|---|
| 有 | 无 | **L1 咨询** | 不下发 `need_tool`；`scope_hint` 注入 domain；答案末尾可给软建议 |
| 有 | 有 | **混合** | advisor 答原理 **＋** 单独产出 L2 handoff 卡片，互不覆盖 |
| 无 | 有 | **L2 执行** | 维持现有 handoff |
| 无 | 无 | 现有 DEF/METHOD/DOC 护栏处理 | 不变 |

- `CONSULT_DEPTH`（示例，需评审后定稿）
  - 中文：原理 / 机制 / 为什么 / 依据 /  rationale / 如何确定 / 如何解释 /
    取决于 / 受影响 / 关系是什么 / 含义 / 假设 / 前提 / 界值 / 消耗函数 /
    把握度 / 多重性 / 收缩 / 偏倚 / 敏感性 / 估计目标 / 95%CI 解释 / 适用条件
  - 英文：`why` / `rationale` / `how is … determined` / `interpret(ation|ed)?` /
    `assumption` / `underlying` / `trade-?off` / `derives? from` / `applicability`
- `EXEC_INTENT`（执行动词 + 明确对象，替换现在「一命中就全让位」的粗放规则）
  - 算 / 计算 / 求 / 帮我算 / 跑一下 / 生成报告 / 检索 / 查 / 拉一下 / 导出 /
    `compute` / `calculate` / `run` / `fetch` / `export` / `pull … trials`
  - 单独的「统计 / 有哪些 / how many」不再无条件让位，需与对象同现。
- **单一真相源**：词表抽到 `config/intent_contract.json`；本地与云端各持内嵌副本，
  扩展 `scripts/check_route_drift.py` 用 AST 断言三份逐字一致（复用
  `scripts/test_cloud_brief.py` 已有的契约同步范式）。
- 🔴 **云端 `tool_router_node.py` 改动需用户手动重新发布 Coze 包**；
  本地代码改动不会自行上线（brief 改造时已验证过这个模式）。

### 3.2 知识锚点层（🔴 用户 2026-11-09 裁定：**Coze 端点统一维护，本地零知识库**）

> **架构红线**：`AGENTS.md` 明确「All domain expertise lives on the Coze cloud side.
> The local side retains ZERO knowledge base」；`CHANGELOG` 2026-09-16 的
> 「知识库双轨铁律」规定所有知识改动**只落扣子端 `adapters/coze/knowledge/`**。
> 初版方案把锚点写成 `config/kb_topics.json` + `docs/methodology_anchors.md`
> （本地、随技能分发）**违反该红线，已撤销**，两文件均已删除。

- **唯一维护位置**（Coze 端点生产库，随 Coze 包发布）：
  `adapters/coze/knowledge/ref-topic-samplesize-methods.md`（estimand 五属性 / α 消耗与
  期中分析 / 非劣效界值 M1-M2 / 把握度假设）、
  `ref-topic-signal-methods.md`（PRR/ROR/IC/EBGM / 贝叶斯收缩 / 95%CI / FAERS 局限）、
  `ref-topic-registry-semantics.md`（复合分期 / Status 枚举 / 登记公示时限 / 跨源去重）。
  沿用家族既有 `ref-topic-*` 模式（`ref-topic-p21-data-rules` / `ref-topic-m12-ddi`）。
- **Coze 端接线**：`reference-index.md` Topic 表登记三个文件 + 新增常驻注入的
  「**L1 咨询答案契约**」（来源标注 / 反幻觉红线 / 混合意图 / 软建议）；
  `src/kb/__init__.py` 的 `_CATEGORY_KNOWLEDGE` 把三文件挂到 b/c/d/f/g，
  `_SEMANTIC_MAP` 新增 `methodology → c`；
  `build_knowledge_index.py --merge` 重建 `knowledge_index.json`（追加 518 键、保留 4750 键）。
- **本地只剩「引用」不剩「正文」**：`entry.py` 把 `scope_guard.domain_hint(q)` 写进
  **`query_meta.domain_hint`**；`full_analysis_node.py` 在 `category` 为空时用它做
  **文件级兜底**。章节级精确路由仍走 `extract_question_keywords(原问题)`，
  靠三个专题 `###` 标题里的中英关键词命中（已实测中文 8 条问句命中）。
- 🔴 **不得复用 `scope_hint` 传 domain**：云端
  `full_analysis_node._doc_prompt_directive` 把任何非空 `scope_hint` 一律渲染成
  「**可能超出本技能临床试验法规/方法学核心覆盖范围**」；`state.py` 亦注明
  「仅透传，不参与检索」。初版把正常域塞进 `scope_hint` 会给每条方法学问题
  加上错误的超范围声明，已修正。
- **已知边界**：`knowledge_index.json` 由 `setdefault` 按文件名字母序生成，
  `prr` / `ror` / `disproportionality` 等英文键被既有 `ref-reg-safety.md` 优先占用，
  英文术语问句仍命中旧库（该库本就覆盖安全信号主题），且 L1 答案契约经常驻
  `reference-index.md` 保证；新专题主要经**中文独占键 + category 兜底**命中。

### 3.3 答案形态层

- L1 答案统一加标识「方法学解释，非取数结果」＋权威来源标注＋边界声明
  （不代替统计师 / 注册事务结论）。
- 🔴 **反幻觉红线**：咨询答案里不得出现具体试验数、PRR 值、样本量结果，
  除非用户已通过 `entry.py --stitch` 回填产物。
- L3 的合规边界（需拍板）：产物可能含 B 档涉密数据，**不得**外发 Coze。
  可选两条路：
  1. **保守版（建议先做）**：L3 不外发数据，只在 `--stitch` 汇总里附本地静态
     「方法学提示文本」（不含数值），并把「这个数值意味着什么」引导回 L1 问答；
  2. **增强版（需单独授权）**：由 `stitch_results.py` 代码抽取**字段白名单内的
     脱敏数值摘要**（如 `prr=1.23`、`n_per_group=190`），作为 `interpret_spec`
     发给 Coze 请求解释；原始产物、方案文本、受试者数据一律不出域。

### 3.4 混合意图拆分

一句话同时要原理和计算时，`predict` 产出 `need_tool=None` +
`suggest_tools=[...]` + 新增 `exec_intent=True`；Coze 侧 `need_tool` 置空、
按 L1 生成方法学答案；`build_output` 用 `suggest_footer` 在末尾附可直接调用的
`@skill:` 卡片。避免现在「原理部分被 handoff 吞掉」的问题。

### 3.5 回归与门禁

- 新增 `scripts/test_consult_intent.py`：同时加载本地 `route_tool` 与云端节点，
  断言 ≥20 条问句（咨询 / 执行 / 混合 / 中英 / 边界）的意图与 handoff 决策。
- `check_route_drift.py` 新增 `intent_contract.json` 三副本一致性断言。
- 线上 canary 增加「咨询问句不得返回 `need_tool`」断言。
- 现有回归必须全绿：`route_tool` 37/37 + 13/13 + 6/6、
  `test_tool_router` 63/63、`test_cloud_brief` 53/53、跨技能 28+15+13+14、
  线上 canary 18/18。

---

## 4. 分阶段实施建议

| 阶段 | 内容 | 部署依赖 | 是否单独生效 |
|---|---|---|---|
| **P0** | 3.1 本地侧词表、`config/intent_contract.json`、`query_meta.domain_hint`、3.5 回归脚本 | 无（纯本地） | ❌ **不能**——Coze 仍会下发 `need_tool` |
| **P1** | 云端 `tool_router_node.py` 同步词表、`full_analysis_node` 消费 `domain_hint`、**Coze 端点 KB 三专题 + 索引 + 路由表**、canary 新断言 | **用户手动重新发布 Coze 包** | ✅ 真正生效 |
| **P2** | 3.4 混合意图拆分、3.3 L3 结果解读（**已拍板增强版：脱敏数值摘要外发**） | 视方案而定 | 可选增强 |

⚠️ 强烈建议 P0 与 P1 **同一批次发布**，否则中间态会出现两端规则不一致。

---

## 5. 红线与风险

- **HARD GATE 不变**：意图判定全部由代码完成；答案仍由 Coze 产出、
  经 `entry.py` 单一出口；本地 LLM 依旧只跑一条命令、原样透传 stdout。
- **F33 出域边界**：咨询类问句只发公开方法学问题；L3 若走云端只能送脱敏数值摘要，
  绝不送原始产物 / 方案 / 受试者数据；`doc_context` 不进检索通道的既有约束不变。
- **两套规则表必须同步**，这是历史上复发过两次的缺陷类型。
- **词表扩张有回归风险**：`PRR` / `样本量` / `统计` 等高频词一旦放宽，
  可能把真实执行请求误拦成咨询 → 必须用 3.5 的门禁与真实问句集守着。
- **可回滚**：新增意图判定做成开关（建议 `CT_ADVISOR_INTENT_DEPTH`，默认关→灰度→开），
  关闭时行为与改造前逐字一致；云端包未发布前线上行为也不变。

---

## 6. 待拍板事项（2026-11-09 已全部结案）

| # | 裁定 | 落地 |
|---|---|---|
| 1 | **P0+P1 同批做** | 本轮同批改本地与云端，统一打包发布 |
| 2 | `CONSULT_DEPTH` 口径按真实问句集迭代定稿 | `config/intent_contract.json` 为单一真相源，drift 门禁锁三副本 |
| 3 | 知识库**由 Advisor 技能产出内容，但上传到 Coze 端点统一维护，本地不放** | §3.2 重写；本地两文件已删；三专题落 `adapters/coze/knowledge/` |
| 4 | L3 用**增强版**：允许脱敏数值摘要外发 | 字段白名单 + 类型/数量约束，原始产物 / 方案 / 受试者数据绝不出域 |
