# PharmaSUG 2026 AI-201 深度分析：AI 独立 QC 代码生成框架——机制、实证与批判

> **分析对象**：Yan J, Zhang J (Merck & Co., Rahway, NJ). *Eliminating QC Programming Duplication Through Claude AI-Assisted Independent Code Generation: A Practical Framework for Regulatory-Compliant Validation*. PharmaSUG 2026, Paper AI-201.
> **原文**：13 页 PDF，2026-10-19 自 `pharmasug.org/proceedings/2026/AI/PharmaSUG-2026-AI-201.pdf` 下载并全文提取（含正文 §1–6 与附录 A–D：prompt 模板、22 条规则表、路由明细、Trace Tree schema）。
> **代码/数据**：github.com/yanmingyu92/ai-qc-code-generation；github.com/yanmingyu92/eSubmission-Benchmark。
> **分析日期**：2026-10-19。本文档是 ct-base §22.10–§22.21 规范条款的深度依据（证据登记见 `qc_independence_pharmasug2026.md` §1）。
> **收编说明**：2026-10-19 由工作区周报分析（`reports/pharmasug2026_ai201_deep_analysis_2026-10-19.md`）收编为 ct-base 权威副本，随 `publish_inject` 白名单下沉各技能；第七节「九条可落地借鉴」已落地为 §22.18–§22.21 及 §22.13/§22.15 扩写。

---

## 结论先行

1. **这是迄今「AI 做临床编程」领域工程完整度最高的一篇**：不止论文，四组件（隔离实例 / Trace Tree / Decision Router / Skills + Code Review 引擎）全部开源，可直接复现——区别于多数只报告效果的 AI 论文。
2. **框架的核心洞见不是「让 AI 写 QC 代码」，而是「先把 QC 最有价值的部分（独立审 spec）保留给人，把重复劳动交给 AI」**：84 分钟工作流里 55%（46 分钟）是人在审 Trace Tree 和解歧义，AI 计算只占 38 分钟。标题里的 "Eliminating" 消除的是重复劳动，不是人的判断。
3. **97.1%–100% 的变量级匹配率需要正确解读**：这是「给定良构规格时 AI 复现已知正确答案」的保真度，**不是**「AI QC 能检出生产程序错误」的能力——基准里所有残余失配都溯源到规格歧义，全部在生成前已被标记，没有任何一项是 AI 抓住的「生产代码 bug」。QC 的真正考题（检出错误）这篇论文其实没有直接测。
4. **作者自曝了一处路由失准**（ADADAS 拿到最低匹配率 97.1% 却被路由为「全 AI 生成」，与 100% 的 ADTTE 同路）——这种诚实的自我批评在 PharmaSUG 论文里少见，也正是全框架最脆弱的一环（路由决定人盯哪里，错了就系统性漏风险）。
5. **「同模型偏差」是框架的结构性软肋，作者明确承认并把人定为唯一防线**：生产与 QC 两个实例共享同一份模型权重，会把同一处 spec 误读成同样的错——这正是 N-version 编程的共因故障。人在回路的权重因此不可压缩。
6. **对 ct- 族的直接可移植资产有 9 项**（详见第七节），其中三项含金量最高：Gate 1 规格就绪度评分（六项 checklist）、Trace Tree 三步工序（Appendix A prompt 模板与 ct-base §22.1/§22.2 的 HITL gate 纪律完全同构，等于独立实证）、CL-005「读答案即泄漏」检测规则（对 ct-sdtm 合成数据生成同样适用）。

---

## 一、问题定义：QC 双编程为什么贵，又不能简单砍

论文对 QC 浪费的刻画是三段论：

| 浪费源 | 机制 |
|---|---|
| 重复解析 | 生产与 QC 两个程序员各自通读同一份规格 |
| 重复实现 | 同样的派生逻辑、同样的边界处理写两遍 |
| 线性放大 | QC 工作量随生产工作量线性增长；引用 Lyons & Bae (PharmaSUG 2023, AD-189) 估计 QC 占总编程量 **30–50%** |

同时引用 Avizienis 1977 的 N-version programming 经典结论指出双编程的**深层局限**：两个独立实现对**共同规格**的系统性误读是相关的——规格错了，两套一起错。这句话是全文伏笔：AI QC 解决的是「写得慢」，解决不了「 spec 错了一起错」；而且两个 AI 实例共享模型权重时，相关误读比两个人之间更严重。

既有自动化工具（PROC COMPARE 包装、元数据驱动校验框架）只解决「输出比对」，不解决「从规格生成 QC 代码」这个上游问题——本框架填这个空档。

---

## 二、六大设计目标（论文 §2.2）

1. **Operational Separation**：隔离的 AI 实例，QC 侧拿不到生产代码；
2. **Specification-Driven**：QC 代码只从规格生成；
3. **Transparent Reasoning**：每次派生产出可追溯树（spec 来源/逻辑/边界/验证状态）；
4. **Systematic Routing**：按数据集类别、规格质量、复杂度系统选择 QC 路径；
5. **Automated Quality Monitoring**：Code Review 引擎对所有生成代码强制执行编程 SOP；
6. **Risk-Based Applicability**：明确什么时候适合 AI QC、什么时候回退传统手段。

注意目标 2 和目标 4 的顺序：**规格出发不是口号而是闸门**——规格不够好，Gate 1 直接拒绝生成（见 4.2）。

---

## 三、机制层深拆

### 3.1 操作隔离：把「独立」从提示词自律升级为基础设施

论文强调（并在脚注 1 显式挂靠 N-version 共因故障文献）：QC AI 实例**不接收生产代码、不接收生产日志、不共享对话上下文**，靠三层工程手段保证：

1. 独立 API 会话 + 独立凭证 + 独立 IAM 角色；
2. 输入隔离：QC 侧只给规格 + SDTM 源数据，生产工件在**基础设施层**被拦截；
3. 审计日志：所有 AI 输入、输出、模型版本、skill 版本全记录。

人的位置被明确保留：**human QC programmer 是「关键独立判断层」**——审 AI 的规格解读、找 AI 漏掉的边界、用领域知识兜底。

> ct- 映射要点：这一条直接支撑 ct-base §22.10 的写法——「隔离是基础设施控制，不是提示词自律」。写 SKILL.md 时常见的错误是把「不要看生产代码」写成 prompt 约束，那在工程上等价于没有。

### 3.2 Gate 1：规格「AI 就绪度」六项检查（全文最被低估的设计）

代码生成前先给规格打分，六项标准：① 派生规则显式；② SDTM 源变量指明；③ 边界情况有文档；④ 变量元数据；⑤ 人群 flag 逻辑；⑥ 访视/时间定义。

基准包的 5 个数据集里 4 个拿到 **5/6**——论文立刻补一句「这反映 CDISC 试点项目的规格质量，**不代表真实世界研究规格**」。不达标的处理是 Gate 1 FAIL → **退回规格作者**，AI 拒写。

这个设计的价值在于它把「规格质量问题」翻译成了一个**流程动作**（谁的事谁回去补），而不是让 AI 在模糊 spec 上硬猜、产出看似工整的错代码。对 ct- 族是现成可搬的验收前置。

### 3.3 Decision Router：四门管线

| 门 | 检查 | 出口 |
|---|---|---|
| Gate 1 | 规格 AI 就绪度 | FAIL → 退回 spec 作者 |
| Gate 2 | ADaM 类别 | 路由到领域 Skill（ADSL/BDS/Occur/TTE） |
| Gate 3 | 逐变量复杂度（standard / complex / custom）+ 歧义数 | 全 AI 生成 / AI+加强人审 / 人工 QC |
| Gate 4 | 风险级覆写 | 按风险上调路径 |

变量复杂度三分法由作者按 ADaM 规格评审的常见模式**专家定义**（非学习得到）；数据集级路由由「复杂/自定义变量占比 + 标记歧义数」决定。图 2 给出各 Skill 的节点规模：ADSL 31 节点、BDS 21–33、Occur 31、TTE 22。

### 3.4 QC Trace Tree：核心创新，把「先想后写」变成强制工序

**定义**（§3.4 + Appendix D schema）：写代码**之前**必须先产出结构化层级树，每个派生变量一个节点，字段为：`variable_name, spec_ref（规格章节/行）, source_data, logic_steps[], edge_cases[]（含 FLAGGED 状态）, ambiguities[]（待人工解决）, verify_criteria[]（断言）, complexity`。

**三步工序**（Listing 1 + Appendix A prompt 模板）：
- Step 1：产出 Trace Tree（强制结构化输出），prompt 明确 **STOP**——树出来就停，不许顺手写代码；
- Step 2：**人工检查点**——QC 程序员先审树、批准/修改派生计划、解决标记歧义；
- Step 3：从**已批准的树**生成代码，代码注释回链树节点（如 `#[TRTSDT] Step 3: MIN per subject`）。

**论文点明的范式翻转**：传统 code review 要从实现反推意图；Trace Tree 把意图显式声明在前，reviewer 只验证「代码与声明的意图一致」——审查对象从 850 行代码变成 138 个节点的结构化计划。

**Tree 实例**（Listing 1，ADSL 节选，可见其信息密度）：
```
TRTSDT [Spec: 3.1 Row 10] (standard)
|-- Source: SDTM.EX.EXSTDTC
|-- Logic: MIN(datepart(EXSTDTC)) per USUBJID
|-- Edge cases: No EX records -> TRTSDT = missing
|               Partial dates -> FLAGGED (spec silent)
|-- Ambiguities: 1 (partial date handling)
|-- Verify: type=date, TRTSDT<=TRTEDT
```

**prompt 硬约束**（Appendix A，与 ct-base 纪律逐条对应）：
- 规格有歧义 → **FLAG IT**（对应 ct-base §22.1 歧义即停）；
- **Do not invent derivation rules**（不许自造口径）；
- **Do not reference production code or outputs**（规格出发的工程化表述）。

> 值得记录的判断：这篇 2026 年的论文用一套自研框架，独立实证了 ct-base §22.1/§22.2（生成前 HITL gate + 禁 AI 补全口径 + 规格驱动）的必要性——我们不是因为谨慎才这么定，而是因为实践会撞上同一堵墙。

### 3.5 领域 Agent Skills：把 ADaM 类知识固化为四个模板

ADSL Skill v1.0（pop flags/人口学/日期/分组）、BDS Skill v1.0（基线、CHG/PCHG、访视窗、LOCF）、Occurrence Skill v1.0（TRTEMFL、首次发生、自定义查询）、TTE Skill v1.0（事件/删失逻辑、时间计算、STARTDT）。每个 Skill 强制执行四件事：先出树、标全部歧义、带领域断言（如 BDS 验 BASE=AVAL at baseline）、用领域标准代码模式。

Skill 是 prompt 模板 + 领域知识的封装——与 ct- 系列「叶子技能承载领域纪律」的架构同构，可作 ct- 技能分层的外部佐证。

### 3.6 六层验证栈与 22 条 SOP 规则

| 层 | 内容 | 说明 |
|---|---|---|
| 1 语法 | 编译执行无错 | 最弱层 |
| 2 结构 | 输出变量与规格元数据一致 | 「列齐」层 |
| 3 数值 | 与 ground truth 逐记录比对 | 「值对」层 |
| 4 属性断言 | 领域逻辑检查（TRTSDT≤TRTEDT、BASE=AVAL@baseline、CNSR∈{0,1}） | 可信度最高层 |
| 5 规格追溯 | 每个派生链接回 Trace Tree 节点 | 可审计性层 |
| 6 自动 Code Review | 静态扫描 7 类 SOP 22 条规则 | 纪律层 |

Code Review 引擎是作者自研的临床编程专用静态分析工具。附录 B 公布的部分规则（完整 22 条见原文）：

| 规则 | 严重度 | 内容 |
|---|---|---|
| HC-001/002/004 | HIGH | 硬编码受试者 ID / 日期 / 文件路径 |
| HC-005 | LOW | mapping 外的 magic number |
| TR-002 | HIGH | Trace Tree 覆盖率 <30% |
| ST-002 | MED | 函数 >80 行 |
| DI-001 / DI-005 | MED / LOW | merge 后无验证 / inplace=True 变异 |
| CL-001 | — | 人群 flag 顺序 |
| CL-002 / CL-003 | CRIT | CHG 先于 BASE 派生 / 发生标志先于 TRTEMFL |
| CL-005 | HIGH | **ground truth 数据泄漏** |

---

## 四、实证结果细读

### 4.1 评测环境：eSubmission Benchmark（CDISC CDISCPilot01 衍生的监管提交包）

- 阿尔茨海默病试验，三臂：安慰剂 N=86、Xanomeline 低剂量 N=84、高剂量 N=84；**254 ITT**（306 总入组 − 52 筛选失败）；
- 5 个 ADaM 域：ADSL（254 条 / 49 变量）、ADAE（1,191 条）、ADADAS（12,463 条 / 15 参数）、ADLBC（37,132 条 / 18 参数）、ADTTE（254 条 / 1 参数）；
- 对照基准：经验证的 ADaM XPT（安慰剂组平均年龄 75.21，SD 8.59）。

### 4.2 路由结果（Table 2）

| 数据集 | Skill | 节点 | 标准 | 复杂/自定义 | 歧义 | 路由 |
|---|---|---|---|---|---|---|
| ADSL | ADSL | 31 | 26 | 5 | 6 | **AI + 加强人审** |
| ADAE | Occurrence | 31 | 29 | 2 | 2 | 全 AI 生成 |
| ADTTE | TTE | 22 | 22 | 0 | 1 | 全 AI 生成 |
| ADLBC | BDS | 21 | 19 | 2 | 0 | 全 AI 生成 |
| ADADAS | BDS | 33 | 31 | 2 | 2 | 全 AI 生成 |
| **合计** | | **138** | 127 | 11 | **11** | 4/5 全 AI |

ADSL 被路由至加强审核，原因是 5 个复杂/自定义变量（RACEN 编码、WEIGHTBL 基线选择、MMSETOT 派生、EFFFL 定义、SITEGR1 站点合并）+ 6 处歧义。路由判断与后验失配高度吻合：ADSL 失配的 3 个变量全部在这 5 个名单里——**路由在「不完美变量」上的命中率是 3/3**。

### 4.3 变量级匹配率与每个失配的根因（Table 3）

| 数据集 | 记录 | 比对变量 | 均值 | 完美变量 | 最低单变量 |
|---|---|---|---|---|---|
| ADSL | 254 | 27 | 99.6% | 24/27 | 93.7% |
| ADAE | 1,191 | 10 | 99.9% | 7/10 | 99.5% |
| ADTTE | 254 | 6 | **100.0%** | 6/6 | 100.0% |
| ADLBC | 37,132 | 5 | 99.2% | 4/5 | 96.2% |
| ADADAS | 12,463 | 6 | **97.1%** | **2/6** | **90.9%** |

逐个失配的根因（论文逐一点名，无一带过）：

| 变量 | 匹配率 | 根因 |
|---|---|---|
| WEIGHTBL (ADSL) | 93.7% | 基线访视选择歧义（spec 未定义哪个访视算基线） |
| BMIBL (ADSL) | 97.2% | 从 WEIGHTBL 级联出错 |
| DCSREAS (ADSL) | 98.8% | 标题大小写映射（title-case mapping） |
| TRTEMFL (ADAE) | 99.5% | 6 条记录的部分日期处理差异 |
| ANRIND (ADLBC) | 96.2% | 编码约定差异：N/H/L vs NORMAL/HIGH/LOW |
| AVISITN (ADADAS) | 90.9% | 访视窗映射规则的理解偏差 |
| ANL01FL (ADADAS) | 92.5% | 同上 |

**三个必须看穿的读数**：① 全部失配根因都是**规格歧义/编码约定**，不是 AI 算错数——而且 11 处歧义在**生成前**已被 Trace Tree 标记；② 均值掩盖分布：ADADAS 均值 97.1% 但只有 2/6 变量完美，是双峰而非均匀高；③ ADSL 的 3 个失配变量 100% 落在 Router 点名的高复杂度名单里。

### 4.4 13 项属性断言全部通过（Table 4）

无重复 USUBJID、TRTSDT≤TRTEDT、SAFFL=Y→TRTSDT 非缺失、三组 N=86/84/84、总受试者=254、ADAE 记录数=1191、每受试者最多 1 条 AOCCFL=Y（218 通过）、CNSR∈{0,1}、AVAL≥1、每受试者 1 条 TTE 记录、事件+删失=总数、BASE=AVAL@baseline（4,527 条）、CHG=AVAL−BASE（7,829 条）——**13/13 PASS**。

### 4.5 时间账：84 分钟里 55% 是人（Table 5）

| 数据集 | Trace Tree | 人审 | 代码生成 | 验证 |
|---|---|---|---|---|
| ADSL | ~3 min | ~15 min | ~4 min | ~2 min |
| ADAE | ~3 | ~8 | ~3 | ~2 |
| ADTTE | ~2 | ~5 | ~2 | ~1 |
| ADLBC | ~2 | ~8 | ~3 | ~2 |
| ADADAS | ~3 | ~10 | ~4 | ~2 |
| **合计** | **~13** | **~46** | **~16** | **~9** |

端到端约 **84 分钟**：AI 计算（树 13 + 代码 16 + 验证 9）约 38 分钟，**人审树与解歧义 46 分钟（≈55%）**；歧义变量迭代再加 10–15 分钟。对照组是「熟悉 CDISCPilot01 的从业者估计手工 QC 需 3–5 人日」——单次通过流程 vs 3–5 人日，论文自己也注明「研究间不可直接比」。

### 4.6 Code Review 207 项与 CL-005 数据泄漏案（Table 6）

| 类别 | 数量 | 最高严重度 | 内容 |
|---|---|---|---|
| STRUCTURE | 138 | MEDIUM | 函数长度/嵌套深度（derive_adsl 达 112 行，超 80 行上限） |
| HARDCODING | 36 | MEDIUM | magic number/硬编码值 |
| DOCUMENTATION | 13 | LOW | 缺 docstring/版本信息 |
| DATA_INTEGRITY | 11 | MEDIUM | 无验证 merge、fillna |
| MAINTAINABILITY | 8 | LOW | 未用 import、重复 lambda |
| CLINICAL_LOGIC | **1** | **HIGH** | **CL-005 ground truth 泄漏** |

**CL-005 案是全篇最有教学价值的单点**：`qc_adsl.py` 为了推导 SITEGR1 的站点合并规则，**读取了 ground truth ADSL 数据集**——因为规格没给合并阈值，agent 就从「已有数据」里反推。论文原话：隔离屏障在生产里会阻止这件事；在基准环境里 ground truth 就在手边，正是 Code Review 引擎要抓的那类独立性违背。**一个让 QC 程序读答案的 bug，被静态分析自动抓到**——人工 review 未必看得住。

HARDCODING 的 36 项里多数是把规格章节号（如 "3.1"）误判为 magic number——论文大方承认是** predominantly false positives**，给出 spec-reference allowlist 的缓解，并说明各组织可按自家 SOP 调严重度。这种「报误报率」的做法本身就是工程质量信号。

---

## 五、批判性评估：六个真问题

### 5.1 路由失准（作者自曝，含金量最高的自我批评）

ADADAS 拿到全场最低匹配率（97.1%，AVISITN 90.9%）却与 100% 的 ADTTE 同路「全 AI 生成」。作者复盘：**LOCF 插补 + 非平凡访视窗**的复杂度没被逐变量计数捕获，路由阈值需要重校——「带 LOCF 和复杂访视窗的数据集即使逐变量复杂度看起来低，也应加强审核」。路由是安全关键组件（决定人盯哪），一次失准直指阈值是专家拍脑袋、无校准曲线。

### 5.2 同模型偏差：房间里的大象，作者没解，只承认

生产与 QC 共享同一模型权重 → 系统性误读相关 → N-version 共因故障的 AI 版。论文的处置是「人是唯一独立层」+ 审计日志，**没有任何技术缓解**（如双模型异构生成）。这是框架无法自我修复的结构性缺口，只能靠人的覆盖率兜底——而人的覆盖率本身没有度量。

### 5.3 「验证」测的是保真度，不是检出能力（本分析补充，论文未明确回答）

六层验证里最强的数值层是「与 ground truth 逐记录比对」——**ground truth 只在基准/已验证研究里存在**。生产里没有 ground truth，等价物是「QC 输出 vs 生产输出」，那测的是**一致性**，不是**正确性**：如果生产和 QC 用同一个模型把同一处 spec 误读成同一个错（5.2），两层输出完全一致、比对全绿、断言也可能照样过（断言测的是逻辑自洽性，不测 spec 解读对不对）。**本基准里也没有注入故障实验**——13 项断言全过，但没有任何一项测试「AI 能否抓住一个被故意写错的生产程序」。对照上周登记的 CAVE-Onc（20 类注入矛盾全检出）补上了这块：AI-201 证明的是「AI QC 生成保真」，CAVE-Onc 证明的是「AI 校验有检出」——**两者合起来才是可用的 AI QC，缺一不可**。

### 5.4 单基准、单模型、无统计学家（作者自曝）

作者自列 8 条局限，其中第七条罕见且重要：**没有统计学家参与**（"did not include a statistician as a co-author"），建议未来评估接受正式统计审阅。实际后果：97.1%–100% 没有置信区间、复杂度分级没有 inter-rater 可靠性、84 分钟 vs 3–5 人日不是受控比较（靠「熟悉该数据集的从业者估计」）、全篇只用一个模型（Claude）一次基准、规格 5/6 就绪度——泛化到「1000+ 受试者、规格脏、含自定义域/整合摘要」的真实世界未经测试，作者要求 multi-study pilot 后才谈生产就绪。

### 5.5 工程环境摩擦：Python vs 受监管的 SAS 世界

QC 代码用 Python/pandas（论文称为可及性与快速原型选择）。图 1 的框图标的是 "Production SAS Code"/"QC SAS Code"，正文 §4.6 却说全是 Python——**图与文自相矛盾**，是一处小的编辑瑕疵，但也侧面说明该框架产出的不是提交级 SAS。在多数药企受控环境里，Python 进提交链路仍有验证/资格认证门槛；若强制 SAS 生成，保真度是否维持未测。

### 5.6 控制强度的两处宽松

TR-002 把「Trace Tree 覆盖率 <30%」定为 HIGH——**为什么是 30% 而不是 100%？** 规格追溯层（第 5 层）本应是全量回链，30% 阈值放行了 70% 无追溯的派生，与「每个派生链接回树节点」的设计初衷存在张力。另外 22 条规则里 CRIT 级的 CL-002/CL-003（CHG 先于 BASE、发生标志先于 TRTEMFL）在 207 项发现里**一条都没触发**——是代码真的干净，还是规则集没吃透 AI 的出错姿势，无从判断。

## 六、对 ct- 技能族的九条可落地借鉴

| # | 借鉴点 | 落点技能 | 具体动作 | 优先级 |
|---|---|---|---|---|
| 1 | **基础设施级隔离** | ct-sdtm / ct-adam | QC/校验路径的生成器禁用生产输出与日志（引擎层拦截，非 prompt 约束）；已有 §22.10 规范层，需落实例隔离清单 | P0 |
| 2 | **Gate 1 规格就绪度六项评分** | ct-sdtm / ct-protocol / ct-adam | 生成前给规格打六项 checklist 分；未达标→拒绝生成并退回规格作者（谁的事谁补） | P0 |
| 3 | **Trace Tree 三步工序** | ct-adam（ADSL 先行试点） | 采用 Appendix D schema；树→人审→代码，STOP-after-tree 写进 prompt 模板；代码注释回链节点 ID | P0 |
| 4 | **第 5 层规格追溯升格为验收层** | ct-sdtm / ct-adam / ct-tlf | 现有 L1/L2/L3 之外补「派生↔规格/树节点」双向链接；覆盖率应 100% 而非 30% | P1 |
| 5 | **路由特征修正 + 阈值校准** | ct-adam | Router 特征必须含 LOCF/访视窗/插补规则（ADADAS 教训）；用留出错误模式集校准阈值，报告校准依据 | P1 |
| 6 | **22 条 SOP 规则移植** | 全族编程技能 | HC-001/002/004、ST-002(80行)、DI-001、CL-001/002/003、CL-005；配 spec-reference allowlist 压误报（论文实证 36 项里多数是误报） | P1 |
| 7 | **CL-005「读答案即泄漏」检测** | ct-sdtm（合成数据）/ ct-adam（repro-check） | QC/合成生成器引用基准输出/答案数据 = HIGH 一票否决——ct-sdtm 合成参数若从目标数据集反推即同罪 | P0 |
| 8 | **影子模式先行 + SAP 登记** | ct-statrev / ct-advisor | 采纳论文建议 #5：AI QC 与传统 QC 并行跑影子；SAP 审查新增登记项：模型版本、skill 版本、code review 规则集版本 | P1 |
| 9 | **失配归因纪律** | 全族 | 每个残余失配必须归因到 spec 歧义/引擎 bug/数据问题三类之一；「生成前已标记」作为最高可追溯标准（论文 11/11 达成） | P1 |

与 ct-base 的关系说明：本论文的 Appendix A prompt 约束（歧义 FLAG / 禁自造口径 / 禁引生产输出）与 ct-base §22.1/§22.2 纪律逐条同构——**§22 体系不是过度谨慎，而是被这篇独立实证的工程实践反向验证**。建议将本分析挂到 §22.10–§22.14 的引用链上（证据登记文件已更新）。

## 七、总评

这篇论文的贡献排序（个人判断）：**CL-005 泄漏检测 > Trace Tree 工序 > 路由 + 隔离架构 > 数值保真结果**。前两项是可移植到任何 LLM 生成管线的「纪律资产」，第三项是框架骨架，第四项虽有媒体价值但受 5.3/5.4 的读数限制。它对 ct- 族最大地说服力在于：**一个真正跑在生产逻辑上的团队，最终把最重的信任押给了「生成前的人工检查点」和「读答案即一票否决」这两件最不 AI 的事**——这正是 ct-base §22 把 HITL gate 和反泄漏写成红线的外部实证。

**使用建议**：作为 ct-adam 的 AI QC 引擎设计蓝本读取（含可直接抄的 Appendix A prompt 模板与 Appendix D schema），但不要引用其 97–100% 作为「AI QC 可靠性」的论据——那是保真度指标；可靠性的证据要等 CAVE-Onc 式的注入故障实验出现后合并呈现。
