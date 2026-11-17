# QC 独立性与 AI 生成验收 · 外部证据登记（2026-10-19 情报轮）

> 本文件登记 2026-10-19 情报周报（`reports/wechat_intel_2026-10-19.md，2026-10-13-10-11-50 workspace`）沉淀的外部证据，作为 `ct-base/docs/13-ai-generation-governance.md` §22.10–§22.17 的单一事实来源。已入 `publish_inject` 白名单随技能下沉。
> 检索通道：微信公众号「林少楠 GCP」「AI药研新社」（降级 WebSearch 取全文）+ PharmaSUG 2026 官方 proceedings + medRxiv / arXiv / BMJ Open / npj Breast Cancer OA 深读。

## 1. PharmaSUG 2026 AI-201：独立 QC 程序生成框架（核心证据）

- **出处**：Yan J, Zhang J. *Eliminating QC Programming Duplication Through Claude AI-Assisted Independent Code Generation: A Practical Framework for Regulatory-Compliant Validation*. PharmaSUG 2026, Paper AI-201（`pharmasug.org/proceedings/2026/AI/PharmaSUG-2026-AI-201.pdf`）。
- **问题量化**：QC 编程要求独立重实现生产逻辑，工作量占编程总量 **30–50%**，且 N-version 编程共性是"共享规格的系统性错误"——两套独立程序可因同一份错误规格同时错。
- **框架四组件**（均为作者自研，LLM 仅用 Claude，部署于公司管理的 AWS 基础设施）：
  1. **操作隔离**：生产与 QC 两个完全隔离的 AI 实例——QC 侧无生产代码、无生产日志、无共享对话上下文，由基础设施控制而非提示词自律；
  2. **QC Trace Tree**：生成代码前先产出可审计的推理树（spec 来源 / 派生逻辑 / 边界情况 / 验证状态），使推理透明可审计；
  3. **Decision Router**：按数据集类别、规格质量、复杂度系统选择 QC 路径；
  4. **领域 Agent Skills + 自动 Code Review 引擎**：按 ADaM 类别编码最佳实践模式，对所有生成代码强制执行编程 SOP。
- **量化结果**（CDISC CDISCPilot01 提交包，254 受试者 / 5 个 ADaM 域）：138 个 Trace Tree 节点、51,294 条匹配记录，**变量级匹配率 97.1%–100.0%**，**13 项属性断言全部通过**；Router 判 4/5 数据集可全 AI 生成、**ADSL 因变量复杂度更高路由至加强审核**；自动 Code Review 在 7 类 SOP 中发现 **207 项问题，含 1 项高危数据泄漏风险**；残余不一致全部溯源到**规格歧义**（访视窗口规则、编码约定），且 Trace Tree 在代码生成前即已标记。
- **对 ct- 的映射**：§22.10（隔离+规格出发）、§22.11（双层验收）、§22.12（Trace Tree 前置）、§22.13（复杂度路由）、§22.14（自动 SOP 扫描）。
- **【2026-10-19 PDF 原文深读补遗】**（13 页全文，含附录 A–D 已核验）：
  - 逐变量失配根因：WEIGHTBL 93.7%（基线访视歧义）/ BMIBL 97.2%（级联）/ DCSREAS 98.8%（title-case）/ TRTEMFL 99.5%（6 条部分日期）/ ANRIND 96.2%（N/H/L vs NORMAL/HIGH/LOW 编码约定）/ AVISITN 90.9%、ANL01FL 92.5%（访视窗映射）。ADSL 3 个失配变量 100% 落在 Router 点名的高复杂度名单内。
  - **作者自曝路由失准**：ADADAS 最低匹配率（97.1%）却路由「全 AI 生成」——LOCF + 非平凡访视窗未被逐变量复杂度计数捕获，阈值需重校。路由是安全关键组件。
  - **CL-005 数据泄漏案**（最有教学价值的单点）：qc_adsl.py 读取 ground truth ADSL 反推 SITEGR1 合并阈值（规格未给阈值，agent 从「已有数据」推断）——静态分析自动抓到；论文原话：隔离屏障在生产里本应阻止此事。→ ct-sdtm 合成参数从目标数据集反推即同罪。
  - 效率账：84 分钟端到端，其中人审 Trace Tree + 解歧义 46 分钟（≈55%），AI 计算（树 13 + 代码 16 + 验证 9）约 38 分钟；手工 QC 估计 3–5 人日（从业者估计，非受控）。
  - 22 条 SOP 规则（附录 B）：HC-001/002/004 HIGH、TR-002 覆盖率<30% HIGH、ST-002 >80 行 MED、DI-001/DI-005、CL-002 CHG 先于 BASE 为 CRIT、CL-003 先于 TRTEMFL CRIT、CL-005 泄漏 HIGH；36 项 HARDCODING 多为规格章节号误报（论文承认 predominantly false positives，配 spec-reference allowlist）。
  - 论文六步落地建议：从 TTE/简单 BDS 起步；投资规格质量；Code Review 第一天就上；用 Router 拦复杂活；**先跑影子模式**（AI QC 与传统 QC 并行）；**SAP 里登记模型版本/skill 版本/code review 规则**。
  - 作者 8 条自列局限：同模型偏差（人是唯一独立层，无技术缓解）、树保真度（stated reasoning ≠ 解释保证）、路由需重校、规格依赖、**无统计学家共同作者**、单基准单 LLM（Claude）、真实规格更脏更大未测。
  - **本分析补充的两点批判**：① 数值层验证需 ground truth，生产环境不存在——97–100% 测的是「复现已知正确答案的保真度」而非「检出生产错误的能力」，全篇无注入故障实验（须与 CAVE-Onc 的检出能力证据合并呈现）；② QC 代码用 Python/pandas 而图 1 标注 SAS，图文不一致。
  - 深度分析文档（**ct-base 权威副本** `references/qc_ai201_deep_analysis.md`，随 publish_inject 下沉；原稿在工作区 `reports/pharmasug2026_ai201_deep_analysis_2026-10-19.md`）：Appendix A prompt 模板 / Appendix D schema / 四门 Router / 六层验证栈 / 九条 ct- 借鉴。

## 2. GxP-Agent：结构匹配 ≠ 值正确

- **出处**：Yan J. *GxP-Agent: Process-DAG Topology for Reliable Clinical Trial Programming with LLM Agents*. arXiv:2608.16890（预印本）。
- **方法**：把临床编程流程写成 DAG 工序图，ADSL 生成拆成 15 个节点，每节点设检查与重试。
- **关键警示数字**：公开测试中 Claude Sonnet 3 次运行 + Opus 1 次运行，均覆盖 49 个目标变量、254 条记录数正确（**100% 结构匹配**），但 4 次运行**平均列级值匹配率仅 73.7%**。
- **对 ct- 的映射**：§22.11 双层验收的实证依据——"列齐了、行数对了"绝不可作为通过标准。

## 3. CAVE-Onc：规则覆盖已知、模型兜新，但泛化有限

- **出处**：Yan J. *CAVE-Onc* 跨域矛盾检测研究. PLOS ONE, DOI `10.1371/journal.pone.0350376`。
- **结论**：对 20 类人工预设注入矛盾全部检出（19 类来自确定性规则、1 类来自 Agent）；但**规则库冻结后新增的 5 类错误模式只检出 3 类**。
- **对 ct- 的映射**：验证集须保留"留出错误模式"，分别报告已知覆盖率与新错误检出率，禁止用历史通过率外推泛化能力（涉及 ct-datacheck，本轮仅登记不动手）。

## 4. VALIDATE：影子模式 go/no-go 量化阈值

- **出处**：*Real-time prospective (shadow mode) validation of an AI-based clinical decision support system for predicting...*, BMJ Open, DOI `10.1136/bmjopen-2026-120511`（2026-10-01）。
- **设计**：3 家高水平卒中中心、目标 200 例；模型**已锁定**（研究期间不再训练/再校准），由影子研究员在卒中流程中实时录入，CDSS 后台产出 4 种再灌注策略的 3 个月 mRS 预测，**对治疗医生完全盲态、不进入决策**；随后与实际治疗及真实结局（盲态评估）离线比对。
- **四阈值 go/no-go**（达标才进入介入性 RCT）：**SUS ≥68、技术失败率 ≤10%、中位门到预测时间 ≤25min、AUROC ≥0.75**（优秀目标 >0.85）。系统渗透率 ≥70% 仅为监测项、明确**不作为红灯**（受人力排班制约，非模型不可用）。
- **对 ct- 的映射**：§22.15 Control Mode 升级准入——影子阶段 + 量化阈值 + 熔断。

## 5. MIRROR：EHR→eCRF 抽取的证据锚点

- **出处**：Parra-Calderón CL et al. *Artificial intelligence for clinical data extraction from EHRs in breast cancer trials: the MIRROR study*. npj Breast Cancer, DOI `10.1038/s41523-026-01060-6`（2026-10-07；Nature 全文页被反爬拦截，经 WebSearch 降级补全）。
- **结论**：113 例乳腺癌患者 / 11 项试验，AI 自动抽取 vs 人工 eCRF 录入**多数变量有效率 ≥80%**；系统为**每个变量回链原始文本**便于核查；**结构化字段（日期/性别/实验室值）显著优于非结构化临床笔记**；作者建议各站点推行标准化 eCRF 以保证一致抽取。
- **对 ct- 的映射**：ct-ecrf / ct-sdtm 的 AI 抽取必须携带证据锚点，非结构化来源字段显式降级人工。

## 6. LLM 靶向 QA：用分歧度排序替代随机抽样

- **出处**：*An LLM-Based Auditing Framework for Targeted Quality Assurance in Cancer Registries*. medRxiv, DOI `10.64898/2026.09.22.26363595`（2026-09-23）。
- **结论**：传统 QA 随机抽查 <10% 记录、易漏机构/时间特定错误；框架用 LLM 抽取生物标志物与登记值比对、**只把分歧记录送专家复核**，并按 NAACCR 规则标注可能原因排序。实证：本地隐私环境基准 6 个开源 LLM 并按站点/报告类型选最佳；乳腺癌 1852 例分歧率 ER 1.67%（最低）~ Ki-67 9.18%（最高），前列腺癌 920 例 Gleason 分类 <8%、**PSA 精确值 17.28%**；全年 11,740 例乳腺 + 6,792 例前列腺；**抽取值链接支撑文本，model / prompt / pipeline 版本全记录**。
- **对 ct- 的映射**：涉及 ct-datacheck / ct-statrev，**本轮仅登记不动手**（用户等确认）。

## 7. RAG 合规检索的默认失败模式

- **出处**：Waikar et al. *Retrieval Augmented Generation (RAG) for Evaluating Regulatory Compliance of Drug Information and Clinical Trial Protocols*. CPT: Pharmacometrics & Systems Pharmacology, DOI `10.1002/psp4.70201`（2026）。
- **结论**：概念验证系统将药品资料、试验方案、指南接入 RAG 后生成摘要/评价/待核实问题，**仍漏掉方案的主要终点，并带入不适用的要求**——"带了资料"不等于回答正确。
- **对 ct- 的映射**：§22.16 RAG 输出强制"问题/原文位置/依据"三列待核对清单，"漏项"为默认失败模式须显式检查。

## 8. ClinAgent：确定性层与 LLM 层分开验收

- **出处**：Yan J. *ClinAgent: AI-assisted methodology for clinical trial data processing and statistical programming*. Biology Methods and Protocols, DOI `10.1093/biomethods/bpag032`（2026-06，超情报窗口，WebSearch 溯源所得）。
- **结论**：MCP 工具层 + 9 个 skills 架构；**确定性组件 1 错误 7 警、零假阳性**；**提示词规格生成整体派生准确率 72.1%**（简单域 >96%、复杂域 <55%）——LLM 依赖输出必须分层报告并按域设复核策略。
- **对 ct- 的映射**：§22.17 确定性工具层 vs LLM 依赖输出分层验证。

## 9. 研究地图速查（林少楠 GCP，2026-10-08）

> 公众号《那些探索AI临床试验的人们》梳理的领域基准，供 ct- 技能选型外部评测集时查阅。完整清单见周报。

| 基准 | 规模 | 对 ct- 的用途 |
|---|---|---|
| TrialBench | 8 类任务 / 23 子数据集（试验时长/脱落/安全/批准/失败原因） | ct-samplesize / ct-safety 外部评测集 |
| PyTrial | 6 类任务 / 34 算法 / 23 数据集 | ct-advisor 路由与合成数据评测 |
| TrialReviewBench | 100 篇系统综述 / 2,220 项研究 | ct-literature 证据综合评测 |
| CDISC-Bench (GxP-Agent 配套) | SDTM→ADaM 转换能力评测（可执行/结构匹配/数据值正确） | ct-adam 验收基准（2026-10-19 情报新增） |
| TOP | 17,538 项试验（建模集 12,465） | 终点成败预测外部参照 |
