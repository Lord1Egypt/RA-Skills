# 能力域扩充说明 · 合规应答 / 项目运营 / 交付物撰写

> 配套 `SKILL.md` v1.3.17「覆盖范围扩大」与 `scripts/scope_guard.py` 的 domain 路由表。
> 本文件把三块"过去未被覆盖、但真实高频"的核心域从一句话登记做实为**可落地的子主题清单 + 权威参照**，供 Coze 引擎作答时锚定，避免凭空发挥。
> 所有外部链接均为公开权威来源（ICH / NMPA / CDE / TransCelerate / DIA / CASRAI / EQUATOR 等），检索于 2026-10-22。
> 本技能**不修改** `adapters/coze/`；引擎侧只需接受 `domain_hint` 即可按域偏置检索/路由。

---

## 0. 为什么需要这份文件

飞书 `advisortbl` 近 30 天真实提问诊断显示：用户高频但过去被 `scope_guard` 旧 `medical_writing` tag 误判或干脆没有能力域托底的，集中在三块——

- **合规应答**（GCP 合规判断、核查 readiness、方案偏离/CAPA、监管函件、登记公示）
- **项目运营**（研究中心启动、TMF、监查模式、RBQM 的 QTL/KRI、供应商/CRO 管理、入组与关中心）
- **交付物撰写**（方案/IB/ICF/SAP/CSR、TransCelerate 模板、估计目标、登记类文件）

这三块现在升为**在范围核心域**：命中即路由到云端引擎作答，不再空拒。下面给每块"子主题 + 权威参照 + 顾问协助边界"。

---

## 1. 合规应答（domain = `compliance`）

### 1.1 子主题清单

| 子主题 | 典型真实提问（advisorlog 提炼） | 权威参照 |
|---|---|---|
| GCP 原则与适用 | "受试者权益和安全是首要考虑，这条出处是哪？" / "研究者 vs 申办者责任怎么分？" | ICH E6(R3) 11 项原则（Step 5，2025-01-23 通过，2025-07-23 生效）：https://ichgcp.net/ ；NMPA《药物临床试验质量管理规范》2020 年第 57 号（2020-07-01 施行）：https://www.gov.cn/gongbao/content/2020/content_5525106.htm |
| 中国 GCP 落地 | "方案偏离和方案违背区别？" / "申办者依从性怎么保证？" | NMPA GCP 第九章 申办者职责（第 43–56 条）；核查/检查条款见同公告 |
| 核查与稽查 readiness | "药监局来检查一般会查什么？" / "稽查轨迹是什么？" | ICH E6(R3) Annex 1 §4 Data Governance；NMPA GCP 术语"检查/稽查/稽查轨迹"（第 17、39、40 条）|
| 方案偏离 / CAPA | "中心实验室结果晚回算偏离吗？" / "反复偏离怎么根因？" | ICH E6(R3) QbD 与 proportionate 原则；TransCelerate RBQM（见 §3）|
| 安全性报告 | "SUSAR 怎么报、时限？" / "DSMB 职责？" | ICH E2A / E2F；NMPA GCP 第 11 条术语（SUSAR/SAE）|
| 登记与信息公示 | "试验获批后多久要登记？" / "CTR 号怎么生成？" | 《药物临床试验登记与信息公示管理规范（试行）》CDE 2020 年第 9 号；平台：http://www.chinadrugtrials.org.cn 。**关键时限**：获批/默示许可后 1 个月内预登记；首例入组前≥30 天完成首次提交；入组后 30 天内登记入组日期；终止后 30 天内登记终止日期；"可更新项"变更后 30 天内更新公示 |
| 监管函件 / 沟通交流 | "Pre-IND 沟通怎么提？" / "补充申请什么情形要交？" | 《药物研发与技术审评沟通交流管理办法》；NMPA GCP 第 54 条（提前终止/暂停须告知监管）|
| 受试者权益与知情同意 | "弱势受试者怎么保护？" / "紧急情形先用药后签知情行不行？" | ICH E6(R3) 原则 1.2 / 2（知情同意）；NMPA GCP 第 12 条伦理委员会、第 3 条 |

### 1.2 顾问能如何协助（边界）

- ✅ 解释某条 GCP/法规条款的**含义与适用场景**、给判定框架（"是否构成偏离"的决策树）、给登记/报告**时限与字段清单**、给核查准备**检查单维度**。
- ⚠️ 不替代法律意见与监管裁定；涉及具体品种注册策略的，建议转 `ct-registry` / 注册申报路径，并提示以批件/通知书/沟通交流纪要为准（登记公示≠监管认可方案科学性）。
- 🔗 与 `scope_guard` 的 `registry` 域（登记平台操作）、`safety` 域（安全性报告）天然衔接。

---

## 2. 项目运营（domain = `ops`）

### 2.1 子主题清单

| 子主题 | 典型真实提问 | 权威参照 |
|---|---|---|
| 研究中心启动 Study Startup | "伦理和遗传办递交顺序？" / "中心筛选看哪些指标？" | ICH E6(R3) Annex 1 §2 Investigator / §3 Sponsor；TransCelerate Site Qualification 思路（可行性→资格访视→启动）|
| TMF / 必备文件 | "TMF 怎么归类才 inspect-ready？" / "必备文件清单？" | DIA TMF Reference Model（现由 CDISC 维护，v3）：https://tmfrefmodel.com/ ；CASRAI TMF 指南：https://casrai.org/guides/trial-master-file-essential-documents-structure-inspection-readiness ；ISF Reference Model（MAGI v0.9，2020-02）用于研究站点文件 |
| 监查模式 | "100% SDV 还要不要做？" / "中心化监查怎么落地？" | TransCelerate RBM 方法论：https://www.transceleratebiopharmainc.com/?p=5675 （以 centralized / off-site 为主，SDR 为基础实践）|
| RBQM（QTL / KRI） | "质量容忍限设几个？" / "KRI 和 QTL 区别？" | TransCelerate QTL Framework（PMC7864825 / PMC10276776）：**每研究 QTL 1–5 个（研究级最高风险）、KRI 约 10–25 个（可到中心/地区/患者级）**；ICH E8(R1) 识别 CtQ 因素；QTL 重要偏离须在 CSR 中汇总 |
| 供应商 / CRO 管理 | "外包给 CRO 责任转移吗？" / "vendor Oversight 怎么做？" | ICH E6(R3) 原则 10（职责可委托、责任不转移）；NMPA GCP 第 16 条（机构外单位承担职责须申办者同意）|
| 入组与留存 | "入组慢怎么预判？" / "脱落率高怎么管？" | ICH E6(R3) 招募可行性、参与者多元性；TransCelerate RBM 中 enrolment / dropout KRI |
| 关中心与数据库锁定 | "关中心要做哪些？" / "DBL 前清源数据？" | ICH E6(R3) Appendix C Essential Records；CASRAI TMF「After completion」清单（最终 CSR、受试者鉴认码表、稽查证明、IP 最终 Accountability）|

### 2.2 顾问能如何协助（边界）

- ✅ 给**启动清单 / TMF 分区（Trial/Country/Site 三级 Artifact ID 如 01.01.01 Protocol）/ RBQM 设计模板（CtQ→QTL/KRI 映射表）/ 监查策略选型（on-site vs centralized vs hybrid）/ 关中心核对表**。
- ⚠️ 不替团队做项目排程与预算承诺；运营动作须结合申办者 SOP 与本机构流程。QTL/KRI 阈值建议基于历史数据与统计学特征（ICH E8(R1)），必要时转 `ct-stats`/`ct-samplesize` 做把握度与 tolerance 计算。
- 🔗 与 `scope_guard` 的 `data` 域（eCRF/数据质量）、`stats` 域（QTL 统计方法）衔接。

---

## 3. 交付物撰写（domain = `writing`）

### 3.1 子主题清单

| 子主题 | 典型真实提问 | 权威参照 |
|---|---|---|
| 方案 Protocol | "方案要写多细？" / "方案修订和重大修改怎么分？" | ICH E6(R3) Appendix B Clinical Trial Protocol；TransCelerate Common Protocol Template（CPT/eCPT）：https://www.transceleratebiopharmainc.com/?p=9572 （2026 起对齐 ICH M11 模板与技术规范）|
| 统计师分析计划 SAP | "SAP 什么时候锁？" / "估计目标怎么写进 SAP？" | ICH E9(R1) 估计目标五属性（治疗 / 目标人群 / 变量 / 并发事件策略 / 总体汇总）：EMA addendum；SAP 模板（CASRAI）：https://casrai.org/guides/statistical-analysis-plan-template ；Gamble et al. JAMA 2017 **55 项 / 32 标题 SAP 清单**（EQUATOR 认可），盲态审核为最后可改窗口 |
| 临床研究报告 CSR | "CSR 和方案不一致怎么解释？" / "获益-风险要不要写？" | ICH E3；TransCelerate eCSR（lean、不含获益-风险解读）；QTL 重要偏离须在 CSR 汇总 |
| 研究者手册 IB | "IB 多久更新？" | ICH E6(R3) Appendix A；NMPA GCP 术语（第 21 条）|
| 知情同意 ICF | "ICF 可读年级几年级？" / "紧急情况下先操作后知情？" | ICH E6(R3) 原则 2（技术辅助知情同意）；NMPA GCP 第 12 条；21 CFR 50（US）|
| 医疗器械文档 | "器械方案按什么写？" | ISO 14155（Clinical investigation of medical devices）；CIP/CIR 结构 |
| 登记类文件 | "登记信息表哪些不可更新？" | CDE《登记填写指南 V1.1》/《使用说明 V1.0》；一个方案编号→一条 CTR 记录，不可更新项公示后不可自改 |

### 3.2 顾问能如何协助（边界）

- ✅ 给**文档结构骨架 / 章节清单 / 常见不一致点排查（如 SAP 主分析人群与方案不符的 protocol-inconsistency）/ 估计目标→分析对照表模板 / ICF 可读性自查清单 / CSR 与方案一致性核对表**。
- ⚠️ 不替代医学写作与监管申报；正式文档须由具备资质的医学/统计/法规作者署名并 QC。涉及估计目标与敏感性分析设计的，建议转 `ct-stats`；涉及 ICH M11/eCTD 申报结构的，转注册路径。
- 🔗 与 `scope_guard` 的 `stats` 域（SAP/估计目标）、`design` 域（方案）、`registry` 域（登记）衔接。

### 3.3 方案评阅路由（→ `ct-protocol`，2026-11-05 新增）

**动因**：用户反馈本技能对「方案评阅 / 修改意见」类问题**输出笼统**；而 `ct-protocol` 有结构化评审框架（U1–U12 工作流 / D1–D9 风险评分 / 立论与逻辑一致性审查 / 批注版输出）。

| 项 | 口径 |
|---|---|
| 触发 | `route_tool.py` 弱触发词：`方案` 与 `评阅/审阅/评审/审查/审一下/批注/修订/修改意见` 同现（英文 `protocol review/audit/assessment`） |
| 动作 | **仅软建议**——答案末尾追加一行「可直接调用 `@skill:ct-protocol` 做结构化评审」，**不自动调用**（ct-protocol 为 B 档本地技能，不在 `tool_mapping` 自动执行表）。2026-11-09 起它与全部 B 档技能一样已在本机注册、客户端可直接调用，故建议改用 `@skill:` 形态，用户可直接走完整评阅流程并拿到批注版交付物 |
| 护栏例外 | 「如何评审这个方案」这类**咨询护栏**命中时仍保留该建议（题是对路的，不应被护栏清空） |
| 反例 | 「方案修改后需要重新伦理审查吗」是合规题，**不**建议 ct-protocol（正则要求审阅动词紧邻「方案」） |
| 决定权 | 是否切换由用户决定；本技能仍先按自身能力作答 |

**2026-11-09 客户端直调适配**：`published=false` / `tier=B` 不再等于「不可调用」。
`handle_need_tool._client_callable()` 以 `sibling_registry.json::installed` 与
`<SKILLS_DIR>/<slug>/SKILL.md` 为本机可得性判据；命中即返回 `status=handoff`
（`@skill:<slug>` + 已识别参数 + 交付物 + B 档保密提醒），不再回
`unreleased_b` 的「不对外发布 / 无法通过安装获取」。卡片由代码产出、经
`entry.py` 单一出口输出，HARD GATE 与 F33 涉密边界不变。
详见 `SKILL.md` 的 Client handoff contract 一节。

---

## 4. 给 Coze 引擎的偏置提示

- 命中 `compliance`/`ops`/`writing` 任一域时，`scope_guard` 输出 `domain_hint`（多标签，最多 3 个），引擎可据此优先检索上述权威源与对应兄弟技能。
- 三域均为**本地路由、不触发越界转介**；仅当问题同时明确非医药/生命科学语境（如消费电子、金融、快消）才走 `scope_hint` 建设性转介。
- 文档内所有链接为"作答时建议引用的权威锚点"，不代表本技能托管其内容；链接失效时以官网现行版本为准。

---

## 5. 一句话自检（给维护者）

- 新增子主题时，先确认它落在 `compliance` / `ops` / `writing` 哪个域；跨域的在 §1.2/2.2/3.2 标注 `🔗` 衔接。
- 任何"能协助"项不得越过"边界"项声称替代法律/监管/医学写作结论。
- 权威链接每发版复核一次（ICH/NMPA/CDE/TransCelerate/DIA 偶有版本更新）。
