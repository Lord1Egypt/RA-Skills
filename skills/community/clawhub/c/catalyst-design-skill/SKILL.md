---
name: catalyst-design
version: 1.0.5
homepage: https://github.com/ANDYPENG09/catalyst-design-skill
category: chemistry
platforms:
  - WorkBuddy
  - Claude Code
  - Cursor
  - OpenClaw
  - Hermes
  - QClaw
  - ima
  - Codex
description: Catalyst design guidance skill. Based on a layered, traceable, and dynamically evolving methodology system (fusing catalyst-search retrieval results, user-acquired materials via AI/skills, and external channels), it provides advice on catalyst composition selection, structural design, synthesis strategy, and performance optimization. Runs standalone; also collaborates with catalyst-search — consuming its structured literature output (matrix) for sharper targeting and feeding new evidence back into the methodology base.
agent_created: true
---

# Catalyst Design

## When to use

- Users asking how to design a catalyst, which composition to pick, how to optimize performance, synthesis-route advice, catalyst formulation, electrocatalyst design, or how to choose synthesis conditions.
- Typical input: design goal (reaction type + material system / performance need). Optional: catalyst-search literature results.
- Covers HER, OER, ORR, PEMWE, overall water splitting, photocatalysis, and plastic upcycling, among other systems.

## When NOT to use

- Pure literature search — use `catalyst-search`; this skill does not re-search.
- Non-catalysis material design (e.g., battery cathodes, semiconductor devices) — not applicable.
- Looking up a specific DOI or full text — use WebSearch / WebFetch directly.

## Prerequisites

- Ships with its own knowledge base (`references/`) and templates (`templates/`); runs with no external dependencies.
- Optional: when WebSearch / WebFetch are available, the skill may trace a specific rule's origin (not required).

## Input interface

- **Required**: design goal — reaction type plus material system or performance need.
- **Optional**: the structured literature output of `catalyst-search` (the `literature_matrix.md` table, supporting conclusions, and validation suggestions).
  - With literature — give targeted advice using its specific systems and metrics, and cite the support.
  - Without literature — give general advice from the built-in methodology (see `references/design_methodology.md`).

## Methodology system (layered, multi-source, traceable, evolvable)

The methodology continuously fuses multi-source evidence, organized in four layers, and evolves dynamically with new literature.

- Full layered knowledge base: `references/design_methodology.md` (each entry carries a source tag, confidence, and update date).
- Dynamic update mechanism: `references/methodology_update_protocol.md`.
- Traceability registry: `references/methodology_registry.md` (trace by ID to source / DOI).

### Four-layer framework

- **L1 — Theory**: structure–property relations, d-band center, Sabatier principle, mechanism typing (AEM / LOM; Volmer–Heyrovsky), activity–stability trade-off, defects as activity, bifunctional synergy.
- **L2 — Methods and tools**: synthesis library (SEA, low-melting doping, ligand anchoring, single-source pyrolysis, Joule heating, templating, grain-boundary engineering), characterization and computation (XRD, STEM, XPS, EXAFS, DFT, ML), structural design (size, ordering, core–shell, support, single- and dual-atom sites).
- **L3 — Parameters**: annealing temperature (450–1150 °C), cooling rate (slow cooling ≤ 2 °C/min), atmosphere, particle size, doping level, composition ratio, post-treatment.
- **L4 — Validation**: RDE → MEA tiered evaluation, applicable standards (TCASMES 400-2024, T/CRES 0030-2025), per-system benchmarks, ordering / stability / scale-up validation.

### Source tags (traceability)

`[CS]` catalyst-search retrieval (with DOI) · `[AI]` user-acquired via AI / skill · `[EXT]` external channel (conference, patent, standard, internal data) · `[EXP]` empirical guess (to verify). Confidence: ★–★★★.

When generating advice, surface the source tag of each cited entry and distinguish "literature-confirmed" from "empirical guess".

## Workflow

1. **Parse input**. Extract the design goal and collect multi-source evidence — catalyst-search matrix `[CS]`, user-provided `[AI]`, external `[EXT]`. If the input is incomplete (missing reaction type or material system), ask the user to clarify first; do not guess.
2. **Match rules by layer**. Map the goal to L1 theory (mechanism direction) → L2 methods (synthesis / characterization) → L3 parameters (windows) → L4 validation (evaluation path).
3. **Generate advice**. Output composition, structure, synthesis, conditions, and validation. Each citation must note its source tag (and DOI) and confidence, and distinguish confirmed from guessed.
4. **Dynamic backfill (evolve, opt-in)**. Only when the user explicitly asks to update the knowledge base (e.g., "update your methodology" / "remember this"): validate new rules per `methodology_update_protocol.md` and backfill the skill's own `references/design_methodology.md` and `references/methodology_registry.md` (source, DOI, confidence, status). Otherwise keep the built-in methodology read-only and do **not** modify any skill files. For under-evidenced (only `[EXP]`) directions, proactively suggest a catalyst-search re-check to upgrade to `[CS]`.
5. **Output**. Write the design proposal per `templates/design_proposal.md` and cite in GB/T 7714 (see catalyst-search's `templates/citation_gb7714.md` or this skill's own copy).

## Output interface

- Design proposal covering composition, structure, synthesis, conditions, and validation; format per `templates/design_proposal.md`.
- When citing literature, give a GB/T 7714 citation and label each item "literature-supported" or "empirical guess".

## Division of labor

- Literature search is `catalyst-search`'s job; this skill does not re-search, only consumes that output or uses its built-in knowledge.
- To trace a specific rule's origin, WebSearch / WebFetch may be used (optional).

## Notes

- Advice must be grounded in the built-in methodology or supplied literature; no ungrounded claims.
- Clearly distinguish "literature-confirmed" from "empirical guess".
- Advice must include an actionable validation path (characterization, testing) for user verification.
- **Safety and permissions**: by default this skill only *reads* its own `references/` and `templates/`; it runs no system commands and makes no network requests beyond optional WebSearch / WebFetch; it collects or exfiltrates no user data. **Optional self-update**: step 4 ("Dynamic backfill") can *write* to the skill's own `references/design_methodology.md` and `references/methodology_registry.md` — but **only when you explicitly enable it** (e.g., "update your methodology"). It never writes to your own files or project directories.

## Example

- **Input**: design an acidic OER catalyst with η₁₀ < 200 mV and stability > 500 h.
- **Output**:
  - Composition: Ru@IrOₓ core–shell (high-activity Ru core, dissolution-resistant IrOₓ shell). `[CS]` ★★★
  - Structure: core–shell interfacial charge redistribution, optimizing oxygen-intermediate adsorption on Ru. `[CS]` ★★★
  - Synthesis: Adams fusion for the IrOₓ shell, followed by reductive Ru deposition. `[CS]` ★★
  - Conditions: anneal at 400–500 °C (too high drives Ru into the shell, too low gives insufficient ordering). `[EXP]` ★
  - Validation: RDE for η₁₀ and Tafel slope; ICP-MS for Ru / Ir dissolution monitoring; 30 000-cycle ADT. `[CS]` ★★★

## Project home

- **GitHub**: https://github.com/ANDYPENG09/catalyst-design-skill — source, updates, and issue tracker.
- **Companion skill**: https://github.com/ANDYPENG09/catalyst-search-skill — catalysis literature search.

---

# 催化剂设计指导

## 何时使用

- 用户咨询:催化剂怎么设计、选什么组分、怎么优化性能、合成路线建议、催化剂配方、电催化剂设计、合成条件怎么选等。
- 典型输入:设计目标(反应类型 + 材料体系 / 性能诉求)。可选:catalyst-search 的文献检索结果。
- 覆盖反应:HER、OER、ORR、PEMWE、全解水、光催化、塑料升级回收等。

## 何时不使用

- 纯文献检索任务 —— 用 `catalyst-search`,本技能不重复检索。
- 非催化领域的材料设计(如电池正极、半导体器件)—— 不适用。
- 仅需查一个具体 DOI 或论文全文 —— 直接用 WebSearch / WebFetch。

## 前置条件

- 本技能自带知识库(`references/`)与模板(`templates/`),无需外部依赖即可运行。
- 可选:当 WebSearch / WebFetch 可用时,可补查特定规律的出处(非必需)。

## 输入接口

- **必填**:设计目标,含反应类型 + 材料体系或性能诉求。
- **可选**:`catalyst-search` 的结构化文献输出,即 `literature_matrix.md` 格式的文献矩阵表 + 支撑结论 + 验证建议。
  - 提供了文献 —— 结合文献中的具体体系与指标,给出针对性建议并标注文献支撑。
  - 未提供文献 —— 基于内置设计方法论(见 `references/design_methodology.md`)给出通用建议。

## 设计方法论体系(分层、多来源、可追溯、可演进)

方法论持续融合多来源证据,按四层体系组织,并可随新增文献动态更新。

- 完整分层知识库:`references/design_methodology.md`(每条带来源标签 + 置信度 + 更新日期)。
- 动态更新机制:`references/methodology_update_protocol.md`。
- 可追溯条目台账:`references/methodology_registry.md`(编号 → 出处 / DOI 逐级溯源)。

### 四层体系

- **L1 基础理论层**:构效关系、d 带中心、Sabatier 原理、反应机理分型(AEM / LOM;Volmer–Heyrovsky)、活性–稳定性权衡、缺陷即活性、双功能协同。
- **L2 方法工具层**:合成方法库(SEA、低熔点掺杂、配体锚定、单源热解、Joule heating、模板、晶界工程等);表征与计算工具(XRD、STEM、XPS、EXAFS、DFT、ML);结构设计手段(尺寸、有序化、核壳、载体、单/双原子)。
- **L3 技术参数层**:退火温度(450–1150 °C)、降温速率(慢冷 ≤ 2 °C/min)、气氛、粒径、掺杂量、组分配比、后处理。
- **L4 实践验证层**:RDE → MEA 分级评测、相关标准(TCASMES 400-2024、T/CRES 0030-2025)、各体系性能基准、有序度 / 稳定性 / 放大验证。

### 来源标签(可追溯性)

`[CS]` catalyst-search 检索文献(含 DOI) · `[AI]` 用户经 AI / skill 获取 · `[EXT]` 外部渠道(会议、专利、标准、内部数据) · `[EXP]` 经验推测(待验证)。置信度:★–★★★。

生成建议时须带出所引条目的来源标签,区分"文献已证实"与"经验推测"。

## 工作流

1. **解析输入**。提取设计目标(反应类型 / 体系 / 性能),并收集多来源证据——catalyst-search 文献矩阵 `[CS]`、用户经 AI / skill 提供的资料 `[AI]`、外部渠道 `[EXT]`。输入不完整(缺反应类型或材料体系)时,先向用户澄清,不臆测。
2. **按四层匹配规律**。目标映射到 L1 理论(选机理方向)→ L2 方法工具(选合成 / 表征手段)→ L3 参数(定参数窗口)→ L4 验证(定评测路径)。
3. **生成建议**。输出组分选择 + 结构设计 + 合成策略 + 条件优化 + 验证建议。每条引用注明**来源标签**(及 DOI)与置信度,区分"文献已证实"与"经验推测"。
4. **动态回填(演进,需显式启用)**。仅当用户明确要求更新知识库时(例如"更新你的方法论 / 记住这条"),才按 `references/methodology_update_protocol.md` 校验后回填本技能自身的 `references/design_methodology.md` 与 `references/methodology_registry.md`(含来源、DOI、置信、状态)。否则保持内置方法论只读,**不**修改任何技能文件。证据不足(仅 `[EXP]`)的方向,主动建议调用 catalyst-search 补检以升级为 `[CS]`。
5. **输出**。按 `templates/design_proposal.md` 输出设计建议书,引用采用 GB/T 7714(格式见 catalyst-search 的 `templates/citation_gb7714.md`,本技能自带同名模板亦可)。

## 输出接口

- 设计建议书(组分 / 结构 / 合成 / 条件 / 验证),格式见 `templates/design_proposal.md`。
- 若引用文献,给出 GB/T 7714 引用,并标明"文献支撑"或"经验推测"。

## 与其他能力分工

- 文献检索由 `catalyst-search` 负责;本技能不重复检索,仅消费其输出或基于内置知识给建议。
- 如需补查特定设计规律的出处,可用 WebSearch / WebFetch(可选,非必需)。

## 注意事项

- 建议须有据(内置方法论或所提供文献),不凭空断言。
- 明确区分"文献已证实"与"经验推测"。
- 设计建议须附带可执行的验证路径(表征 / 测试),便于用户复核。
- **安全与权限**:默认情况下本技能仅*读取*自带 `references/`、`templates/`;不执行系统命令,除可选的 WebSearch / WebFetch 外不发起网络请求,不收集或外传用户数据。**可选的自更新**:工作流第 4 步"动态回填"可*写入*本技能自身的 `references/design_methodology.md` 与 `references/methodology_registry.md` 以演进知识库——但**仅在您显式启用时**(例如"更新你的方法论")才会发生,且绝不会写入您自己的文件或项目目录。

## 示例

- **输入**:设计一个酸性 OER 催化剂,要求 η₁₀ < 200 mV、稳定 > 500 h。
- **输出**:
  - 组分:Ru@IrOₓ 核壳(Ru 核活性高、IrOₓ 壳抗溶)。`[CS]` ★★★
  - 结构:核壳界面电荷重分布,优化 Ru 的含氧中间体吸附。`[CS]` ★★★
  - 合成:Adams Fusion 制 IrOₓ 壳 + 还原沉积 Ru 核。`[CS]` ★★
  - 条件:退火 400–500 °C(过高致 Ru 溶入壳,过低有序度不足)。`[EXP]` ★
  - 验证:RDE 测 η₁₀ / Tafel;ICP-MS 监测 Ru / Ir 溶解;30k 圈 ADT。`[CS]` ★★★

## 项目主页

- **GitHub**:https://github.com/ANDYPENG09/catalyst-design-skill —— 源码、更新与 Issue 反馈。
- **配套技能**:https://github.com/ANDYPENG09/catalyst-search-skill —— 催化文献检索。
