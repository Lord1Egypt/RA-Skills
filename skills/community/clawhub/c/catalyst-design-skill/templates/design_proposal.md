# 催化剂设计建议书（模板）| Catalyst Design Proposal (template)

> 本模板为 catalyst-design 的标准输出格式。若消费了 catalyst-search 的文献矩阵，请在"文献支撑"列明对应文献序号（与 literature_matrix 序号一致）。
> This is catalyst-design's standard output format. If you consumed catalyst-search's matrix, cite the matching literature numbers (consistent with literature_matrix) under "Literature support".

## 设计目标 | Design goal
- 反应类型 | Reaction type：___（HER / OER / ORR / PEMWE / 光催化 / photocatalysis）
- 材料体系 / 性能诉求 | Material system / performance need：___

## 一、组分选择 | I. Composition selection
- 活性组分 | Active component：___（依据 | basis：___）
- 载体 | Support：___（依据 | basis：___）
- 助剂/掺杂 | Promoter/dopant：___

## 二、结构设计 | II. Structural design
- 几何结构 | Geometry：尺寸 / 分散度 / 有序化 / 核壳（建议 | suggestion：___）
  - size / dispersion / ordering / core-shell
- 电子结构 | Electronic：掺杂 / MSI 调控（建议 | suggestion：___）
  - doping / MSI tuning
- 载体结构 | Support structure：孔道 / 缺陷（建议 | suggestion：___）
  - pores / defects

## 三、合成策略 | III. Synthesis strategy
- 推荐方法 | Recommended method：___（如 SEA / Joule heating / 模板法 / 微波辅助 / e.g., SEA / Joule heating / templating / microwave）
- 选择理由 | Rationale：___

## 四、反应条件优化 | IV. Condition optimization
- 热处理温度/气氛 | Annealing temp/atmosphere：___
- 酸洗/纯化 | Acid wash/purification：___
- 淬火/退火 | Quench/anneal：___
- 评价规范 | Evaluation norm：RDE → MEA（参照 TCASMES 400-2024 / T/CRES 0030-2025 / per TCASMES 400-2024 / T/CRES 0030-2025）

## 五、验证建议 | V. Validation suggestions
- 表征 | Characterization：XRD（颗粒尺寸/晶型 / particle size/phase）、TEM、XPS（价态/电子结构 / valence/electronic structure）
- 电化学 | Electrochemistry：RDE（ECSA/MA/TOF/Tafel）、MEA（器件验证 / device validation）
- 对照实验 | Control experiments：___

## 六、方法论溯源（每条建议标注依据）| VI. Methodology traceability (cite basis per suggestion)
> 依据 catalyst-design 四层方法论体系，标注每条关键建议所用条目编号与来源标签，便于审核。
> Per catalyst-design's four-layer system, label each key suggestion's entry ID and source tag for audit.

| 建议要点 Suggestion | 方法论编号 Methodology ID | 来源标签 Src tag | 置信 Conf | DOI/出处 DOI/source |
|---|---|---|---|---|
| ___（如组分配比 / e.g., composition ratio） | L3.06 | [CS] | ★★★ | ___ |
| ___（如合成策略 / e.g., synthesis strategy） | L2.02 | [CS] | ★★★ | ___ |
| ___ | ___ | ___ | ___ | ___ |

来源标签 | Source tags：[CS] catalyst-search 检索 / [AI] 用户经 AI·skill 获取 / [EXT] 外部渠道 / [EXP] 经验推测。
Source tags: [CS] catalyst-search / [AI] user via AI·skill / [EXT] external / [EXP] empirical guess.

## 七、文献支撑 | VII. Literature support
- [1] ___（GB/T 7714 格式；标注"文献支撑"或"经验推测" / GB/T 7714 format; label "literature-supported" or "empirical guess"）
- [2] ___

## 八、可回填的新规律（供方法论演进）| VIII. New rules to backfill (for evolution)
> 若本次分析产生了方法论库尚未收录的新规律，在此列出，按 update_protocol 校验后回填 registry。
> If this analysis yields rules not yet in the base, list them here; after protocol validation, backfill the registry.
- 新条目 | New entry：___｜层级 | Layer：___｜来源 | Source：___｜置信 | Conf：___｜状态 | Status：pending/active

---
*说明：本建议基于分层方法论体系与（可选的）文献检索结果生成；具体合成须以小试验证，并遵守安全与环保规范。*
*Note: this proposal is generated from the layered methodology system and (optional) literature search; actual synthesis must be validated by experiment and follow safety & environmental rules.*
