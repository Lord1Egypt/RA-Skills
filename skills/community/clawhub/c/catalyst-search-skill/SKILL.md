---
name: catalyst-search
version: 1.0.5
homepage: https://github.com/ANDYPENG09/catalyst-search-skill
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
allowed-tools: WebSearch WebFetch
requires: WebSearch, WebFetch
description: Catalysis literature search skill. Given a user-provided catalyst topic, reaction type, or material system, retrieve and organize relevant catalysis research papers from the open web (ScienceDirect, arXiv, OpenAlex, Google Scholar, etc.) and output structured literature-review information (literature matrix, supporting conclusions, and validation suggestions). Can collaborate with catalyst-design — its structured output is consumed directly as catalyst-design's input.
agent_created: true
---

# Catalyst Search

## When to use

- Users asking to search catalyst literature, find catalyst papers, retrieve a specific catalyst, do a literature review, survey catalyst research progress, or gather a few papers on a given topic.
- Typical input: catalyst topic, reaction type (HER / OER / ORR / PEMWE / photocatalysis), and material system (Pt/C, PtCo, HEA, SAC, IrO₂, etc.).

## When NOT to use

- Catalyst design or selection advice (composition, synthesis route) — use `catalyst-design`; this skill only retrieves literature and gives no design advice.
- Non-catalysis literature search (e.g., pure organic synthesis, medicinal chemistry) — not applicable.
- Fetching a single paper with a known DOI — use WebFetch directly.

## Prerequisites

- Requires `WebSearch` (topic=academic) and `WebFetch`; without them retrieval is not possible.
- Ships with search essentials (`references/`) and output templates (`templates/`); depends on no paid-database account.

## Input interface

- **Required**: search topic (natural language, must contain at least one of: reaction type, material system, performance target).
- **Optional**: time range, language preference, open-access-only restriction.

## Search essentials (generic dimensions for building queries)

- **Reaction types**: hydrogen evolution reaction (HER), oxygen evolution reaction (OER), oxygen reduction reaction (ORR), overall water splitting, proton exchange membrane water electrolysis (PEMWE), anion exchange membrane (AEM), photocatalysis, plastic upcycling.
  - Always distinguish acidic vs alkaline media: the mechanism, catalyst, and benchmark for the same reaction differ greatly between acid and base. For example, only Ir / Ru-based catalysts are stable for acidic OER; the rate-determining step of alkaline HER is water dissociation.
  - Reaction-specific keyword lists, performance benchmarks, and mechanism / characterization terms are detailed in `references/reaction_systems.md` (with literature-backed benchmark values for judging relevance and advancement).
- **Catalyst systems**: Pt/C, Pt-Co alloy / intermetallic, high-entropy alloy (HEA), single-atom catalyst (SAC), core-shell, IrO₂ / IrOₓ, Ru@IrOₓ, N/S-doped carbon, MOF-derived.
- **Performance metrics**: overpotential at 10 mA cm⁻², ECSA, mass activity (MA, A/mg_Pt), turnover frequency (TOF), Tafel slope, stability / durability.
- **Characterization and testing**: XRD (particle size), TEM, XPS, rotating disk electrode (RDE), membrane electrode assembly (MEA).
- **Synthesis methods**: Joule heating, strong electrostatic adsorption (SEA), microwave-assisted, continuous-flow.
- **Abbreviation expansion**: PtCo → "Pt-Co alloy" OR "Pt cobalt intermetallic"; HEA → "high-entropy alloy"; SAC → "single-atom catalyst".
- **Journal and source distribution**: prioritize high-impact-factor (IF) journals, highly cited papers, and literature from the last 5–10 years. English: use high-IF journals (Adv. Energy Mater., Nat. Commun., Angew. Chem., Energy Environ. Sci., J. Power Sources, Chem. Eng. J, ScienceDirect / Elsevier, ACS, RSC, Nature family) and highly cited papers as priority sources. Standards and patents (TCASMES 400-2024, T/CRES 0030-2025, corporate patents) remain valid sources.

## Workflow

1. **Semantic parsing and query generation**. Combine reaction type, catalyst system, and performance / characterization; expand abbreviations as above; connect synonyms with OR.
2. **Parallel search**. Use `WebSearch` (topic=academic) in parallel per group. Prioritize authoritative sources: ScienceDirect (https://www.sciencedirect.com/), arXiv (https://arxiv.org/), OpenAlex (https://openalex.org/), Google Scholar.
   - Fallback (M2b): if a group returns empty or times out, relax the query (split AND to OR, drop qualifiers) or switch source (search Google Scholar / OpenAlex directly). If all groups return empty, state honestly that no relevant literature was found; never fabricate.
3. **Fetch abstracts**. For the 3–5 most relevant papers, use `WebFetch` to grab the abstract page (prefer journal site, Semantic Scholar, arXiv, PubMed; behind a paywall, abstract + metadata + DOI suffice). Abstracts alone are enough to judge relevance; full-text download or citation is unnecessary.
4. **Extract metadata**. Title, authors, journal / source, year, DOI, abstract highlights.
5. **Filter, deduplicate, and rank**. Rank by relevance, impact factor (IF) or citation count, and recency (prefer last 5–10 years); label OA availability (obtained / online / paywalled / manual).
   - Result validation (M5b): verify DOI / abstract accessibility via WebFetch for each paper (paywalled papers need at least metadata); deduplicate (same DOI or normalized title); keep only papers whose abstract explicitly contains the target reaction type and catalyst system; drop keyword-only hits.
6. **Output**. Literature matrix, supporting conclusions, and validation suggestions per `templates/literature_matrix.md`. Citation format: `templates/citation_gb7714.md`.

## Output interface (standard format, consumed by catalyst-design)

- Output the literature matrix in the table format of `templates/literature_matrix.md` with fields: No. / Title / Authors / Journal·Source / Year / DOI / Reaction type / Catalyst system / Key metrics / OA status / Abstract highlights / Relevance.
- After the matrix, append two sections: **Supporting conclusions** (evidence summary for the research question) and **Validation suggestions** (XRD / TEM / XPS characterization, RDE / MEA tests, control experiments).
- This output is treated as the "literature search result" and can be fed directly into `catalyst-design` (see catalyst-design's "Input interface").

## Data sources

- ScienceDirect (https://www.sciencedirect.com/), arXiv (https://arxiv.org/), OpenAlex (https://openalex.org/), Google Scholar.
- Catalyst structural data refer to Materials Project (https://next-gen.materialsproject.org/apps); retrieve its public pages via WebFetch. This skill does no built-in computation.

## Capability boundaries

- See `references/capabilities.md`.

## Division of labor

- This skill only retrieves and organizes literature; catalyst design advice is handled by `catalyst-design`.
- Only WebSearch (academic) and WebFetch are used; no built-in or copied internal interfaces of other specialized search tools.

## Notes

- Over-strict AND combinations easily return empty; relax or split groups (e.g., search HER + Pt + HEA separately then merge).
- Cited papers must be verifiable; validate DOI / abstract via WebFetch; never fabricate.
- Note the search source (open web) and availability status at the end of output.
- Search-result fields vary widely; parse title / authors / source / year from WebSearch output blocks yourself.
- **Safety and permissions**: this skill only accesses public academic pages via WebSearch / WebFetch; runs no system commands, writes no user files, logs into no paid database, and collects or exfiltrates no user data.

## Common pitfalls (anti-patterns)

- **Treating search output as design advice.** This skill only retrieves and organizes literature; do not derive catalyst composition or synthesis recommendations from the matrix alone — hand off to `catalyst-design`.
- **Fabricating or guessing DOIs.** Never invent a DOI or metadata. If a paper lacks a verifiable DOI, mark it "unverified" and say so; do not fill the matrix with plausible-but-fake identifiers.
- **Over-strict AND queries returning empty.** Combining too many AND constraints yields no results; relax or split groups (search HER + Pt + HEA separately, then merge) per the M2b fallback.
- **Citing keyword-only hits as relevant.** Drop papers whose abstract does not explicitly contain the target reaction type and catalyst system (M5b validation).

## Example

- **Input**: search "alkaline HER single-atom catalysts, last 5 years".
  - **Output**: a literature matrix (3–5 papers with full fields) + supporting conclusions (e.g., Ru SAs / N-C reaches η₁₀ = 29 mV, water-dissociation barrier ≈ 0.5 eV) + validation suggestions (XPS for atom dispersion, RDE for η₁₀ / Tafel, DFT for ΔG_H*).

## Project home

- **GitHub**: https://github.com/ANDYPENG09/catalyst-search-skill — source, updates, and issue tracker.
- **Companion skill**: https://github.com/ANDYPENG09/catalyst-design-skill — catalyst design guidance.

---

# 催化文献检索

## 何时使用

- 用户咨询:查催化文献、找催化剂论文、检索某类催化剂、做文献综述、了解催化剂研究进展、或收集某主题的几篇论文。
- 典型输入:催化剂主题、反应类型(HER / OER / ORR / PEMWE / 光催化)、材料体系(Pt/C、PtCo、HEA、SAC、IrO₂ 等)。

## 何时不使用

- 催化剂设计 / 选型建议(组分、合成路线)—— 用 `catalyst-design`,本技能只检索文献,不给设计建议。
- 非催化领域的文献检索(如纯有机合成、药物化学)—— 不适用。
- 仅需查一个已知 DOI 的论文 —— 用 WebFetch 直接抓取即可。

## 前置条件

- 需 `WebSearch`(topic=academic)与 `WebFetch` 工具可用;二者不可用则无法检索。
- 本技能自带检索要点(`references/`)与输出模板(`templates/`),不依赖任何付费数据库账号。

## 输入接口

- **必填**:检索主题(自然语言,含以下之一即可:反应类型、材料体系、性能目标)。
- **可选**:时间范围、语种偏好、是否仅限 OA。

## 催化领域检索要点(通用检索维度,用于构造检索式)

- **反应类型**:析氢反应(HER)、析氧反应(OER)、氧还原反应(ORR)、全解水、质子交换膜水电解(PEMWE)、阴离子交换膜(AEM)、光催化、塑料升级回收。
  - 务必区分酸性 / 碱性介质:同一反应在酸 / 碱下机理、催化剂、评价基准差异大。如酸性 OER 只有 Ir / Ru 基稳定;碱性 HER 速控步是水解离。
  - 各反应体系(HER / OER / ORR / 全解水)的专门检索词表、性能基准、机理与表征关键词详见 `references/reaction_systems.md`(含文献支撑基准值,用于判断文献相关性与先进性)。
- **催化剂体系**:Pt/C、Pt-Co 合金 / 金属间化合物、高熵合金(HEA)、单原子催化剂(SAC)、核壳、IrO₂ / IrOₓ、Ru@IrOₓ、N / S 掺杂碳、MOF 衍生。
- **性能指标**:过电位(10 mA cm⁻² 处)、ECSA、质量活性(MA, A/mg_Pt)、周转频率(TOF)、Tafel 斜率、稳定性 / 耐久性。
- **表征与测试**:XRD(粒径)、TEM、XPS、旋转圆盘电极(RDE)、膜电极组件(MEA)。
- **合成方法**:Joule heating、强静电吸附(SEA)、微波辅助、连续流。
- **缩写扩展**:PtCo → "Pt-Co alloy" OR "Pt cobalt intermetallic";HEA → "high-entropy alloy";SAC → "single-atom catalyst"。
- **期刊 / 来源分布**:优先选用高影响因子(IF)期刊、高被引文章与近 5–10 年内的文献。英文文献以高 IF 期刊(如 Adv. Energy Mater.、Nat. Commun.、Angew. Chem.、Energy Environ. Sci.、J. Power Sources、Chem. Eng. J,及 ScienceDirect / Elsevier、ACS、RSC、Nature 子刊等)与高被引文章为优先来源;标准 / 专利(TCASMES 400-2024、T/CRES 0030-2025、企业专利)仍可作来源。

## 工作流

1. **语义解析 + 检索式生成**。按"反应类型 + 催化剂体系 + 性能指标 / 表征"组合;缩写按上节扩展;同义词用 OR 连接。
2. **并行检索**。用 `WebSearch`(topic=academic)并行检索各组;权威来源优先 ScienceDirect(https://www.sciencedirect.com/)、arXiv(https://arxiv.org/)、OpenAlex(https://openalex.org/)、Google Scholar。
   - 失败降级(M2b):若某组返回空或超时,放宽(拆 AND 为 OR、去限定词)或换源(直接检索 Google Scholar / OpenAlex);若全部为空,如实告知"未检索到相关文献",不得编造。
3. **抓取摘要**。对最相关 3–5 篇用 WebFetch 抓摘要页(优先期刊官网 / Semantic Scholar / arXiv / PubMed;付费墙内抓到摘要 + 元数据 + DOI 即可)。仅凭摘要即可判断是否为目标文献,无需下载或引用全文。
4. **提取元数据**。标题、作者、期刊 / 来源、年份、DOI、摘要要点。
5. **过滤去重 + 排序**。按相关性、影响因子(IF) / 被引量、时效性(优先近 5–10 年)排序;标注 OA 可获取状态(已获取 / 在线 / 付费 / 手动)。
   - 结果校验(M5b):对每篇用 WebFetch 验证 DOI / 摘要可访问(付费墙至少元数据存在);去重(同 DOI / 规范化标题);仅保留摘要明确含目标反应类型与催化剂体系的文献,剔除仅关键词命中但不相关者。
6. **输出**。按 `templates/literature_matrix.md` 输出文献矩阵 + 支撑结论 + 验证建议。引用格式见 `templates/citation_gb7714.md`。

## 输出接口(标准格式,供 catalyst-design 消费)

- 必须以 `templates/literature_matrix.md` 的表格格式输出文献矩阵,字段:序号 / 标题 / 作者 / 期刊·来源 / 年份 / DOI / 反应类型 / 催化剂体系 / 关键指标 / OA 状态 / 摘要要点 / 相关性。
- 矩阵后附两段:**支撑结论**(对研究问题的证据总结)、**验证建议**(XRD / TEM / XPS 表征、RDE / MEA 测试、对照实验)。
- 本输出即视为"文献检索结果",可直接作为 `catalyst-design` 的输入(参见 catalyst-design 的"输入接口")。

## 数据源

- ScienceDirect(https://www.sciencedirect.com/)、arXiv(https://arxiv.org/)、OpenAlex(https://openalex.org/)、Google Scholar。
- 催化剂结构数据参考 Materials Project(https://next-gen.materialsproject.org/apps),用 WebFetch 检索其公开页面;本技能不内置计算。

## 能力边界

- 详见 `references/capabilities.md`。

## 与其他能力分工

- 本技能仅负责文献检索与整理;催化剂设计建议由 `catalyst-design` 负责。
- 仅使用 WebSearch(academic)与 WebFetch;不内置、不复制任何其他专用检索工具的内部接口。

## 注意事项

- 多重 AND 组合过苛易返回空,宜放宽或拆组(如 HER + Pt + HEA 三组分别检索再合并)。
- 引用文献必须真实可查;用 WebFetch 验证 DOI / 摘要,不得编造。
- 输出末尾注明检索来源(开放网络)与可获取状态。
- 检索结果字段差异大,WebSearch 返回块需自行解析标题 / 作者 / 来源 / 年份。
- **安全与权限**:本技能仅用 WebSearch / WebFetch 访问公开学术网页;不执行系统命令、不写入用户文件、不登录任何付费数据库、不收集或外传用户数据。

## 常见误用(反模式)

- **把检索结果当设计建议**:本技能只检索与整理文献,不要仅凭文献矩阵推导催化剂组分或合成方案,应转交 `catalyst-design`。
- **编造或臆测 DOI**:绝不虚构 DOI 或元数据;若某论文无可核实 DOI,标注"未核实"并说明,不要用看似合理但虚假的编号填空。
- **过严的 AND 组合导致空结果**:多重 AND 叠加易返回空,宜放宽或拆组(HER + Pt + HEA 分别检索再合并),见 M2b 失败降级。
- **把仅关键词命中的文献当相关**:剔除摘要未明确含目标反应类型与催化剂体系的论文,见 M5b 结果校验。

## 示例

- **输入**:检索"碱性 HER 单原子催化剂,近 5 年"。
  - **输出**:文献矩阵(3–5 篇,含标题 / 作者 / 期刊 / 年份 / DOI / 反应类型 / 催化剂体系 / 关键指标 η₁₀ 与 Tafel / OA 状态 / 摘要要点 / 相关性)+ 支撑结论(如"Ru SAs / N-C 的 η₁₀ 低至 29 mV,水解离能垒降至 ≈ 0.5 eV")+ 验证建议(XPS 确认单原子分散、RDE 测 η₁₀ / Tafel、DFT 算 ΔG_H*)。

## 项目主页

- **GitHub**:https://github.com/ANDYPENG09/catalyst-search-skill —— 源码、更新与 Issue 反馈。
- **配套技能**:https://github.com/ANDYPENG09/catalyst-design-skill —— 催化剂设计指导。
