# 各反应体系检索要点（HER / OER / ORR / 全解水） | Search essentials by reaction system (HER / OER / ORR / Overall Water Splitting)

> 用途：为不同电催化反应体系构造精准检索式提供领域词表、性能基准与机理关键词。
> Purpose: provides domain keyword lists, performance benchmarks, and mechanism terms to build precise queries for different electrocatalytic reaction systems.
> 使用方式：先按用户主题定位反应体系 → 取对应"检索关键词"组合检索式 → 用"性能基准"过滤真正有价值的文献 → 用"机理/表征关键词"补充深度检索。
> Usage: locate the reaction system from the user's topic → take the matching "search keywords" to compose a query → filter for truly valuable papers using "performance benchmarks" → deepen retrieval with "mechanism/characterization keywords".
> 说明：以下基准值为近年代表性文献量级，仅用于判断文献相关性与先进性，非绝对阈值。
> Note: benchmark values below are representative magnitudes from recent literature, used only to judge relevance/advancement, not absolute thresholds.

---

## 一、HER（析氢反应，Hydrogen Evolution Reaction）

### 1. 体系细分（务必区分酸性 / 碱性，二者机理与催化剂差异大） | Subsystems (always distinguish acid/base; mechanisms and catalysts differ greatly)
- **酸性 HER**（PEM 电解）：质子直接放电，Volmer–Heyrovsky/Tafel 机理，Pt 系仍最优。
  - **Acidic HER** (PEM electrolysis): direct proton discharge, Volmer–Heyrovsky/Tafel mechanism; Pt-based still best.
- **碱性 HER**（AEM/碱性电解）：需先水解离（Volmer 步为速控步），"水解离 + H* 吸附"双功能是设计核心。
  - **Alkaline HER** (AEM/alkaline electrolysis): requires prior water dissociation (Volmer step is rate-determining); the "water dissociation + H* adsorption" dual function is the design core.

### 2. 催化剂检索关键词 | Catalyst search keywords
- 贵金属 | Noble metals: `Pt/C`、`Ru`、`Ru single atom`、`Pt single atom`、`RuP2`
- 过渡金属/非贵金属 | Transition/non-noble metals: `Ni-Mo`、`MoS2`（1T 相 `1T-MoS2` 活性高于 2H）、`Ni3S2`、`WS2`、`CoP / Ni2P`（磷化物）、`Mo2C`（碳化物）、`NiFe-LDH`、`Ni(OH)2`
  - Transition/non-noble: Ni-Mo, MoS2 (1T phase more active than 2H), Ni3S2, WS2, CoP/Ni2P (phosphides), Mo2C (carbide), NiFe-LDH, Ni(OH)2
- 结构策略 | Structural strategies: `heterostructure / heterointerface`（异质结）、`MoS2/Ni3S4`、`Pt-Ni(OH)2`、`single-atom`、`defect engineering`、`sulfur vacancy`（硫空位活化基面）
  - heterostructure/heterointerface, MoS2/Ni3S4, Pt-Ni(OH)2, single-atom, defect engineering, sulfur vacancy (activates basal plane)

### 3. 性能基准（用于判断文献先进性，文献支撑见下） | Performance benchmarks (for judging advancement; references below)
- **过电位 η₁₀**（10 mA cm⁻²）：先进碱性 HER 可低至 29–80 mV；异质结 1T-MoS2/Ni3S4 达 η₁₀≈44 mV（1 M KOH）[3]
  - **Overpotential η₁₀** (10 mA cm⁻²): advanced alkaline HER as low as 29–80 mV; heterostructure 1T-MoS2/Ni3S4 reaches η₁₀≈44 mV (1 M KOH) [3]
- **Tafel 斜率**：31–52 mV dec⁻¹ 为优（越小动力学越快）；~40–120 mV dec⁻¹ 提示 Volmer–Heyrovsky 机理 [1][2][3]
  - **Tafel slope**: 31–52 mV dec⁻¹ is excellent (lower = faster kinetics); ~40–120 mV dec⁻¹ suggests Volmer–Heyrovsky mechanism [1][2][3]
- **水解离能垒**（碱性关键）：优异体系可将 H₂O 解离能垒从 ~1.0 eV 降至 ~0.5 eV（NiFeRu-LDH）[1]
  - **Water-dissociation barrier** (key in base): excellent systems lower the H₂O dissociation barrier from ~1.0 eV to ~0.5 eV (NiFeRu-LDH) [1]

### 4. 机理/表征检索词 | Mechanism/characterization keywords
- `hydrogen adsorption free energy (ΔG_H*)`、`water dissociation barrier`、`Volmer/Heyrovsky/Tafel step`、`d-band center`
- 表征 | Characterization: `DFT`、`EIS (charge-transfer resistance)`、`Cdl / ECSA`、`operando Raman`

---

## 二、OER（析氧反应，Oxygen Evolution Reaction）

### 1. 体系细分 | Subsystems
- **酸性 OER**（PEMWE 阳极，最苛刻）：强酸+高氧化电位，目前工业唯一稳定材料为 **IrO₂**；RuO₂ 活性更高、成本更低但稳定性差，是主要替代研究方向 [4][5]
  - **Acidic OER** (PEMWE anode, most demanding): strong acid + high oxidation potential; currently IrO₂ is the only industrially stable material; RuO₂ is more active and cheaper but less stable, making it the main alternative research direction [4][5]
- **碱性 OER**（AEM/碱性电解）：非贵金属可用，`NiFe-LDH`、尖晶石、钙钛矿为主力
  - **Alkaline OER** (AEM/alkaline electrolysis): non-noble metals usable; NiFe-LDH, spinel, perovskite are mainstream

### 2. 催化剂检索关键词 | Catalyst search keywords
- 酸性 | Acidic: `IrO2 / IrOx`、`RuO2 / RuOx`、`Ru@IrOx core-shell`、`Ru-based`、`Ir single atom`、`doped RuO2`（B/Ta/W 掺杂）
  - IrO2/IrOx, RuO2/RuOx, Ru@IrOx core-shell, Ru-based, Ir single atom, doped RuO2 (B/Ta/W doping)
- 碱性 | Alkaline: `NiFe-LDH`、`spinel (Co3O4, NiCo2O4)`、`perovskite (BSCF)`、`NiOOH / CoOOH`
- 结构/调控策略 | Structure/regulation: `grain boundary engineering`（晶界）、`lattice strain`（应变）、`long-range disorder`（长程无序）、`double doping`、`core-shell`、`heterojunction`

### 3. 性能基准（文献支撑见下） | Performance benchmarks (references below)
- **过电位 η₁₀**（酸性）：先进 RuO₂ 基可低至 175–187 mV；IrO₂ 双掺杂核壳 ~192 mV [4][5][6]
  - **Overpotential η₁₀** (acidic): advanced RuO₂-based as low as 175–187 mV; IrO₂ double-doped core-shell ~192 mV [4][5][6]
- **Tafel 斜率**：34–50 mV dec⁻¹ 为优（GB-RuO₂ 达 34.5 mV dec⁻¹）[4]
  - **Tafel slope**: 34–50 mV dec⁻¹ excellent (GB-RuO₂ reaches 34.5 mV dec⁻¹) [4]
- **质量活性**：Ir 基 MA 可达 3.36 A mg_Ir⁻¹（η=270 mV）[6]
  - **Mass activity**: Ir-based MA up to 3.36 A mg_Ir⁻¹ (η=270 mV) [6]
- **稳定性**（酸性最关键，务必看）：优异体系 0.1–0.5 M 酸中稳定 300–1100 h；PEM 电解槽级：2 A cm⁻² @ ~1.63–2.0 V，槽寿命 100–500 h [4][5][6]
  - **Stability** (most critical in acid, must check): excellent systems stable 300–1100 h in 0.1–0.5 M acid; PEM stack level: 2 A cm⁻² @ ~1.63–2.0 V, stack life 100–500 h [4][5][6]

### 4. 机理/表征检索词 | Mechanism/characterization keywords
- **两种机理必查**：`adsorbate evolution mechanism (AEM)`（吸附质演化）vs `lattice oxygen mechanism (LOM)`（晶格氧）；LOM 活性高但易致晶格失稳/溶解 [4]
  - **Two mechanisms must be checked**: AEM (adsorbate evolution) vs LOM (lattice oxygen); LOM is more active but prone to lattice instability/dissolution [4]
- `Ru dissolution / demetallation`（溶解失活）、`high-valent Ru/Ir species`、`overpotential @10 mA cm-2`
- 表征 | Characterization: `operando XAS`、`DEMS`（检测晶格氧参与）、`ICP 溶解量监测`
  - operando XAS, DEMS (detects lattice-oxygen participation), ICP dissolution monitoring

---

## 三、ORR（氧还原反应，Oxygen Reduction Reaction，燃料电池阴极） | ORR (fuel-cell cathode)
> 详见文献矩阵典型体系；核心检索词与本项目已建"有序化 PtCo"案例一致。
> See the literature matrix for typical systems; core keywords align with the established "ordered PtCo" case.
- 催化剂 | Catalysts: `Pt/C`、`L1₀-PtCo intermetallic`、`PtNi`、`high-entropy alloy`、`Fe-N-C single atom`、`M-N-C`
- 性能基准 | Benchmarks: 质量活性 MA @0.9 V（DOE 2025 目标 0.44 A/mg_Pt；先进 L1₀-PtCo 0.67–1.21 A/mg_Pt，高熵体系可达 2.4 A/mg_Pt）
  - Mass activity MA @0.9 V (DOE 2025 target 0.44 A/mg_Pt; advanced L1₀-PtCo 0.67–1.21 A/mg_Pt, high-entropy up to 2.4 A/mg_Pt)
- 稳定性 | Stability: 3 万圈 ADT 后 MA 保持率；MEA 级验证（T/CRES 0030-2025 / TCASMES 400-2024）
  - MA retention after 30k ADT cycles; MEA-level validation (T/CRES 0030-2025 / TCASMES 400-2024)
- 关键词 | Keywords: `ordering degree`、`superlattice`、`mass activity`、`half-wave potential (E1/2)`、`accelerated durability test (ADT)`

---

## 四、全解水 / 双功能（Overall Water Splitting / Bifunctional）
- 检索词 | Keywords: `bifunctional HER/OER catalyst`、`overall water splitting`、`cell voltage @10 mA cm-2`、`self-supported electrode`（自支撑，如泡沫镍 NF）
  - bifunctional HER/OER catalyst, overall water splitting, cell voltage @10 mA cm⁻², self-supported electrode (e.g., Ni foam NF)
- 性能基准 | Benchmark: 全解水槽压 @10 mA cm⁻² 越接近 1.5 V（理论）越优，先进体系 ~1.5–1.6 V
  - Overall-water-splitting cell voltage @10 mA cm⁻² closer to 1.5 V (theoretical) is better; advanced systems ~1.5–1.6 V
- 关键词 | Keywords: `NiFe-based`、`heterostructure`、`3D self-supported`

---

## 五、检索式构造示例（组合上述词表） | Example queries (combine the keyword lists above)
- 酸性 OER 稳定性 | Acidic OER stability: `("acidic OER" OR "PEM water electrolysis") AND (RuO2 OR IrO2) AND (stability OR durability) AND overpotential`
- 碱性 HER 异质结 | Alkaline HER heterostructure: `("alkaline HER" OR "hydrogen evolution") AND heterostructure AND (MoS2 OR Ni-Mo) AND "water dissociation"`
- 分组建议 | Grouping tip: 反应体系（酸/碱）+ 催化剂体系 + 性能/机理，三组分别检索再合并，避免多重 AND 返回空。
  - Reaction system (acid/base) + catalyst system + performance/mechanism — search the three groups separately then merge, to avoid empty results from over-stacked ANDs.

---

## 文献支撑（本要点来源，均基于开放网络摘要判定） | References (basis of this note; judged from open-web abstracts)
- [1] Recent advances in transition metal-based electrocatalysts for alkaline hydrogen evolution. *J. Mater. Chem. A*, 2019, C9TA03220G.（NiFeRu-LDH η₁₀=29 mV、Tafel 31 mV dec⁻¹、水解离能垒 0.50 vs 1.02 eV；MoS2/NiCo-LDH 协同）
  - NiFeRu-LDH η₁₀=29 mV, Tafel 31 mV dec⁻¹, water-dissociation barrier 0.50 vs 1.02 eV; MoS2/NiCo-LDH synergy
- [2] An efficient HER catalyst: Pt-modified Ni₃S₂/MoS₂ across full pH range. *Nanoscale*, 2025, D4NR03811H.（Tafel 40–120 mV dec⁻¹ → Volmer–Heyrovsky 机理判定）
  - Tafel 40–120 mV dec⁻¹ → Volmer–Heyrovsky mechanism
- [3] Constructing a 1T-MoS₂/Ni₃S₄ heterostructure ... *Catal. Sci. Technol.*, 2023, 13, 3901, D3CY00616F.（碱性 HER η₁₀=44 mV、Tafel 43 mV dec⁻¹ @1 M KOH，高电流下超越 Pt/C）
  - Alkaline HER η₁₀=44 mV, Tafel 43 mV dec⁻¹ @1 M KOH, surpasses Pt/C at high current
- [4] RuO₂ Catalysts for Electrocatalytic OER in Acidic Media: Mechanism, Activity ... *Molecules* 2024, 29(2), 537.（AEM vs LOM 机理综述；RuO₂ 作为 Ir 替代）；晶界工程 GB-RuO₂ η₁₀=187 mV、Tafel 34.5 mV dec⁻¹、550 h 稳定，*Angew. Chem. Int. Ed.* 2024, e202405798.
  - AEM vs LOM review; RuO₂ as Ir alternative; GB-RuO₂ η₁₀=187 mV, Tafel 34.5 mV dec⁻¹, 550 h stable
- [5] A Long-Range Disordered RuO₂ Catalyst ... *Angew. Chem. Int. Ed.* 2024, 63(50), e202411603.（B 掺杂长程无序 LD-B/RuO₂ η₁₀=175 mV，0.5 M H₂SO₄ 稳定 ~1.6 个月；PEM 槽 1000 mA cm⁻²@1.63 V）
  - B-doped long-range disordered LD-B/RuO₂ η₁₀=175 mV, stable ~1.6 months in 0.5 M H₂SO₄; PEM stack 1000 mA cm⁻² @1.63 V
- [6] Double doping and bi-directional strains for acidic OER (IrO₂). *Catal. Sci. Technol.*, 2024, D4CY00550C.（Tm/Sb 双掺杂核壳 IrO₂ η₁₀=192 mV、MA 3.36 A mg_Ir⁻¹、PEM 槽 500 h）
  - Tm/Sb double-doped core-shell IrO₂ η₁₀=192 mV, MA 3.36 A mg_Ir⁻¹, PEM stack 500 h
