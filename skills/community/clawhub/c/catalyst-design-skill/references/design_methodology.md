# 催化剂设计方法论体系（分层 · 可追溯 · 可演进） | Catalyst Design Methodology System (Layered · Traceable · Evolvable)

> 本文件是 catalyst-design 的核心知识库。方法论持续融合多来源证据（见"来源标签"），并按四层体系组织，支持动态更新（机制见 `methodology_update_protocol.md`）。
> This file is catalyst-design's core knowledge base. The methodology continuously fuses multi-source evidence (see "Source tags"), is organized in four layers, and supports dynamic updates (mechanism in `methodology_update_protocol.md`).
> 每条方法论均标注 **来源标签 + 置信度 + 更新日期**，便于审核与演进。生成设计建议时，应优先引用高置信度且有明确来源的条目；若用户提供 catalyst-search 文献矩阵，则以其中具体体系/指标为准并回填本库。
> Each entry is tagged with **source + confidence + update date** for audit and evolution. When generating advice, prefer high-confidence, well-sourced entries; if the user supplies a catalyst-search matrix, follow its specific systems/metrics and backfill this base.

---

## 来源标签体系（可追溯性约定）| Source-tag system (traceability convention)

| 标签 Tag | 含义 Meaning | 审核优先级 Audit priority |
|---|---|---|
| `[CS]` | 来自 catalyst-search 检索的最新公开文献<br>Latest public literature from catalyst-search | 高—含 DOI 可回溯<br>High — DOI-traceable |
| `[AI]` | 用户经 AI 对话 / 其他 skill 获取的文献资料<br>Literature the user obtained via AI chat / other skills | 中—需补 DOI 校验<br>Medium — needs DOI check |
| `[EXT]` | 其他外部渠道（会议、专利、标准、行业报告、课题组内部数据）<br>Other external channels (conferences, patents, standards, industry reports, group-internal data) | 中—注明具体出处<br>Medium — name the exact source |
| `[EXP]` | 经验推测/跨体系类比，尚无直接文献<br>Empirical guess / cross-system analogy, no direct literature yet | 低—标注"待验证"<br>Low — mark "to verify" |

**置信度 | Confidence**：★★★（多来源交叉验证 / multi-source cross-validated）/ ★★（单一可靠来源 / single reliable source）/ ★（经验或单点证据 / empirical or single-point）。
**条目编号 | Entry ID**：`层号.序号`（如 L1.03 / e.g., L1.03），与 `methodology_registry.md` 台账一一对应 / maps 1:1 to `methodology_registry.md`.

---

## L1 · 基础理论层（Theory）——为什么这样设计 | Why design this way

| 编号 ID | 方法论条目 Methodology entry | 来源 Src | 置信 Conf | 更新 Updated |
|---|---|---|---|---|
| L1.01 | **构效关系驱动**：性能差异 → 追溯结构根源（尺寸/有序度/电子结构/载体）→ 反推合成策略<br>**Structure-property driven**: performance gap → trace to structural root (size/ordering/electronic structure/support) → infer synthesis | [CS] | ★★★ | 2026-07-23 |
| L1.02 | **d 带中心理论**：合金化/应变/掺杂调节 d 带中心相对费米能级位置，优化中间体吸附强度（Sabatier 原理，"过强/过弱皆不利"）<br>**d-band center**: alloying/strain/doping shift the d-band center vs E_F to tune intermediate adsorption (Sabatier: too strong/weak both bad) | [CS] | ★★★ | 2026-07-23 |
| L1.03 | **电子结构优先于几何结构**：掺杂与金属-载体相互作用(MSI)调控常比单纯尺寸调控更高效<br>**Electronic structure > geometry**: doping & MSI tuning often beats mere size control | [CS] | ★★ | 2026-07-23 |
| L1.04 | **反应机理分型决定设计方向**：OER 区分 AEM(吸附质演化) vs LOM(晶格氧)——LOM 活性高但易致晶格失稳/金属溶解；HER 区分 Volmer/Heyrovsky/Tafel，碱性下水解离(Volmer)常为速控步<br>**Mechanism typing sets direction**: OER AEM vs LOM (LOM active but lattice-unstable/dissolving); HER Volmer/Heyrovsky/Tafel, water dissociation (Volmer) often RDS in base | [CS] | ★★★ | 2026-07-23 |
| L1.05 | **活性—稳定性权衡**：有序化/核壳提升稳定性但可能牺牲活性，按场景(酸性 PEMWE / 燃料电池 / 碱性)取舍<br>**Activity-stability trade-off**: ordering/core-shell boost stability but may cost activity; choose per scenario (acidic PEMWE / fuel cell / alkaline) | [CS] | ★★ | 2026-07-23 |
| L1.06 | **缺陷即活性**：合理缺陷(空位/晶界/长程无序)是活性位点来源，但过度缺陷损害稳定性<br>**Defects are activity**: sensible defects (vacancy/grain boundary/long-range disorder) are active sites, but excess defects hurt stability | [CS] | ★★★ | 2026-07-23 |
| L1.07 | **双功能协同**：异质界面分工(如 MoS₂ 管 H* 吸附、Ni 位点管水解离)可突破单一材料 Sabatier 极限<br>**Bifunctional synergy**: heterointerface division of labor (e.g., MoS₂ for H* adsorption, Ni for water dissociation) breaks single-material Sabatier limit | [CS] | ★★ | 2026-07-23 |

## L2 · 方法工具层（Methods & Tools）——用什么手段实现 | What means to use

### 2A 合成方法库 | Synthesis library
| 编号 ID | 方法 Method | 适用/特点 Applicable / features | 来源 Src | 置信 Conf | 更新 Updated |
|---|---|---|---|---|---|
| L2.01 | 强静电吸附 (SEA) | 亚 3 nm 金属间化合物，精确尺寸与有序度控制<br>Sub-3 nm intermetallics; precise size & ordering control | [CS] | ★★★ | 2026-07-23 |
| L2.02 | 低熔点金属掺杂 (Ga/Sn) | 降低有序化温度(可至 ≤450 °C)，键强调控降能垒，支持十克级放大<br>Lowers ordering temp (≤450 °C), bond-strength tuning, gram-scale scale-up | [CS] | ★★★ | 2026-07-23 |
| L2.03 | 配体锚定 (苯胺辅助) | 温和退火(~650 °C)得高有序度(89.8%)，抑制烧结<br>Mild anneal (~650 °C) → high ordering (89.8%), anti-sintering | [CS] | ★★ | 2026-07-23 |
| L2.04 | 单源双金属前驱体热解 | 保证原子级混合，高温直接得高有序相(~1150 °C, ~80%)<br>Single-source bimetallic precursor → atomic mixing, high-order phase (~1150 °C, ~80%) | [CS] | ★★ | 2026-07-23 |
| L2.05 | Joule heating (焦耳热) | 快速高温抑制团聚，制高分散单原子/高熵合金<br>Rapid high-T suppresses agglomeration; highly dispersed SAC / HEA | [CS] | ★★ | 2026-07-23 |
| L2.06 | 模板法(软/硬/尿素辅助) | 介孔/分级多孔结构，空间限域抑烧结<br>Meso/hierarchical pores; spatial confinement vs sintering | [CS] | ★★ | 2026-07-23 |
| L2.07 | 微波辅助 / 连续流 | 窄尺寸分布，利于放大<br>Narrow size distribution; scale-up friendly | [CS] | ★★ | 2026-07-23 |
| L2.08 | 液相还原 / Adams Fusion | IrO₂ 等经典氧化物制备<br>Classic oxide prep (e.g., IrO₂) | [CS] | ★★ | 2026-07-23 |
| L2.09 | 掺杂+后处理(N/S 共掺、酸洗、CO₂ 蚀刻) | 引入活性位、调掺杂量、温和调孔<br>Introduce sites, tune doping, mild pore control | [CS] | ★★ | 2026-07-23 |
| L2.10 | 晶界工程 / 长程无序调控(B 掺杂扰动结晶度) | 提升酸性 OER 活性与稳定性(RuO₂)<br>Boosts acidic OER activity/stability of RuO₂ | [CS] | ★★ | 2026-07-23 |

### 2B 表征与计算工具 | Characterization & computation
| 编号 ID | 工具 Tool | 用途 Use | 来源 Src | 置信 Conf | 更新 Updated |
|---|---|---|---|---|---|
| L2.20 | XRD 超晶格峰 / HAADF-STEM | 有序度定量与原子级成像<br>Ordering quantification & atomic imaging | [CS] | ★★★ | 2026-07-23 |
| L2.21 | XPS / EXAFS(XAS) | 电子结构、结合能位移、配位数(有序度)<br>Electronic structure, BE shift, coordination (ordering) | [CS] | ★★★ | 2026-07-23 |
| L2.22 | operando Raman / DEMS | 原位机理(LOM 晶格氧参与判定)<br>In-situ mechanism (LOM lattice-O participation) | [CS] | ★★ | 2026-07-23 |
| L2.23 | DFT / 机器学习筛选 | ΔG_H*、水解离能垒、d 带中心计算与高通量筛选<br>ΔG_H*, water-dissociation barrier, d-band; high-throughput screening | [CS] | ★★ | 2026-07-23 |
| L2.24 | 结构数据库(Materials Project) | 候选相/晶体结构参考<br>Candidate phases / crystal structures | [EXT] | ★★ | 2026-07-23 |

### 2C 结构设计手段 | Structural design
| 编号 ID | 手段 Means | 内容 Content | 来源 Src | 置信 Conf | 更新 Updated |
|---|---|---|---|---|---|
| L2.30 | 尺寸效应 | 亚 3 nm 颗粒 / 单原子分散最大化原子利用率<br>Sub-3 nm / SAC maximize atom utilization | [CS] | ★★★ | 2026-07-23 |
| L2.31 | 有序化(金属间化合物) | L1₀-PtCo 等有序相较无序合金更稳定、抗溶解<br>L1₀-PtCo etc. more stable/dissolution-resistant than disordered | [CS] | ★★★ | 2026-07-23 |
| L2.32 | 核壳/界面工程 | Ru@IrOₓ 电荷重分布、核壳保护活性核<br>Ru@IrOₓ charge redistribution, core-shell protects active core | [CS] | ★★ | 2026-07-23 |
| L2.33 | 载体设计 | 介孔/分级多孔碳、N/S 掺杂载体、载体缺陷协同<br>Meso/hierarchical C, N/S-doped support, support-defect synergy | [CS] | ★★ | 2026-07-23 |
| L2.34 | 单/双原子位点 | 分散活性位、双原子协同(如 Fe-SAs 诱导有序化)<br>Dispersed sites, dual-atom synergy (e.g., Fe-SAs induce ordering) | [CS] | ★★ | 2026-07-23 |

## L3 · 技术参数层（Parameters）——具体参数窗口 | Concrete parameter windows

| 编号 ID | 参数 Parameter | 推荐窗口/规律 Recommended window / rule | 来源 Src | 置信 Conf | 更新 Updated |
|---|---|---|---|---|---|
| L3.01 | 有序化退火温度 | 依策略 450–1150 °C：低熔点掺杂 ≤450 °C / 苯胺辅助 ~650 °C / 单源前驱体 ~1150 °C<br>By strategy 450–1150 °C: low-melt doping ≤450 / aniline ~650 / single-source ~1150 | [CS] | ★★★ | 2026-07-23 |
| L3.02 | 降温速率 | 慢冷(≤2 °C/min)穿越有序化温区，促超晶格畴长大；急冷冻结无序态<br>Slow cool (≤2 °C/min) through ordering window grows superlattice domains; quench freezes disorder | [CS]+[EXT] | ★★ | 2026-07-23 |
| L3.03 | 退火气氛 | H₂/Ar 还原+抑烧结；NH₃/Ar 用于 N-C 体系；纯 Ar 防载体损耗<br>H₂/Ar reduction + anti-sinter; NH₃/Ar for N-C; pure Ar protects support | [CS] | ★★ | 2026-07-23 |
| L3.04 | 粒径目标 | ORR 优选亚 3–4 nm(兼顾活性与稳定)，工艺宽容可用 ~6 nm<br>ORR prefer sub-3–4 nm (activity+stability); ~6 nm if process-tolerant | [CS] | ★★ | 2026-07-23 |
| L3.05 | 掺杂量 | 低熔点/杂原子掺杂需权衡(过量牺牲本征活性)，一般个位数 at.% 起扫<br>Doping needs trade-off (excess hurts intrinsic activity); start at single-digit at.% | [EXP] | ★ | 2026-07-23 |
| L3.06 | 组分配比 | L1₀ 相取近化学计量比(如 Pt:Co≈1:1)<br>L1₀ takes near-stoichiometric ratio (e.g., Pt:Co≈1:1) | [CS] | ★★★ | 2026-07-23 |
| L3.07 | 后处理 | 酸洗去不稳定相/调掺杂；淬火调制 MSI<br>Acid wash removes unstable phases / tunes doping; quench modulates MSI | [CS] | ★★ | 2026-07-23 |

## L4 · 实践验证层（Validation）——如何证明有效 | How to prove it works

| 编号 ID | 验证项 Validation | 规范/基准 Spec / benchmark | 来源 Src | 置信 Conf | 更新 Updated |
|---|---|---|---|---|---|
| L4.01 | 分级评测 | RDE 初筛(本征 ECSA/MA/TOF) → MEA 器件验证，避免"论文高活性、器件失效"<br>RDE screening (intrinsic ECSA/MA/TOF) → MEA device validation; avoid "high paper activity, dead device" | [CS] | ★★★ | 2026-07-23 |
| L4.02 | 评价标准 | 遵循 TCASMES 400-2024 / T/CRES 0030-2025<br>Follow TCASMES 400-2024 / T/CRES 0030-2025 | [EXT] | ★★ | 2026-07-23 |
| L4.03 | 性能基准(ORR) | DOE 2025 目标 MA≥0.44 A/mg_Pt；先进 L1₀-PtCo 0.67–1.21，高熵可达 2.4<br>DOE 2025 target MA≥0.44 A/mg_Pt; advanced L1₀-PtCo 0.67–1.21, HEA up to 2.4 | [CS] | ★★★ | 2026-07-23 |
| L4.04 | 性能基准(酸性 OER) | η₁₀=175–192 mV，Tafel 34.5 mV dec⁻¹，稳定 300–1100 h<br>η₁₀=175–192 mV, Tafel 34.5 mV dec⁻¹, stable 300–1100 h | [CS] | ★★★ | 2026-07-23 |
| L4.05 | 性能基准(碱性 HER) | η₁₀=29–80 mV，Tafel 31–52 mV dec⁻¹，水解离能垒可降至 ~0.5 eV<br>η₁₀=29–80 mV, Tafel 31–52 mV dec⁻¹, water-dissociation barrier down to ~0.5 eV | [CS] | ★★★ | 2026-07-23 |
| L4.06 | 有序度验证 | XRD 超晶格峰(L1₀-PtCo (001)~23.9°/(110)~32.9°)+峰强比；HAADF-STEM<br>XRD superlattice (L1₀-PtCo (001)~23.9°/(110)~32.9°) + intensity ratio; HAADF-STEM | [CS] | ★★★ | 2026-07-23 |
| L4.07 | 稳定性/耐久 | 3 万圈 ADT 保持率；酸性 OER 关注 Ru/Ir 溶解(ICP 监测)<br>30k-cycle ADT retention; acidic OER watch Ru/Ir dissolution (ICP) | [CS] | ★★★ | 2026-07-23 |
| L4.08 | 放大验证 | 优先验证十克级可行性，为工程化铺路<br>Prioritize gram-scale feasibility for engineering | [CS] | ★★ | 2026-07-23 |

---

## 使用规则（生成设计建议时）| Usage rules (when generating advice)
1. **来源优先级 | Source priority**：用户提供的 [CS] 文献矩阵 > 本库 [CS]/[AI]/[EXT] 高置信条目 > [EXP] 经验推测。
   - User-supplied [CS] matrix > in-base high-confidence [CS]/[AI]/[EXT] > [EXP] guess.
2. **必须标注 | Must label**：引用某条方法论时，在建议书中带出其来源标签与（若有）DOI，区分"文献已证实"与"经验推测"。
   - When citing an entry, surface its source tag and DOI (if any); distinguish confirmed vs guessed.
3. **冲突处理 | Conflict handling**：新旧证据冲突时，以置信度更高、时效更新者为准，并在 registry 记录变更。
   - On conflict, follow higher-confidence / newer evidence and log the change in the registry.
4. **回填机制 | Backfill**：若本次用到用户新提供的文献产生了新规律，按 `methodology_update_protocol.md` 回填本库与 `methodology_registry.md`。
   - If new user literature yields new rules, backfill this base and `methodology_registry.md` per the protocol.
