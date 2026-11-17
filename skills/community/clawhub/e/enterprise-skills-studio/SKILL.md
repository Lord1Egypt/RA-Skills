---
name: enterprise-skills-studio
version: "1.1.0"
description: 企业技能工程台（通用、跨平台）。面向企业管理者、业务与技术人员，覆盖企业级技能的"学习理解 / 构建设计 / 个人→企业升级 / 治理管理 / 安全审查 / 持续进化 / 跨平台适配 / 体系规划 / 流程技能生成 / 生命周期 Ops / ROI 筛选 / 进化维护 / 技能发现复用 / 培训推广 / Agentic 治理 / 选题透镜 / 技能编排 / 评测套件 / 统一 CLI / 成本计量 / 门户生成"。基于 Agent Skills 开放标准（agentskills.io），产出的技能可在 WorkBuddy、Codex、Claude Code、Cursor、龙虾、Hermes 等支持该标准的桌面 Agent 间移植。遵循"厚技能+薄 harness"原则。当用户要"懂企业技能 / 做一个企业技能 / 把个人技能转企业级 / 治理审查技能 / 跨平台适配技能 / 规划企业技能体系 / 把 ERP·CRM·HRM·OA 等系统型业务流或 Agentic Workflow 做成技能 / 评估技能值不值得做(ROI) / 治理技能生命周期与弃用 / 维护技能 Evolution Log / 新造技能前查重避免重复 / 生成业务培训推广包 / 做跨平台适配合规检查 / 治理一支 Agent 队伍(评估护栏可观测责任归属) / 用 PEST·波特五力·价值链找高杠杆流程做技能选题 / 把多个技能编排成工作流 / 生成技能的评测测试用例 / 加固技能防 PII 泄露与 prompt 注入 / 用一个统一命令(studio)调度所有技能工程脚本 / 追踪技能运行成本与调用计量来佐证 ROI / 把技能库生成可发现的门户目录或网页 / 在发布或移植某技能前同时跑安全体检与移植体检做卡点(gate) / 让本技能自我更新(说"检查/更新本技能"，默认仅检查、需确认才应用) / 审计扫描某技能的安全性(SkillSec 16 类，借鉴 NVIDIA SkillSpector 方法论)"时使用。
agent_created: true
capabilities:
  network: "仅向固定可信源 jiwei1122/enterprise-skills-studio 发起 HTTPS GET 以下载更新归档；不发送任何本地数据，不连接该仓库以外的任何地址"
  filesystem: "读取/写入严格限制在本技能自身目录；绝不访问 ~/.ssh、.env 或任何凭据文件"
  execution: "仅运行本技能自带的标准库 Python 脚本；自更新仅复制文件，绝不执行远程下载的代码"
  privilege: "不使用 sudo/root，不提权，不读取环境变量或系统凭据"
  autonomy: "所有写操作与自更新均须用户显式触发（--apply 默认交互确认，并明确警告将覆盖本地文件）；不做自主决策；企业可设 ESS_SELF_UPDATE=off 禁用写盘更新、ESS_ALLOWED_REPOS 限定可拉取仓库"
  data_handling: "不采集、不上传、不持久化用户业务数据；分析仅在本机文件内进行"
---

# 企业技能工程台 (Enterprise Skills Studio)

把"企业技能（Enterprise Skills）"的方法论，固化成一个**通用、跨平台**的技能工程台。本质：将组织最佳实践/业务流程/个人经验，结构化为 Agent 可调用、可治理、可复用的能力模块——即**受治理的业务工作流制品**。

> **维护者 / owner**：企业技能工程台 · 平台工程组（platform-eng）；问题归属此角色，安全审查由独立安全官执行（作者不自审）。

## 资料来源（方法论底座）

- 主文章：《一文读懂 Enterprise Skills》（公众号）+ 用户 Obsidian 扩展阅读包（17 篇权威出处）
- 提炼自：Anthropic 官方企业规范、Atlan、Sidbharath 部署指南、Cloud Security Alliance(CISO 5/AST10)、腾讯云持续进化、Agentman 生态报告、aigenticlab 分层治理、人人都是产品经理、AIERI 论文库(SkillsBench 等)
- 市场检索结论：SkillHub/ClawHub 无专门"技能构建与管理"技能，本技能填补空位

## 跨平台定位

产出严格遵循 **agentskills.io 开放标准**，可在 WorkBuddy / Codex / Claude Code / Cursor / 龙虾 / Hermes 等桌面 Agent 间移植。具体适配见 `references/cross-platform.md`。

## 最高准则：厚技能 + 薄 harness

把智能尽量封装进技能本身（脚本/模板/决策树/校验），harness 只负责发现与调用。详见 `references/principles.md`（含厚技能体检清单）。本技能自身亦遵循之。

## 能力模式（先判断用户意图，选一种进入；可串联）

1. **学习理解** — 面向管理者/业务：科普 + 起步规划（`references/learning.md`）
2. **构建设计** — 设计器五步法，个人/企业模式（`assets/SKILL.md.template`）
3. **个人→企业升级** — 个人技能直接转企业级（`references/personal-to-enterprise.md` + `scripts/upgrade_skill.py` 自动升级）
4. **治理管理** — 注册表/命名/角色包/版本/分发（`references/governance.md`）
5. **安全审查体检** — 8 项 + CISO 5 + 质量 5 + 厚技能体检 + **安全语义层**（编码绕过/base64·ROT13·零宽字符、敏感路径 ssh/aws 私钥与环境配置与 agent 记忆文件、裸 IP 外联、提权、未声明装包、声明-能力一致性；仅扫可执行文件，借鉴 `skill-scanner`(朱雀 A.I.G) 与 `skill-vetter` 规则），跑 `scripts/review_checklist.py`，结合 `references/governance.md` + `references/principles.md`
6. **持续进化** — 会话挖掘/Evolution Log/周度运营（`references/evolution.md`）
7. **跨平台适配** — 移植到目标桌面 Agent（`references/cross-platform.md` + `scripts/cross_platform_check.py` 适配合规检查：name/description/agentskills.io/依赖预置/防特化）
8. **体系规划** — 成熟度评估 + 三模式选型 + 四前提自检 + 角色能力矩阵（`references/planning.md` + `scripts/maturity_assess.py` 量化自测）
9. **流程技能生成器** — 面向 ERP/CRM/HRM/OA 等系统型业务流 + Agentic Workflow + LLM 融合，把"连接器抽象/领域本体/事务安全四件套/状态机/HITL/降级/强 schema/置信闸门"固化进技能（`references/process-systems.md` + 模板「系统/工作流扩展段」）
10. **生命周期 Ops** — 规划→创建→评估→部署→运营→弃用 六阶段治理 + 注册表 + 版本/弃用归档（`references/lifecycle-ops.md` + `scripts/lifecycle_track.py` 阶段追踪与弃用候选）
11. **ROI 筛选** — 用例门槛判定值不值得做（周≥10次/单次>30min/年>£5k/步骤一致）（`references/roi.md` + `scripts/roi_filter.py` 量化门槛）
12. **持续进化器** — 会话挖掘/Evolution Log 自动维护（`references/evolution.md` + `scripts/evolution_log.py` 追加条目）
13. **技能发现/复用** — 新造前先查重：name 重名/近似 + description Jaccard 重叠 + 触发词重叠，给复用/扩展/合并/新造决策（`references/discovery.md` + `scripts/dupe_check.py` 重名与重叠检测）
14. **培训推广包** — 试点 + 培训材料生成：场景卡/上手指南/FAQ/反馈单四件套（`references/training.md` + `scripts/training_pack.py` 生成培训包骨架）
15. **Agentic 治理** — 管理一支 Agent 队伍：评估/护栏/可观测/责任归属/人机协同（治理面，与模式 9 的工程面互补）（`references/agentic-governance.md`）
16. **选题透镜** — 用 PEST / 波特五力 / 产业价值链作技能选题的**上游透镜**，找高杠杆流程再接 ROI 判定（`references/scoping.md`，薄引用不深搬）
17. **技能编排器** — 把多个厚原子技能串成工作流：串行/并行/条件/人工门/降级（`references/composer.md` + `scripts/compose.py` 生成编排器骨架）
18. **评测套件生成器** — 生成应触发/不应触发/边界测试用例，从静态审查推进到**动态评测**（`references/evaluation.md` + `scripts/eval_gen.py`）
19. **统一 CLI 入口** — 一个 `studio` 命令调度全部脚本（review/upgrade/maturity/lifecycle/roi/evolution/dupe/training/cross-platform/compose/eval/portal/usage），降低使用摩擦、统一参数与 `--help`（`scripts/studio.py` 薄 harness 透传）
20. **成本/计量追踪** — 半自动 usage 日志采集 token/调用/成本，外推月用量直接喂给 ROI 判定，给 sponsor 算账（`scripts/usage_tracker.py` + `references/roi.md` 闭环）
21. **技能门户生成器** — 技能库 → 门户目录/README/HTML，提升可发现性与治理可视化，可结合 lifecycle 注册表标注状态（`scripts/portal.py`）
22. **发布前卡点（gate）** — 一键同时跑【安全体检 + 移植体检】，任一 BLOCK 即整体 BLOCK，发布/移植前必过（`scripts/studio.py gate --skill <dir> [--platform codex]`）
23. **自更新（Self-Update）** — 说"检查/更新本技能"即检查并（确认后）应用自身最新版本：从钉置到不可变发布标签的可信仓库拉取归档、SHA256SUMS 完整性校验、合并白名单、可备份回滚、git 仓库自动保护、非默认仓库强制确认（`scripts/update_skill.py` + `references/self-update.md`，默认 `studio update` 仅检查，需 `--apply` 并经确认才写盘）
24. **技能安全审计（SkillSec 16 类）** — 对任一技能（含本技能自身）做类 NVIDIA SkillSpector 式静态安全审计：覆盖过度能动/输出处理/叛变特工/触发滥用/MCP 最低特权/MCP 工具中毒/提示注入/数据外流/特权升级/供应链/系统提示漏出/记忆中毒/工具滥用/危险 AST/污染追踪/YARA 签名 16 类，输出「类别/严重度/置信度/证据/发现」报告，可作 CI 卡点（`scripts/skillsec_audit.py` + `references/skill-spector-method.md`，`studio audit <skill> [--json|--md]`；方法论借鉴 SkillSpector 公开分类，本实现为自有开源代码）

> 增强项（扩展既有模式）：成熟度模型新增 **Agentic 维度**（模式 8 / `scripts/maturity_assess.py`，向后兼容）；审查器新增 **AI 安全维度** PII/凭据/外部输入校验（模式 5 / `scripts/review_checklist.py`）；审查器再新增 **安全语义层维度**（模式 5 / `scripts/review_checklist.py`，借鉴腾讯朱雀 `skill-scanner` 的编码绕过/零宽走私检测 + `skill-vetter` 的敏感路径/裸IP/提权/未声明装包/声明-能力一致性红标清单）；新增 **技能安全审计能力**（模式 24 / `scripts/skillsec_audit.py`，方法论借鉴 NVIDIA SkillSpector 公开 16 类漏洞模式，自有开源实现，与 `review` 体检互补）。

## 核心工作流：设计器五步法（模式 2）

1. **梳理业务逻辑**：明确场景/触发/输入输出/隐含规则（少问多读已有材料）
2. **准备知识材料**：按四层（指令/知识/工具/示例）+ 技术层/规则层二分法归类；业务写规则、工程做能力，AI 产品经理桥梁
3. **生成 SKILL.md**：套 `assets/SKILL.md.template`；硬性规则——name≤64 小写连字符、description≤1024 含"何时调用"、祈使句、三级加载、**厚技能化**（脚本/模板/校验）、聚焦单一职责、召回保守≤8
4. **测试迭代**：3–5（企业 10–20）条查询，覆盖 应触发/不应触发/模糊边界
5. **发布治理**（企业模式）：四前提自检 + 命名 + 注册表 + 角色包 + 安全审查 + 版本回滚 + 分发 + 持续进化

## 个人→企业升级（模式 3，要点）

逐条对照 `references/personal-to-enterprise.md` 升级清单：命名规范→结构补全→技术/规则拆分→厚技能化→安全审查→作用域隔离→治理信封→审计回滚→分发→四前提自检；输出升级版 SKILL.md + 差异说明。

## 资源索引

- `references/principles.md` — **厚技能+薄 harness** 原则与体检清单（最高准则）
- `references/learning.md` — 管理者/业务人员科普与起步规划
- `references/framework.md` — 技术框架：Tools/MCP/Skills 分类、三级加载、四层、技术/规则层
- `references/governance.md` — 治理：四前提、六阶段、安全8项、CISO 5(AST10)、质量5、分层治理、分发六法
- `references/personal-to-enterprise.md` — 个人→企业升级转换器
- `references/cross-platform.md` — 跨平台适配（WorkBuddy/Codex/Claude Code/Cursor/龙虾/Hermes）
- `references/evolution.md` — 持续进化：会话挖掘、反馈闭环、Evolution Log、周度运营
- `references/planning.md` — 体系规划：成熟度五级 + 三模式选型 + 四前提自检 + 角色能力矩阵 + 落地路线图
- `references/lifecycle-ops.md` — 生命周期 Ops：六阶段 + 注册表 + 版本/弃用归档流程
- `references/roi.md` — ROI 筛选：用例四门槛（频次/时长/成本/一致性）
- `references/evolution.md` — 持续进化：会话挖掘、反馈闭环、Evolution Log、周度运营
- `references/process-systems.md` — 流程技能方法论：系统型流（连接器/本体/事务安全四件套/RBAC/确定性边界）+ Agentic Workflow（状态机/薄编排厚原子/HITL/可观测/降级）+ LLM 融合（概率-确定性分界/强 schema/置信闸门/模板固化）
- `references/discovery.md` — 技能发现/复用：查注册表 + name 重名/近似 + description Jaccard 重叠 + 触发词重叠 + 复用决策矩阵
- `references/training.md` — 培训推广包：试点选择 + 培训包四件套（场景卡/上手指南/FAQ/反馈单）+ 角色话术
- `references/cases.md` — 真实案例与基准（SkillsBench、IBM/JPMorgan/Klarna/Cognizant 等）
- `assets/SKILL.md.template` — 标准企业技能 SKILL.md 模板（四层 + 治理件 + Evolution Log + 厚技能提示）
- `scripts/review_checklist.py` — 审查器：安全8项 + CISO5(AST10) + 质量5 + 厚技能体检 + 事务安全/工作流可恢复性（支持 `--json`/`--md`，可作 CI 卡点）
- `scripts/upgrade_skill.py` — 个人→企业升级器：读入个人 SKILL.md，自动套升级清单产出企业版 + 差异说明
- `scripts/maturity_assess.py` — 体系成熟度自测器：五维度打分→L0–L4 等级 + 最短板 + 下一步建议（支持 `--answers`/`--json`/`--md`）
- `scripts/lifecycle_track.py` — 生命周期追踪器：注册表阶段分布 + 待复审 + 弃用候选（支持 `--registry`/`--json`/`--md`）
- `scripts/roi_filter.py` — ROI 筛选器：四门槛→BUILD/HOLD + 未达标原因（支持 参数/`--answers`/`--json`/`--md`）
- `scripts/evolution_log.py` — Evolution Log 维护器：追加结构化条目并输出 markdown（支持 `--skill`/`--version`/`--change`/`--trigger`）
- `scripts/dupe_check.py` — 技能发现/复用检测器：name 重名/近似 + description Jaccard 重叠 + 触发词重叠 → 复用/扩展/合并/新造（支持 `--skills-dir`/`--registry`/`--name`+`--desc`/`--json`/`--md`）
- `scripts/training_pack.py` — 培训包生成器：读 SKILL.md → 场景卡/上手指南/FAQ/反馈单四件套骨架（支持 `--skill`/`--name`/`--desc`/`--json`/`--md`）
- `scripts/cross_platform_check.py` — 跨平台适配检查器：name/description/agentskills.io/依赖预置/防特化 → 各平台适配要点（支持 `--skill`/`--platform`/`--json`/`--md`）
- `references/agentic-governance.md` — Agentic 治理：评估/护栏/可观测/责任归属/人机协同（与 process-systems 的工程面分工）
- `references/scoping.md` — 选题透镜：PEST/波特五力/产业价值链作技能选题**上游透镜**（薄引用，不深搬战略框架）
- `references/composer.md` — 技能编排器：编排模式（串行/并行/条件/人工门/降级）+ spec 规范 + 薄编排器原则
- `references/evaluation.md` — 评测套件方法论：应触发/不应触发/边界 + 动态评测闭环（含 eval_gen 用法）
- `references/skill-spector-method.md` — 技能安全审计方法论：16 类 taxonomy 与检测器映射、借鉴声明、运行方式（借鉴 NVIDIA SkillSpector 公开分类，自有开源实现）
- `scripts/compose.py` — 编排器生成器：读工作流 spec JSON → 编排器 SKILL.md 骨架（支持 `--spec`/`--out`/`--json`/`--md`）
- `scripts/eval_gen.py` — 评测套件生成器：读 SKILL.md → 应触发/不应触发/边界用例（支持 `--skill`/`--name`/`--desc`/`--json`/`--md`）
- `scripts/studio.py` — 统一 CLI 入口（薄 harness）：子命令调度以上全部脚本，参数透传；`studio gate` 为发布前卡点（同时跑安全+移植双体检）（支持 `studio -h` 列出全部能力）
- `scripts/usage_tracker.py` — 成本/计量追踪：usage JSONL 日志的 log/report/export，外推月用量并给 ROI 输入建议（半自动，需调用方落日志）
- `scripts/portal.py` — 技能门户生成器：扫描技能库 → PORTAL.md + 可选 HTML，可结合 lifecycle 注册表标注状态
- `scripts/update_skill.py` — 自更新器：检查/应用本技能自身更新（从可信仓库拉归档增量合并，支持 --check/--apply/--backup/--dry-run/--json，更新前快照可回滚、git 仓库自动保护）
- `scripts/skillsec_audit.py` — 技能安全审计器（SkillSec 16 类）：静态扫描任一技能的安全风险，输出类 SkillSpector 报告（类别/严重度/置信度/证据/发现），支持 --json/--md，可作 CI 卡点（方法论借鉴 NVIDIA SkillSpector 公开分类，自有开源实现）

## 已实现模块

- ✅ **审查器** `scripts/review_checklist.py`：自动跑安全8项 + CISO5 + 质量5 + 厚技能体检 + **事务安全四件套 + 工作流可恢复性**（流程技能专用，见 `references/process-systems.md`）；脚本可重复运行（幂等，重跑不改既有产出）
- ✅ **个人→企业升级器** `scripts/upgrade_skill.py`：读入个人 SKILL.md 自动套清单产出
- ✅ **流程技能生成器**（模式 9）：系统型流 + Agentic Workflow + LLM 融合方法论已落成（`references/process-systems.md` + 模板「系统/工作流扩展段」）
- ✅ **体系规划师**（模式 8）：成熟度五级 + 三模式选型 + 四前提自检 + 角色能力矩阵已落成（`references/planning.md` + `scripts/maturity_assess.py` 量化自测）
- ✅ **生命周期 Ops**（模式 10）：六阶段治理 + 注册表 + 弃用归档已落成（`references/lifecycle-ops.md` + `scripts/lifecycle_track.py`）
- ✅ **ROI 筛选**（模式 11）：用例四门槛量化判定已落成（`references/roi.md` + `scripts/roi_filter.py`）
- ✅ **持续进化器**（模式 12）：Evolution Log 自动维护已落成（`references/evolution.md` + `scripts/evolution_log.py`）
- ✅ **跨平台适配器**（模式 7 升级）：适配合规检查已落成（`references/cross-platform.md` + `scripts/cross_platform_check.py`）
- ✅ **技能发现/复用**（模式 13）：重名与重叠检测已落成（`references/discovery.md` + `scripts/dupe_check.py`）
- ✅ **培训推广包**（模式 14）：培训包四件套生成已落成（`references/training.md` + `scripts/training_pack.py`）
- ✅ **Agentic 治理**（模式 15）：评估/护栏/可观测/责任归属/人机协同方法论已落成（`references/agentic-governance.md`）
- ✅ **选题透镜**（模式 16）：PEST/五力/价值链作技能选题上游透镜已落成（`references/scoping.md`）
- ✅ **技能编排器**（模式 17）：多技能串工作流编排已落成（`references/composer.md` + `scripts/compose.py`）
- ✅ **评测套件生成器**（模式 18）：动态评测用例生成已落成（`references/evaluation.md` + `scripts/eval_gen.py`）
- ✅ **成熟度模型 Agentic 扩展**（模式 8 增强）：`scripts/maturity_assess.py` 新增 agentic 维度（评测/护栏/可观测/人机协同），向后兼容旧 5 维输入
- ✅ **审查器 AI 安全加固**（模式 5 增强）：`scripts/review_checklist.py` 新增 AI安全维度（PII 检测 / 凭据跨文件扫描 / 外部输入校验），已验证脏技能正确触发
- ✅ **统一 CLI 入口**（模式 19）：`scripts/studio.py` 薄 harness 调度全部脚本，参数透传，统一 `--help` 全能力清单
- ✅ **成本/计量追踪**（模式 20）：`scripts/usage_tracker.py` 半自动 usage 日志 → 聚合外推月用量 → 接 ROI 闭环
- ✅ **技能门户生成器**（模式 21）：`scripts/portal.py` 技能库 → PORTAL.md/HTML，结合 lifecycle 注册表标注状态
- ✅ **发布前卡点 gate**（模式 22）：`scripts/studio.py gate` 一键同时跑【安全体检 + 移植体检】，任一 BLOCK 整体 BLOCK；实跑验证（脏技能 BLOCK、正常技能 PASS、JSON 模式正常）
- ✅ **技能安全审计 SkillSec 16 类**（模式 24）：`scripts/skillsec_audit.py` 静态审计任意技能（含自身），覆盖过度能动/输出处理/叛变特工/触发滥用/MCP 最低特权/提示注入/数据外流/特权升级/供应链/危险 AST/污染追踪/YARA 等 16 类，输出类 SkillSpector 报告（支持 --json/--md，可作 CI 卡点）；方法论借鉴 NVIDIA SkillSpector 公开分类，自有开源实现

## 路线图与已落地状态

**第一轮（8 模块，已全落地）**：体系规划师 / 生命周期 Ops(含弃用归档) / 持续进化器 / 跨平台适配器 / 技能发现复用 / ROI 筛选 / 培训推广包 / 流程技能生成器。

**第二轮增强（已落地）**：
- ✅ **Agentic 治理**（模式 15）：评估/护栏/可观测/责任归属/人机协同（`references/agentic-governance.md`）
- ✅ **选题透镜**（模式 16）：PEST/波特五力/价值链作技能选题上游透镜（`references/scoping.md`）
- ✅ **技能编排器**（模式 17）：多技能串工作流（`references/composer.md` + `scripts/compose.py`）
- ✅ **评测套件生成器**（模式 18）：应触发/不应触发/边界动态评测（`references/evaluation.md` + `scripts/eval_gen.py`）
- ✅ **成熟度模型 Agentic 维度**（扩展模式 8 / `maturity_assess.py`，向后兼容）
- ✅ **审查器 AI 安全加固**（扩展模式 5 / `review_checklist.py`：PII/凭据/外部输入校验）

**第三轮可用性增强（已落地）**：
- ✅ **统一 CLI 入口**（模式 19）：`scripts/studio.py` 调度全部脚本（`studio review/compose/eval/maturity/portal/usage ...`）
- ✅ **成本/计量追踪**（模式 20）：`scripts/usage_tracker.py` 半自动 usage 日志 → ROI 闭环
- ✅ **技能门户生成器**（模式 21）：`scripts/portal.py` 技能库 → 门户目录/HTML
- ✅ **发布前卡点 gate**（模式 22）：`studio gate --skill <dir> [--platform codex]` 双体检——回答"要安装/要移植的技能，安全和可移植性是否同时通过"

**第四轮自更新（已落地）**：
- ✅ **自更新（模式 23）**：`scripts/update_skill.py` 从钉置到不可变发布标签的可信仓库拉取归档、SHA256SUMS 完整性校验、合并白名单、增量更新本技能副本；支持检查/应用/备份/干跑/JSON；更新前快照可回滚，git 仓库自动保护不误覆盖；默认仅检查、需确认才应用（详见 SECURITY.md）

**第五轮安全审计能力（已落地）**：
- ✅ **技能安全审计 SkillSec 16 类（模式 24）**：`scripts/skillsec_audit.py` 借鉴 NVIDIA SkillSpector 公开 16 类漏洞模式，自有开源实现，对任一技能（含本技能自身）做类 SkillSpector 式静态安全审计，输出「类别/严重度/置信度/证据/发现」报告，支持 --json/--md 可作 CI 卡点；配套 `references/skill-spector-method.md` 方法论文档（含借鉴声明）

**技能当前规模**：24 能力模式 / 19 份 reference / 16 个脚本。

**本轮新增已落地**：打包 v1.0(README+VERSION+安装说明，已升 v1.0.1) / 跨平台实测(WorkBuddy·Codex·TRAE WORK 三平台验证) / 发布前双体检 gate / 自更新模式23 / 上架 ClawHub 市场(MIT-0)。

**可继续的方向（未做）**：真实企业样例库(替代 cases.md 的理论占位) / 更多平台实测(Cursor·Claude Code 等) / CI 自动 gate 卡点工作流。

> 实现任一模块时，在顶部"能力模式"追加对应入口，并把方法论落到 `references/` 或 `scripts/`。
