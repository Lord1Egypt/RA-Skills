# 已分析论文登记册（living registry）

> 单一事实来源：记录所有被评估并提议纳入 ct 系列的**外部论文 / 文章 / 工具介绍**。
> 维护规则：新论文评估完毕追加一行（**倒序，最新在上**）；只记结论与落地改进项，详细评估见各技能 CHANGELOG 与工作区日志。
> 评估方法论见 `docs/12-paper-improvement.md §21`；新评估填写模板见 `references/paper_eval_template.md`。

---

## 登记册

### 2026-10-19 · PharmaSUG 2026 AI-201 独立 QC 框架 + GxP-Agent 验收实证 + MIRROR / VALIDATE / LLM 靶向 QA / RAG 合规检索 / ClinAgent（情报周报第 4 轮）
- **来源**：微信公众号「林少楠 GCP」《那些探索AI临床试验的人们》（2026-10-08，搜狗深读）+「AI药研新社」《AI正在重做药企的工作：从找资料，到交付结果》（2026-10-15，搜狗验证码降级 WebSearch 取全文）+ PharmaSUG 2026 官方 proceedings PDF（AI-201 官方原文）+ 论文通道 4 query 120 条去重 + OA 深读（medRxiv / arXiv / BMJ Open / npj Breast Cancer(nature 页被 Cloudflare 拦，WebSearch 降级补全)）。全链可溯源。
- **主题**（最核心为前两组）：① **PharmaSUG 2026 AI-201**（Yan & Zhang, Merck）——用**操作隔离的双 AI 实例**从规格独立生成 QC 程序：QC Trace Tree（生成前可审计推理树）+ Decision Router（按复杂度路由）+ 领域 Agent Skills + 自动 Code Review 引擎；CDISC CDISCPilot01（254 受试者/5 ADaM 域）**变量级匹配率 97.1%–100%、138 节点/51,294 记录、13 项断言全过；ADSL 因复杂度路由至加强审核；自动审查 7 类 SOP 207 项发现含 1 高危数据泄漏；残余不一致全溯源到规格歧义**。QC 编程占总编程量 30–50%。② **GxP-Agent**（arXiv:2608.16890）——ADSL 生成 DAG 拆 15 节点；Sonnet×3+Opus×1 运行 **100% 结构匹配但列级值匹配率平均仅 73.7%**。③ CAVE-Onc（PLOS ONE）——20 类已知注入矛盾全检出，规则冻结后新增 5 类仅检出 3 类。④ MIRROR（npj Breast Cancer, DOI `10.1038/s41523-026-01060-6`）——AI 从 EHR 抽取 vs 人工 eCRF（113 例/11 试验），每变量回链原文引用，多数变量 ≥80% 有效，非结构化是短板。⑤ VALIDATE（BMJ Open, DOI `10.1136/bmjopen-2026-120511`）——锁定模型影子模式 + 四阈值 go/no-go（SUS≥68/失败率≤10%/时钟窗≤25min/AUROC≥0.75）。⑥ LLM 靶向 QA（medRxiv, DOI `10.64898/2026.09.22.26363595`）——用分歧度排序替代随机抽 <10%（ER 1.67%/Ki-67 9.18%/PSA 17.28%），记录 model/prompt/pipeline 版本。⑦ Waikar et al. RAG 合规检索（CPT:PSP, DOI `10.1002/psp4.70201`）——**漏掉方案主要终点、带入不适用要求**。⑧ ClinAgent（Biol Methods Protoc, DOI `10.1093/biomethods/bpag032`，超窗口溯源所得）——确定性层零假阳性 vs 规格生成 72.1%（复杂域 <55%）。
- **最相关技能**：ct-sdtm（高）/ ct-adam（高）/ ct-tlf（高）/ ct-csr（中高）/ ct-statrev（中高）/ ct-advisor（中高）/ ct-literature（中）/ ct-ecrf（中高）/ ct-samplesize（中）/ ct-analysis（中）/ ct-base（高，规范层）；ct-datacheck（高）**本轮排除**——另一任务正在修改该技能，涉及项等用户确认后单独实施。
- **结论**（高·多源交叉精读）：工业界已把「AI 生成资产」从"LLM 直出"推进到**"隔离实例 + 可审计推理前置 + 复杂度分级 + 分层验收"**的工程范式；三个可量化硬事实重塑验收口径——**L1 结构 100% ≠ 验收通过（列级值 73.7%）、规则覆盖已知 ≠ 泛化（新增类仅 3/5）、RAG 引用 ≠ 覆盖（漏主要终点）**。与 2026-10-18 CDISC 2026 情报互为正反两面：前者证明"合规形态可行"，本轮证明"验收必须分层且批判性外推有限"。
- **落地改进（本次已执行规范层，2026-10-19；引擎改造列 🔴规划，等确认）**：
  - **ct-base §22 增补 8 条纪律（v1.4.0）**：§22.10 P0·c 独立 QC 操作隔离+规格出发 / §22.11 P0·d 结构+列级值双层验收 / §22.12 P0·e QC Trace Tree 前置 / §22.13 P1·e 复杂度路由 Decision Router / §22.14 P1·f 自动 Code Review SOP 前置扫描 / §22.15 P1·g 影子模式 go/no-go 量化阈值（Control Mode 准入）/ §22.16 P1·h RAG 三列待核对清单 / §22.17 P2·a 确定性层 vs LLM 层分层验证
  - **可复用资产**：`references/qc_independence_pharmasug2026.md`（九组外部证据登记 + 研究地图速查）入 SHARED_ASSETS 白名单，随发布下沉
  - **叶子适配**：ct-sdtm v2.5.0（7 义务行）/ ct-adam v0.7.0（5）/ ct-tlf v0.8.0（3）/ ct-csr v0.5.0（2）/ ct-advisor v1.3.15（2）/ ct-literature v1.4.10（治理段）/ ct-statrev v0.7.0（1）/ ct-ecrf v0.2.2（证据锚点+非结构化降级）/ ct-samplesize v5.13.14 + ct-analysis v0.6.0（RWD 分布平衡 DBML 报告义务）；各仓库 CHANGELOG 同步，本地提交零推送
  - **未实施（等确认）**：ct-datacheck 专项 §22.16-adjacent 靶向质控 + 留出错误模式基线（另一任务在改）；全部引擎层实现（qc_independent_gen.py / Trace Tree / SOP 扫描 / DBML 引擎 / MIRROR 式锚点抽取）均列 🔴规划
- **不照搬**：AI-201 的商业 LLM 部署形态（Merck 自管 AWS + Claude）；GxP-Agent 预印本身份（未期刊复核的结果仅作范式不作基准）；RAG PoC 的漏项场景照抄为测试用例而非结论

### 2026-10-18 · CDISC 2026 AI 创新挑战（赛果 + 唯一开源投稿 Appsilon 源码级深挖）
- **来源**：公众号解读文「老白的AI实践」《CDISC 2026 AI 挑战结果出炉…》（2026-10-15，链接已过期）+ CDISC 官方结果页 + LinkedIn 详述 + **唯一开源投稿 Appsilon `cdisc-case-1`（含 `synthsdtm` R 包）/ `mediforce` 已 `git clone` 逐文件读源码**（置信度高）
- **主题**：6 个获奖方案（Novartis+AWS Syn2Real/PAIR、Saama Smart ClinSAP、Jazz SAP-Genie、Zifo TLFGenix、BioInformatiCo Leova）中唯一开源的 Appsilon 投稿，把"AI 到底做了哪一步"拆干净——**LLM 只做配置（判断哪些域+检测面板），真正生成数据的是确定性 R 包 `synthsdtm`（固定 seed 逐字节可复现），人类审查 gate 在生成之前**；Mediforce 提供 Control Mode（CM0–CM4）+ ALCOA+ 审计（actor/timestamp/snapshot/basis/processDefinitionVersion）。
- **最相关技能**：ct-sdtm（高）/ ct-adam（高）/ ct-tlf（高）/ ct-csr（高）/ ct-datacheck（高）/ ct-advisor（高）/ ct-statrev（中高）/ ct-base（高，规范层）
- **结论**：印证并具体化"AI 生成临床数据"的合规形态 = 确定性引擎 + 固定 seed + LLM 只喂受约束配置 + 风险点人工 gate + ALCOA+ 审计；直接命中上一轮周报 P0。6 方案真正高价值在"AI 知道何时该停"，而非生成速度。
- **落地改进（本次已执行 P0/P1，2026-10-18）**：
  - **P0**：新增 ct-base §22「AI 生成资产治理」全规范（docs/13-ai-generation-governance.md），将"歧义即停"HITL 闸门 + 确定性生成+固定 seed 两条 P0 纪律固化为全库统一红线
  - **P1**：§22 同时固化三层合规检查（T1/T2/T3）+ LINEAGE + 可复现、标准工件版本 pin + CT 离线快照、ALCOA+ 审计 + 工作流版本锁定、Control Mode 自治阶梯（CM0–CM4）四条 P1 纪律
  - **P1**：新增可复用资产 `assets/audit_event.schema.json`（ALCOA+ 审计事件 schema）+ `assets/artifact_version_pin.schema.json`（标准工件版本 pin 清单）
  - **P1/B**：ct-sdtm / ct-adam / ct-tlf / ct-csr / ct-datacheck / ct-advisor / ct-statrev 七技能 SKILL.md 追加「AI 生成治理（ct-base §22）」适配段落，明确各自承担的闸门/确定性/QC/版本pin/审计/控制模式义务与状态
  - **参考文献**：本分析全文入库 `references/cdisc2026_ai_challenge.md`，并加入 `scripts/publish_inject.py` SHARED_ASSETS 白名单（随叶子技能发布自动下沉）
- **未照搬**：`synthsdtm` 的 AEDECOD 无 MedDRA 透传原词 stopgap（抄架构不抄该缺口）；闭源方案的商业能力描述（看不到实现）；SAP 生成赛道待 Jazz SAP-Genie 开源再对标

### 2026-10-14 · Pinnacle 21 Community 1.0.9（OpenCDISC Validator 延续）验证引擎逆向分析
- **来源**：本地安装 `C:\Users\WintoneFileSrv\AppData\Local\Programs\Pinnacle 21 Community\`（Electron 外壳 + 随包 JRE 8 + `p21-client-1.0.9.jar` 核心引擎）；用 REA 技能 + 应用自带 JRE 运行 CFR 反编译，逆向其受控术语与规则引擎。遵循 ct-base §6.1：仅借鉴结构模式，规则文本与术语值仍以 CDISC 官方源为准。
- **主题**：CDISC 标准验证引擎架构——受控术语分**封闭码表（closed）**与**可扩展码表（extensible）**；规则以可执行算子表达（Find/Lookup/Unique/Required/Regex/Match/Property/Metadata/Varlength/Varorder/Define/Condition）；每条规则带 PublisherID 映射 CDISC 官方规则编号。
- **最相关技能**：ct-sdtm（高）/ ct-datacheck（高）/ ct-base（高，规范层）
- **结论**：印证并具体化 ct-sdtm 受控术语校验方向；关键增量是「CT 可扩展性二分」与「规则算子化 + PublisherID 溯源」，正对 ct-base §17.3 合规规则库与 §6.1 溯源硬规则。
- **落地改进（本次已执行 P1，2026-10-14 追加 B3/B4/B5）**：
  - ct-base §17.3 新增「受控术语可扩展性二分」原则（A1 方案）
  - ct-sdtm `references/ct_codelists.json` 顶层新增 `extensibility` 块（33 码表：23 closed / 7 extensible / 3 unknown；值集仍以 CDISC v3.4 聚合为准）（B1 方案）
  - ct-sdtm `scripts/term_check.py` 按可扩展性分流严重级：closed=Error、extensible|unknown=Warning，新增 `--strict`（B2 方案）
  - ct-sdtm `references/core_rules_cache.json` 每条规则新增 `publisher_id` 字段，指向 CDISC 官方规则集（CG=General 一致性规则；SDTM_V2_0=SDTM and SDTMIG Conformance Rules v2.0），与 P21 `RuleMetadata.publisherId` 同构，完成 §6.1 溯源结构（B3 方案）
  - 同文件新增 `scope` 字段（record / dataset），落地 P21 双 Scope 模型：7 条 dataset 级（001/002/003/004/005/034/040）+ 33 条 record 级（B4 方案）
  - 同文件 `check_type` 对齐 P21 算子命名（required/unique/lookup/match/condition/property/varlength/regex/metadata），与 12 算子映射一致（B5 方案）
  - 产出算子对照分析：`p21-analysis/P21算子与ct-sdtm合规检查对照.md`——确认 12 算子中 11 个已在 ct-sdtm 有对应实现，仅 Varorder 缺失；并给出「接入 Define(value_level_rules)」「采纳 Varorder」「抽取可复用 Condition 算子」「回填 publisher_id 精确 CDISC 规则号」4 条改进建议
- **2026-10-14 续作（P1+P2 已落地 + 11 算子正确性审计）**：
  - **P1 Define 接入**：`ct-sdtm/scripts/sdtm_validate.py` 新增 `check_value_level`（Define/ValueListDef 等价算子，功能等价独立代码），按 `value_level_rules.json` 的 where 子句（具体值优先于通配 `*`）校验值级受控术语 → `CG.VAL.VL-CT`(Error)，占位 CodeList 如 (LAB_UNIT)/(VS_UNIT) 按自由单位跳过；已接入 `validate_dataset`。
  - **P1 Varorder 采纳**：同文件新增 `check_var_order`（Varorder 等价算子），比对列相对顺序 vs SDTMIG 参考顺序，偏离 → `CG.VAL.COL-ORDER`(Warning)；已接入 `validate_dataset`。此前 12 算子缺的 Varorder 已补齐。
  - **P2 Condition 抽取**：`ct-sdtm/scripts/sdtm_build.py` 新增复用 helper `_cond_required`（Condition 等价；when_vals=None=when_var 非空即触发 / when_vals={..}=精确匹配）；CORE-009/025/028 三处硬编码 if 改为复用，issue 输出与重构前一致。`scripts/` 与 `workbench/publish/scripts/` 两份同步。
  - **P2 publisher_id 回填就绪**：`core_rules_cache.json` 每条规则新增 `cdc_rule_id`(null，预留精确 CDISC 编号槽) + `publisher_id_status`("family-root")；metadata 增 `cdc_rule_id_backfill` 说明回填须自 CDISC 官方 conformance-rules 导出、**严禁臆造具体编号**（合规红线）。`publisher_id` 规则集族(CG/SDTM_V2_0)保持正确。
  - **11 算子正确性审计**：产出 `p21-analysis/P21算子正确性审计.md`——逐算子比对 P21 语义与 ct-sdtm 实现，结论 10/11 正确，发现 **CORE-002 P0 缺陷**（USUBJID 重复误报 Warning，受试者标识单域多行重复为常态，近乎全量误报）。
  - **CORE-002 缺陷修复**：改为 Required 语义（仅查 USUBJID 缺失→Error），移除 n>1 误报；同步缓存中 CORE-002 的 check_type(unique→required) 与 rule 文本。功能测试验证重复 USUBJID→0 误报 / 空 USUBJID→命中。
  - 验证：`py_compile` 通过；值级 CT / 列序 / Condition / CORE-002 回归全绿；`scripts/` 与 `workbench/publish/` 两份 sdtm_build.py / sdtm_validate.py / core_rules_cache.json 均 byte-identical。
- **未照搬**：XML 规则格式（与 B 档零依赖冲突）；12 算子全量移植（现有 check_type 分类标签已够用，避免过度工程）；P21 规则文本 / 术语值（受 Pinnacle 21 LLC 版权约束，依 §6.1 以 CDISC 官方源为准）；**具体 CDISC 规则号（CG00xx/FDAB017）未臆造**，仅回填规则集族溯源**

### 2026-10-06 · PharmaSUG 2026 AI-125「GenAI 进 ADaM 编程」
- **来源**：微信公众号解读文 `https://mp.weixin.qq.com/s/pjjTNThd6bIlxEe0mEXRfA`（已精读，置信度高；主题经 AI-125 论文内容核对）
- **主题**：用 GenAI + AWS Bedrock 增强 ADaM Spec 验证与 SAS 代码开发（Spec 验证前移 → 变量级生成 → 程序整合；raw/polished 双版；ToDo 占位符；JSON 结构化协议 + 多级兜底；自适应分块；治理留痕清单）
- **最相关技能**：ct-adam（高）/ ct-sdtm（中高）/ ct-tlf（中，上游质量）
- **结论**：印证并具体化用户 10-05 修正「LLM 自由生成可采纳但须标识」（与 ct-base §6.9 同源）；raw/polished 双版=留痕+标识工程实现，ToDo 占位符=把不确定留给人。
- **落地改进**：
  - ct-base §5 新增「出站上下文脱敏 — 内部规则与敏感示例值剔除」红线（D 方案）
  - ct-adam `AI_ADAM_GENERATION_DRAFT.md` 工程模式草稿（E 方案，强制绑定 §6.9 + §5）
- **未改动**：§6.9 无需改（论文仅印证）

### 2026-10-05 · PharmaSUG China 2026 AI201「ADaM2TFL」
- **来源**：论文 PDF（用户分享，已精读全文 6 页，置信度高）；公众号解读文 `https://mp.weixin.qq.com/s/QDrt1P9CJhk3enPn4x4Neg`
- **主题**：LLM-native TFL 自动化架构（compact skill file 喂上下文 + 可复用确定性工具 + agent 生成候选 R 程序；五阶段 Init→Parse(人工确认门)→Cache(源哈希/新鲜度)→Generate→Verify(结构检查)；6 设计模式；知识积累循环仍实验性）
- **最相关技能**：ct-tlf（高）/ ct-base（高，方法论）
- **结论**：方法论印证 > 新增能力；指出 ct-tlf 两缺口（ADaM 源完整性闸门、失败知识库模板）；论文自身定位探索性原型、强调「模型不是完整方案」。
- **落地改进**：
  - ct-base §6.9「AI 生成物标识与人工确认门」红线（A 方案，同步 AGENTS.md §4.1 + docs/03 §6.9）
  - ct-tlf v0.5.0 ADaM 源完整性闸门（B 方案：tlf_build.py + pub_tables.py 源指纹缓存 + 产物 `_source_fingerprint`）
  - 用户修正采纳：「LLM 自由生成代码可考虑，但需对结果明确标识」
- **未照搬**：不让 LLM 自由生成 R 程序（B 档可复现红线）；不引入 Word shell 解析（ct-tlf 用 r4csr mock shell 本地内置）

### 2026-10-05 · 微信公众号 gtsummary 介绍文
- **来源**：`https://mp.weixin.qq.com/s/3cdDYhEVKZlmP-nd3YT38A`（已读，置信度高）
- **主题**：gtsummary R 包（基于 gt）——医学期刊投稿表（Table 1 基线 + 自动 P 值 / 回归表 OR·HR+95%CI / 生存表；JAMA/Lancet/NEJM 主题；导出 docx/xlsx）
- **最相关技能**：ct-tlf（中，出表技能）
- **结论**：不适合作 ct-tlf 监管 TLF 核心（缺 RTF / 期刊主题哲学 / opinionated 默认检验 / 加 R 依赖）；但暴露「把 ADaM 转成投稿论文表」的真实缺口。
- **落地改进**：
  - ct-tlf v0.4.0 模块 H「期刊发表表」（gtsummary 可选 R 引擎，与监管核心严格隔离；边界声明非监管 RTF、方法学诚实声明）
- **未照搬**：不并入监管核心（A 方案守红线，B 方案补缺口）

---

### 2026-10-11 · Clarity 解读（PharmaSUG China 2026 AI175《Clarity》）
- **来源**：微信公众号解读文 `https://mp.weixin.qq.com/s/adXWvIgE9gb1MdAD8cfLIw`（已精读，置信度中高；主题经论文标题/机构 BeOne Medicines 核对）
- **主题**：基于 R Shiny 的 NL→临床分析工具；核心四件套=分析技能库 + 数据集元数据（只发结构不发值）+ 执行前安全硬检查 + 真实报错回传；强调「每次只注入一份分析规范」「上下文不是越多越好」「Prompt Tips 帮用户把问题说完整」「透明可查可导出」
- **最相关技能**：ct-base（高，方法论）/ ct-analysis（中高）/ 全库（中）
- **结论**：Clarity 范式（技能库+元数据+安全检查+报错回传）正是 ct-base 已采用且更工程化的方向；文章价值在外部佐证 + 几个可落地工程细节，而非新范式。ct 已领先点：工程化治理/默认离线/完整双语/发布自包含。
- **落地改进（本次已执行 P0/P1）**：
  - P0 ct-base `r_libs.scan_forbidden_ops()` 本地 R 代码运行前禁止操作黑名单扫描（纵深防御，对应 Clarity §05）+ AGENTS.md §4 红线补条
  - P1a 新增 `references/prompt_tips.md`（用户侧请求模板，与 search_menu.md agent 侧互补）
  - P1b AGENTS.md §2 补「定点修复 + 停止条件」纪律
- **未照搬**：患者级数据不出本地（ct 已更严，B 档 network:none）；确定性+YAML 路由（ct-advisor 已践行）；会话→报告组装/6 项 DQ 前置（留作 P2）

## 统计

- 已评估：6 项（4 篇论文 + 1 个验证引擎逆向分析 + 1 个竞赛开源投稿源码深挖；全部高置信，其中 2 篇已精读原文 PDF、1 个已 clone 读源码）
- 已落地改进：ct-base §5+§6.9 红线；ct-tlf v0.4.0 模块 H + v0.5.0 源完整性闸门；ct-adam AI 生成 ADaM 草稿；ct-base P0 黑名单扫描 + P1 Prompt Tips + 定点修复纪律；**ct-base §17.3 CT 可扩展性二分 + ct-sdtm ct_codelists.json extensibility 块 + term_check.py 严重级分流 + core_rules_cache.json 新增 publisher_id/scope/算子化 check_type（2026-10-14，源自 P21 引擎逆向）**；**ct-base §22 AI 生成资产治理全规范（2026-10-18，源自 CDISC 2026 AI 挑战开源投稿源码深挖）+ 可复用资产 audit_event.schema.json / artifact_version_pin.schema.json + 七叶子技能 §22 适配段落 + 参考文献 cdisc2026_ai_challenge.md 入 publish_inject 白名单**
- 误判撤回：1 次（AI201 延伸阅读标题误当论文内容，10-05 已撤回）
