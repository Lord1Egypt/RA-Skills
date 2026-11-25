---
name: ai-docgen-expert
description: 为代码库生成、评审与治理编程文档的完整知识库：Diátaxis 类型学、API 文档（TSDoc/JSDoc/TypeDoc/OpenAPI）、注释/docstring、ADR 与 changelog、README、AI 文档生成工作流、幻觉验证与文档漂移/腐化治理、doc-as-code 文档门禁与测试，产品与技术文档模板（PRD、技术方案/设计文档、测试方案、发布方案、runbook、故障复盘），以及软件开发项目专业文档（SRS 需求规格、架构总览 C4、业务流程、交互设计交接、数据设计、集成契约、项目管理、威胁建模）。Use when 为代码库生成、评审或治理编程文档：让 AI 写 API 文档/注释/README/ADR/changelog，检测与治理文档漂移与腐化，搭建 docgen 与文档门禁 CI，验证 AI 生成文档的可信度，设计项目文档体系与信息架构，撰写/评审 PRD、技术方案、测试方案、发布方案、runbook、故障复盘，或编写 SRS、架构文档、业务流程、数据字典、集成契约、项目管理与安全文档。Triggers: 文档生成, 文档治理, API 文档, 注释, docstring, TSDoc, JSDoc, TypeDoc, OpenAPI, Swagger, ADR, 架构决策记录, changelog, 变更日志, README, 文档漂移, 文档腐化, Diátaxis, 文档评审, 文档门禁, doc-as-code, 文档测试, AI 文档, 幻觉, PRD, 需求文档, 技术方案, 设计文档, 测试方案, 发布方案, runbook, 故障复盘, SRS, 需求规格说明书, 架构文档, C4, 业务流程, 数据字典, 接口文档, 威胁建模。Covers Diátaxis 四象限 / TSDoc / Keep a Changelog 1.1.0 / Conventional Commits 1.0.0 / SemVer 2.0.0 / ADR（MADR·Nygard·Y-Statement）/ Google 文档风格指南 / Google Design Docs / Atlassian PRD·Postmortem / C4 model / OWASP 威胁建模 / OMG BPMN。
---

# ai-docgen-expert

编程文档（API 文档、注释、README、ADR、changelog、教程/指南）、产品/技术工作文档模板（PRD、技术方案、测试方案、发布方案、runbook、故障复盘）与软件开发项目专业文档（SRS、架构总览、业务流程、交互交接、数据设计、集成契约、项目管理、安全文档）的生成、评审与治理知识库。适用于让 AI 生成或审校文档、治理文档漂移与腐化、搭建文档门禁；不适用于纯文学写作与非代码项目文档。

## 知识库索引

| 文件 | 内容 | 何时读 |
|---|---|---|
| kb/laws.md | 全局宪法：LAW-1~19 按事实/结构/同步/验证/治理五组（含溯源与合并登记） | **写任何文档前必读** |
| kb/doc-taxonomy.md | Diátaxis 四象限判型、混写崩塌（blur）拆分、README 定位、读者-时刻矩阵、信息架构（DT-1~12） | 动笔前判型 / 文档体系设计 |
| kb/api-doc-gen.md | TSDoc 24 标签、JSDoc 对照、TypeDoc 工具链、OpenAPI spec 生成、签名完整性、示例纪律（AD-1~13） | 写 API reference / 选 docgen 工具 |
| kb/code-comment.md | 注释价值判据（why/context）、Google 官方谱系、噪音注释反模式、TODO 纪律、语言风格差异（CC-1~12） | 写注释/docstring / 清理噪音注释 |
| kb/adr-changelog.md | ADR 四段结构与 supersede 流程、KaC 1.1.0 官方六类目、三模板族、release notes 区分（AC-1~11） | 写 ADR / changelog / release notes |
| kb/ai-docgen-workflow.md | AI 文档生成工作流：输入契约、prompt 四件套、批量与增量策略、置信度分层、CI 集成（AW-1~11） | 设计/执行 AI 文档生成流程 |
| kb/ai-doc-verification.md | AI 文档幻觉模式识别、事实锚定比对、三态链接检查、人工评审清单、批次抽样（AV-1~10） | 验证 AI 生成的文档 |
| kb/doc-governance.md | 文档漂移检测、SSOT 设计、文档门禁 CI、生命周期处置、owner 责任模型、度量局限（DG-1~11） | 治理文档腐化 / 建门禁 |
| kb/doc-quality.md | 质量四维评估（可发现/可理解/可操作/时效）、示例代码规范、渐进披露、AI 腔治理（DQ-1~10） | 评审文档质量 / 治理 AI 腔 |
| kb/doc-templates.md | 产品与技术文档模板：PRD、技术方案（Design Doc/RFC）、测试方案、发布变更、Runbook、故障复盘——文档链与轻重变体、法则 PT-1~15、七套可复制模板正文（PT-1~15） | 写/评 PRD、技术方案、测试方案、发布方案、runbook、故障复盘 |
| kb/proj-docs.md | 软件开发项目专业文档：SRS 需求规格、架构总览（C4 模型）、业务流程（BPMN）、交互设计交接、数据设计（数据字典/ER/迁移）、集成契约、项目管理（章程/纪要/状态报告/风险登记册/RACI）、安全文档（威胁建模/渗透报告）——法则 PJ-1~15、十六套可复制模板正文 | 写/评 SRS、架构文档、业务流程、交接文档、数据设计、集成契约、PM 文档、安全文档 |
| kb/ai-mistakes.md | 10 子域 166 条「AI 生成文档典型错误」总集（按子域分节表） | **让 AI 写文档前扫一遍** |
| kb/gotchas.md | 跨域 Top 19 坑点（G-1~19）：事实幻觉/结构混写/漂移失效/流程门禁/台账生命周期五组 | 快速排雷 |
| kb/patterns.md | 7 个跨域模式（P-1~7）：工具链选型、体系从零搭建、生成-验证-审校流水线、联动设计、门禁最小集 | 方案设计阶段 |

## 决策树（按问题类型找知识文件）

- 红线在哪 / 全局约束自检 → `kb/laws.md`
- 判型（tutorial/how-to/reference/explanation）/ 混写拆分 / README / 信息架构 → `kb/doc-taxonomy.md`
- API 文档生成 / TSDoc·JSDoc 标签 / TypeDoc·OpenAPI 工具链 → `kb/api-doc-gen.md`
- 注释与 docstring / 噪音注释清理 / TODO 纪律 → `kb/code-comment.md`
- ADR / changelog / release notes / 决策记录流程 → `kb/adr-changelog.md`
- AI 文档生成工作流 / prompt 设计 / 批量·增量生成 → `kb/ai-docgen-workflow.md`
- AI 文档幻觉识别 / 验证手段 / 人工评审清单 → `kb/ai-doc-verification.md`
- 文档漂移与腐化 / SSOT / 文档门禁 CI / owner 制 → `kb/doc-governance.md`
- 文档质量评估 / 示例规范 / 风格与 AI 腔 → `kb/doc-quality.md`
- PRD / 技术方案 / 测试方案 / 发布方案 / runbook / 故障复盘 / 模板裁剪与轻重变体 → `kb/doc-templates.md`
- SRS 需求规格 / 架构总览（C4）/ 业务流程（BPMN）/ 交互交接 / 数据字典·ER·迁移 / 集成契约 / 章程·纪要·状态报告·风险登记册·RACI / 威胁建模·渗透报告 → `kb/proj-docs.md`
- 先查 AI 典型错误再动笔 → `kb/ai-mistakes.md`
- Top 坑点速查 → `kb/gotchas.md`
- 选型决策 / 体系搭建 / 流水线设计模式 → `kb/patterns.md`

## Top 法则（不读 kb 也必须遵守的）

- [LAW-1] **NEVER** 硬事实零编造：版本号/签名/参数/默认值/日期/issue 号/badge 无源不写，无源只能产出「结构模板 + 待填标注」。
- [LAW-2] **NEVER** 理由零编造：决策 forces/why/动机/备选对比是项目私有事实，无输入不生成——AI 是结构师+提问者，不是决策代笔。
- [LAW-5] **MUST** 先判型后写作：官方判型四问（"Can you teach me to…?" / "How do I…?" / "What is…?" / "Why…?"）落到四类型之一，判不出型说明该拆分。
- [LAW-6] **MUST** 信息进最高可表达载体层：类型 > 命名 > 注释 > 手写文档；注释/文档只写载体表达不了的（why > context > how > what）。
- [LAW-9] **MUST** SSOT：每个事实只有一个权威存放处；链接 > 复制；生成物单向——改源再生成，不手改编译产物。
- [LAW-10] **MUST** 文档同步靠结构触发不靠记忆：接口变更→reference+changelog、行为变更→全站 grep 旧行为；「记得更新文档」不是机制。
- [LAW-11] **MUST** 质量多维评估缺一不可，准确性优先：准确 > 时效 > 完整 > 一致 > 可发现 > 可读——「错而美」的文档不能过评审。
- [LAW-16] **MUST** 发布即担责：「AI 写的」不构成免责；AI 参与度影响审校强度，不影响责任归属。

## Top 坑点（不读 kb 也必须知道的）

- [G-1] 无源编造事实数据（签名/版本/日期/badge），编造与事实同形输出，读者无法分流——P0。
- [G-2] 交叉引用与链接幻觉（`详见 §3.2` 指向不存在章节、`{@link}` 指向不存在导出），读者点击 404——P0。
- [G-6] 类型混写崩塌（blur）：单文档教程腔+参考腔+解释腔混排，长文档前半守型后半回归默认模板——P0。
- [G-10] 代码-文档同步漂移：改代码不动旧注释/示例，漂移静默发生——静默失效。
- [G-11] 示例复制即报错：省略号 `// ...`、import 缺失、版本沉默假设——死示例，P0。
- [G-13] 链接检查把 403 反爬当 BROKEN：全量误报淹没真 404，团队关闭整个检查——门禁失效。
- [G-15] 零审校直出：AI 生成直接 publish，「看起来很好」时恰恰最危险——P0 + 静默失效。
- [G-17] ADR/追加型历史被原地改写：把 ADR 当活文档，历史被摧毁——P0（changelog 可诚实修订，ADR 永不改写）。
- [G-18] 批次错误自相关不扩抽：抽 10 篇 2 篇幻觉仍放行同批 90 篇——AI 错误在批次内同模式，发现一处即整批扩抽信号。
- [G-19] 活台账写完即僵尸：台账类活文档（风险登记册/威胁模型/检查表）AI 生成「完美初始台账」——状态机、复审日期、更新触发缺失即静默失效。

## 回答规范

- 回答引用 kb 条目时保留来源标注（[官方文档]/[模型经验]/[推断]/[实战回流]）。
- 生成文档前先核对 `kb/laws.md` 的 LAW 条款与对应子域法则，逐条自检是否违反；动笔前先过判型四问。
- 事实类内容（版本/签名/参数/数字）无来源时明说无来源并降级为模板 + 待填标注，不编造；版本敏感结论注明所基于的版本。
- 低置信内容（docs.anthropic.com 域锚点不可达的降级条目）引用时注明「降级域，未经官方文档验证」。

## 知识回流

触发条件：修复了 kb 未覆盖的文档问题 / 发现 kb 错误过时 / 官方规范更新（如 KaC/TSDoc 新版本）。
处理：按 kb-distiller 的 refine 规程向对应 kb 文件追加结构化条目，标注 [实战回流]，更新 version 与 updated。
路径提示：kb-distiller/prompts/refine.md

## 对账记录

| 轮次 | 结果 | 日期 |
|---|---|---|
| 第 2 轮（refresh 补锚） | 豁免——Top 法则（LAW-1/2/5/6/9/10/11/16）与 Top 坑点（G-1/2/6/10/11/13/15/17/18）清单无变化（本轮零新法则、零新 Top 坑点，纯溯源升级：AC-8/AD-9/DG-1/DQ 溯源官方锚化） | 2026-11-17 |
| 第 5 轮（doc-templates 扩展子域） | 对账完成——LAW-17（可判定性）新增但未入选 Top 法则位（判据位适用面集中在模板文档与门禁设计，Top 保持 8 条）；Top 坑点清单无变化（候选「模板八股化」「判据空转」不达 Top 标准，见 kb/gotchas.md 对账记录）；索引/决策树/description 新增 doc-templates 分节与 8 个触发关键词 | 2026-11-17 |
| 第 6 轮（proj-docs 扩展子域） | 对账完成——LAW-18（正常/异常路径并重，G1 升格）与 LAW-19（行动项三要素，G2 升格）新增，均未入选 Top 法则位（Top 保持 8 条）；G-19（活台账写完即僵尸）新增入 Top 坑点（判定 a+c：三子域成立 + 静默失效，OWASP 官方背书）；候选「规格填充」豁免（G-1 实例化）、「理想态偏科」豁免（LAW-18 承担）、G3/G4 GLOBAL 候选留域层（PJ-1/PJ-10 与 PJ-13 分别承担，G4 列入下轮全局对账候选）；patterns.md 不动（无跨域新 pattern——本轮模式均沉淀为域层最佳实践与模板）；索引/决策树/description 新增 proj-docs 分节与 8 个触发关键词 | 2026-11-18 |
| 第 7 轮（refresh 补锚对账） | 对账完成——补锚两处：MADR 官方 spec 站（adr.github.io/madr/，第三路径成功，解决第 2 轮「MADR 状态枚举」挂账：status 为 YAML front matter 可选元数据、官方示例枚举开放集，冲突消解 #3 收口）与 api-extractor.com 三页（AD-8 溯源升级「官方锚 + 模型经验」：.api.md 报告 Git 追踪/随 PR 提交/diff 审查面官方确认，冲突消解 #8 登记）；G4「坏消息显性化」终裁不升格、关闭候选（LAW 维持 19/20 余 1 位，三成立点维持域层 PJ-13/PT-12/AC-1）；横切对账：laws（G4 终裁 + 对账行）、gotchas（豁免）、ai-mistakes（豁免）、patterns 不动（无新跨域 pattern）；SKILL.md description/索引/决策树/Top 清单无变化（零新法则零新 Top 坑点，纯溯源升级） | 2026-11-18 |

## 事实抽查记录

| 轮次 | 抽查条数 | 结果 | 日期 |
|---|---|---|---|
| 第 2 轮（refresh 补锚） | 19（全量） | OK 16 / BLOCKED 3 / BROKEN 0；BLOCKED 均为已知项：2 个 GitHub compare 真实慢页（KaC 官方页脚原文 URL）+ developers.google.com/style（已知不可达族，文件内已标注）；本轮 5 个新锚（conventionalcommits.org/en/v1.0.0/、semver.org/spec/v2.0.0.html、docs.github.com about-code-owners、google.github.io style.html、diataxis.fr/colophon/）全部 OK | 2026-11-17 |
| 第 5 轮（doc-templates 扩展子域） | 24（全量） | OK 19 / BLOCKED 3 / BROKEN 2；BLOCKED 均已知项（同上）；BROKEN 2 为来源索引中预声明放弃的 sre.google URL（SSL 异常，与 ingest 阶段传输错误同因）——非活锚，已在 kb/doc-templates.md 冲突消解记录 #2 登记豁免，不计失败；本轮 3 个新锚（industrialempathy design-docs、Atlassian requirements、Atlassian postmortem）全部 OK | 2026-11-17 |
| 第 6 轮（proj-docs 扩展子域） | 28（全量） | OK 25 / BLOCKED 1 / BROKEN 2；BLOCKED 为已知项（developers.google.com/style 不可达族，文件内已标注）；BROKEN 2 为既有预声明放弃的 sre.google URL（SSL 异常，kb/doc-templates.md 冲突消解记录 #2 登记豁免，非活锚，不计失败）；本轮 4 个新锚（c4model.com、owasp.org/www-community/Threat_Modeling、omg.org/spec/BPMN/ 及 proj-docs.md 内 c4model.com/）全部 OK；基线变化：2 个 GitHub compare URL 本轮由 BLOCKED 转 OK（网络恢复）；ingest 阶段放弃登记：Microsoft STRIDE 三试 404、ISO 29148 目录页 403（见 corpus/ai-docgen/proj-docs/docs/ingest-notes.md） | 2026-11-18 |
| 第 7 轮（refresh 补锚对账） | 32（全量） | OK 27 / BLOCKED 3 / BROKEN 2；本轮 4 个新 URL（adr.github.io/madr/、api-extractor.com 及 intro/demo_api_report 两子页）全部 OK；BLOCKED 3 为已知项（developers.google.com/style 不可达族 + 2 个 GitHub compare URL——网络波动族，第 5/6/7 轮在 BLOCKED↔OK 间波动，本轮 timeout）；BROKEN 2 为既有预声明放弃的 sre.google URL（SSL 异常，kb/doc-templates.md 冲突消解记录 #2 登记豁免，非活锚，不计失败） | 2026-11-18 |
