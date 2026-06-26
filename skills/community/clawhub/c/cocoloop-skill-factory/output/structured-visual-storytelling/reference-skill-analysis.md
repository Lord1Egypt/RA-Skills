# 参考能力分析

## 已有能力

### `presentation-generation`

已经沉淀了适合 PPT 的内容组织、页级节奏、答辩型结构和信息图页面要求。

### `infographic-generation`

已经沉淀了适合网页信息图和展示图的纵向叙事、密度控制、视觉分区和图示表达。

### `design_md`

已经验证了让视觉类 Skill 先读取 `references/design.md` 再产出版式，可以显著提升风格稳定性。

## 共同规律

两类能力共享的不是输出格式，而是同一套视觉叙事方法：

- 把材料压缩成有限叙事单元
- 用少数核心结论组织版面
- 用标题、摘要、指标、注释建立层级
- 用流程、矩阵、对比卡、时间线等可视化结构替代纯文字堆砌

## 抽象建议

把这套共同规律上收为 `structured-visual-storytelling`。

底层 adapter 负责：

- `ppt` 的分页与演示节奏
- `web_infographic` 的滚动阅读节奏
- `showcase_graphic` 的单页展示节奏

共享层负责：

- `story_units`
- `design_md`
- `text_hierarchy`
- `infographic_elements`
- `validation_checks`
