# 方法论条目台账（Traceability Registry）

> 用途：为 `design_methodology.md` 中每条方法论提供**可审计的来源记录**，支持后续审核、更新与淘汰。
> Purpose: an **auditable source record** for every entry in `design_methodology.md`, supporting later review, update, and retirement.
> 每次更新方法论时，按 `methodology_update_protocol.md` 在此同步追加/修改一行。
> On every methodology update, append/modify a row here per `methodology_update_protocol.md`.
> 状态：active（生效）/ superseded（被取代）/ deprecated（废弃）/ pending（待验证）。
> Status: active (in effect) / superseded (replaced) / deprecated (obsolete) / pending (to verify).

## 台账主表 | Registry master table

| 编号 ID | 摘要 Summary | 层级 Layer | 来源标签 Src | 具体出处 / DOI / 标准号 Specific source / DOI / standard | 置信 Conf | 更新日期 Updated | 状态 Status |
|---|---|---|---|---|---|---|---|
| L1.01 | 构效关系驱动设计<br>Structure-property-driven design | L1 理论 | [CS] | ACS Nano 2022, 10.1021/acsnano.2c08919 | ★★★ | 2026-07-23 | active |
| L1.02 | d 带中心/Sabatier 优化吸附<br>d-band center / Sabatier adsorption | L1 理论 | [CS] | Catal. Sci. Technol. 2024 D4CY00550C 等 | ★★★ | 2026-07-23 | active |
| L1.03 | 电子结构优先于几何结构<br>Electronic > geometric structure | L1 理论 | [CS] | ACS Catal. 2024, 10.1021/acscatal.4c03088 | ★★ | 2026-07-23 | active |
| L1.04 | 机理分型(AEM/LOM;Volmer-Heyrovsky)<br>Mechanism typing | L1 理论 | [CS] | Molecules 2024, 29(2), 537 | ★★★ | 2026-07-23 | active |
| L1.05 | 活性—稳定性权衡<br>Activity-stability trade-off | L1 理论 | [CS] | Nat. Commun. 2024, 10.1038/s41467-024-54987-4 | ★★★ | 2026-07-23 | active |
| L1.06 | 缺陷即活性(空位/晶界/长程无序)<br>Defects are activity | L1 理论 | [CS] | Angew 2024 e202411603 | ★★★ | 2026-07-23 | active |
| L1.07 | 双功能界面协同<br>Bifunctional interface synergy | L1 理论 | [CS] | Catal. Sci. Technol. 2023 D3CY00616F | ★★ | 2026-07-23 | active |
| L2.01 | 强静电吸附 SEA | L2 方法 | [CS] | Google Scholar 摘要(SEA sub-3nm PtCo) | ★★★ | 2026-07-23 | active |
| L2.02 | 低熔点金属掺杂(Ga/Sn)<br>Low-melting doping | L2 方法 | [CS] | Nat. Commun. 2023; Nat. Mater. 2024 | ★★★ | 2026-07-23 | active |
| L2.03 | 配体锚定(苯胺辅助)<br>Ligand anchoring (aniline) | L2 方法 | [CS] | ScienceDirect 2023(PtCo/NC 89.8%) | ★★ | 2026-07-23 | active |
| L2.04 | 单源双金属前驱体热解<br>Single-source bimetallic pyrolysis | L2 方法 | [CS] | Angew. Chem. 2023(PtCo(SAc)₄) | ★★ | 2026-07-23 | active |
| L2.05 | Joule heating | L2 方法 | [CS] | iScience 2025, 10.1016/j.isci.2025.114602 | ★★ | 2026-07-23 | active |
| L2.06 | 模板法(软/硬/尿素)<br>Templating (soft/hard/urea) | L2 方法 | [CS] | Nanoscale Horiz. 2025, 10.1039/d5nh00300h | ★★ | 2026-07-23 | active |
| L2.07 | 微波辅助/连续流<br>Microwave / continuous-flow | L2 方法 | [CS] | RSC Adv. 2020, 10.1039/c9ra10140c | ★★ | 2026-07-23 | active |
| L2.08 | 液相还原/Adams Fusion | L2 方法 | [CS] | Catalysts 2019, 10.3390/catal9040318 | ★★ | 2026-07-23 | active |
| L2.09 | 掺杂+后处理(N/S,酸洗,CO₂蚀刻)<br>Doping + post-treatment | L2 方法 | [CS] | Int. J. Hydrogen Energy 2023, 10.1016/j.ijhydene.2023.05.189 | ★★ | 2026-07-23 | active |
| L2.10 | 晶界工程/长程无序(B掺杂)<br>Grain-boundary / long-range disorder | L2 方法 | [CS] | Angew 2024 e202405798 / e202411603 | ★★ | 2026-07-23 | active |
| L2.20 | XRD超晶格/HAADF-STEM | L2 工具 | [CS] | 多篇 PtCo 文献表征<br>Multiple PtCo characterization papers | ★★★ | 2026-07-23 | active |
| L2.21 | XPS/EXAFS | L2 工具 | [CS] | 多篇文献表征<br>Multiple characterization papers | ★★★ | 2026-07-23 | active |
| L2.22 | operando Raman/DEMS | L2 工具 | [CS] | Molecules 2024 537(LOM 判定) | ★★ | 2026-07-23 | active |
| L2.23 | DFT/机器学习筛选<br>DFT / ML screening | L2 工具 | [CS] | J. Mater. Chem. A 2019 C9TA03220G | ★★ | 2026-07-23 | active |
| L2.24 | Materials Project 结构库<br>Materials Project DB | L2 工具 | [EXT] | next-gen.materialsproject.org | ★★ | 2026-07-23 | active |
| L2.30 | 尺寸效应(亚3nm/单原子)<br>Size effect (sub-3nm/SAC) | L2 结构 | [CS] | SEA/N-C 锚定文献<br>SEA/N-C anchoring papers | ★★★ | 2026-07-23 | active |
| L2.31 | 有序化(金属间化合物)<br>Ordering (intermetallic) | L2 结构 | [CS] | L1₀-PtCo 系列文献<br>L1₀-PtCo series | ★★★ | 2026-07-23 | active |
| L2.32 | 核壳/界面工程<br>Core-shell / interface | L2 结构 | [CS] | Chem 2019, 10.1016/j.chempr.2018.11.010 | ★★★ | 2026-07-23 | active |
| L2.33 | 载体设计(介孔/掺杂碳)<br>Support design | L2 结构 | [CS] | Inorg. Chem. Front. 2024, 10.1039/d4qi00637b | ★★ | 2026-07-23 | active |
| L2.34 | 单/双原子位点<br>Single/dual-atom sites | L2 结构 | [CS] | PKU Fe-SAs 诱导 PtCoFe | ★★ | 2026-07-23 | active |
| L3.01 | 有序化退火温度窗口<br>Ordering anneal temp window | L3 参数 | [CS] | 450-1150°C 多策略文献<br>Multi-strategy papers | ★★★ | 2026-07-23 | active |
| L3.02 | 降温速率(慢冷≤2°C/min)<br>Cooling rate (slow ≤2°C/min) | L3 参数 | [CS]+[EXT] | CN110404555A 控温程序<br>Patent CN110404555A | ★★ | 2026-07-23 | active |
| L3.03 | 退火气氛(H₂/Ar,NH₃/Ar)<br>Anneal atmosphere | L3 参数 | [CS] | 多篇文献<br>Multiple papers | ★★ | 2026-07-23 | active |
| L3.04 | 粒径目标(亚3-4nm)<br>Particle-size target | L3 参数 | [CS] | SEA/N-C 文献 | ★★ | 2026-07-23 | active |
| L3.05 | 掺杂量(个位数at.%起扫)<br>Doping level | L3 参数 | [EXP] | 经验推测，待验证<br>Empirical, to verify | ★ | 2026-07-23 | pending |
| L3.06 | 组分配比(近化学计量)<br>Composition ratio | L3 参数 | [CS] | L1₀ Pt:Co≈1:1 文献 | ★★★ | 2026-07-23 | active |
| L3.07 | 后处理(酸洗/淬火调MSI)<br>Post-treatment | L3 参数 | [CS] | Mol. Catal. 2025, 10.1016/j.mcat.2025.115122 | ★★ | 2026-07-23 | active |
| L4.01 | RDE→MEA 分级评测<br>RDE→MEA tiered eval | L4 验证 | [CS] | 通用规范<br>General practice | ★★★ | 2026-07-23 | active |
| L4.02 | 评价标准(TCASMES/T-CRES)<br>Evaluation standards | L4 验证 | [EXT] | TCASMES 400-2024; T/CRES 0030-2025 | ★★ | 2026-07-23 | active |
| L4.03 | ORR 性能基准<br>ORR benchmark | L4 验证 | [CS] | DOE 2025; L1₀-PtCo 文献 | ★★★ | 2026-07-23 | active |
| L4.04 | 酸性 OER 基准<br>Acidic OER benchmark | L4 验证 | [CS] | Angew 2024 e202405798/e202411603 | ★★★ | 2026-07-23 | active |
| L4.05 | 碱性 HER 基准<br>Alkaline HER benchmark | L4 验证 | [CS] | JMCA 2019; Catal Sci Technol 2023 | ★★★ | 2026-07-23 | active |
| L4.06 | 有序度验证(XRD/STEM)<br>Ordering validation | L4 验证 | [CS] | L1₀-PtCo 文献 | ★★★ | 2026-07-23 | active |
| L4.07 | 稳定性/耐久(ADT/ICP溶解)<br>Stability (ADT/ICP) | L4 验证 | [CS] | 多篇文献<br>Multiple papers | ★★★ | 2026-07-23 | active |
| L4.08 | 放大验证(十克级)<br>Scale-up validation | L4 验证 | [CS] | Nat. Mater. 2024 | ★★ | 2026-07-23 | active |

## 变更记录（Change Log）
| 日期 Date | 编号 ID | 变更 Change | 说明 Note |
|---|---|---|---|
| 2026-07-22 | L1–L4(初始部分) | 初始建库<br>Initial build | 从公开文献提炼四维方法论<br>Four-dimension methodology from public literature |
| 2026-07-23 | 全表 All | 体系化重构<br>Systematic rebuild | 升级为四层体系；融合 catalyst-search 检索文献([CS])；增加来源标签/置信度/状态；新增 HER/OER/PtCo 相关条目<br>Upgraded to 4-layer; fused catalyst-search [CS]; added source/confidence/status; new HER/OER/PtCo entries |
| 2026-07-23 | L1.01/L1.03/L1.05/L2.05-09/L2.32/L2.33/L3.07 | 来源补检<br>Source backfill | 经 catalyst-search 补检公开文献后升级为 [CS]，补 DOI<br>Upgraded to [CS] via catalyst-search backfill with DOIs |

> **审计入口 | Audit entry**：如需核查某条方法论依据，按"编号→本表→具体出处/DOI"逐级溯源。
> To audit an entry's basis, trace "ID → this table → specific source/DOI".
