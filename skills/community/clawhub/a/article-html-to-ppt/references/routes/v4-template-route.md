# PPT Smith V4 Template / Path C 路线

## 定位

本页用于已有 Atlas、组件组合计划和 `strict-template` 任务。新任务若主要是克隆原页、替换文字与原生数据、调整页序，优先使用[原页编辑式模板工具](../native-template-workflow.md)。二者均属于 `template`；旧计划不自动迁移，不能把新工作区状态文件交给旧命令执行。

Template 是强模型主导的模板组件编排路线。用户模板提供原生视觉语言和可复用组件，模型
负责理解内容、规划叙事、匹配与组合组件，并在组件不足时按模板风格创作新原生组件。
引擎负责验证组件合同、执行绑定、保持资产、真实渲染和 QA。

```text
完整源材料 + 用户目标 + 用户模板
              ↓
强模型：Content/Evidence Map + Narrative Contract + 高质量 IR + notes
              ↓
模板分析：视觉 token + reviewed Component Atlas + 可组合关系
              ↓
模型：逐页候选匹配 → 组件组合 → 缺口组件原生创作
              ↓
strict plan → 原生绑定/克隆 → 真实渲染 → 内容与视觉复审
```

严格保留模板资产时使用本路线；只参考模板风格并允许重新设计时使用 create，
按[模板风格设计流程](../template-visual-design.md)选择原生预览或可选生图目标。

## Component Atlas

Atlas 不只是形状清单。每个 reviewed 组件必须记录：

- 语义用途和支持的信息拓扑；
- 必需槽位、字段类型和文本容量；
- 元素数量、图表 series/category 容量和表格容量；
- 可组合的父子槽位、等价实例和原生保真度；
- 支持的 archetype、编辑性和已知风险。
- 能否独立成页、最低信息单元、推荐整页配方、必需搭配角色、图表标注要求和禁止场景。
- 内容边界与装饰边界、背景语义和复用时的背景策略；
- 原生宽高比、支持的目标宽高比、响应式方式和不同尺寸下的适配限制；
- 最低标签信息量、最低数字标注和系列页面角色。

应覆盖模板中可复用的图表、表格、KPI 卡、时间线、流程、比较、矩阵、层级、图标卡、
图片框、章节结构、页脚和装饰系统。仅登记两个通用卡片不构成完整模板分析。

## 模型组件编排

每页模型先声明 assertion、证据、拓扑、数据形态、可见文案和 speaker notes，再执行：

1. 计算全部可行模板组件；
2. 优先选择精确匹配的原生组件；
3. 一个组件不足时组合多个 reviewed 组件；
4. 对所有未选择的可行组件记录原因；
5. 没有可行组件时，使用模板 token 编写新的原生组件；
6. 新组件必须声明 `style_reference_component_ids`，明确继承哪些 reviewed 组件的图标、
   填充、线条、层级和空间语法；
7. 新组件通过 QA 后可进入待审核 Atlas 扩展，但不能自动冒充 reviewed 组件。

模板组件是页面里的表达模块，不自动等于一张完整页面。选择主组件后，模型还必须提交
`page_composition`：页面配方与变体、判断/主证据/解释/含义层、实质内容模块、信息单元
数量、关键数字、图表标注和 takeaway。新版模型计划还必须声明模板无关的
`composition_archetype`，由总览、数据证据、机制、案例、比较系列、行动框架、方法、
概念框架等语义合同验证模块角色与信息量，而不是绑定某套模板坐标。普通正文页默认至少包含两个实质模块。聚焦单一判断/证据的页面可显式使用
`focused_message` / `focused_evidence`，声明 `visual_intent`（message、
focal_component_id、reading_order 的模块 ID、rationale、interpretation）。
这两类允许一个实质模块与简短 takeaway，但保留语义层、来源绑定、组件专属容量/
搭配要求、数据标注、真实渲染与逐页视觉复审，不能用来绕过模板组件本身的限制。

全稿按页面配方和实际变体检查节奏，而不是只统计 component family 名称。相同精确变体
不得连续超过两页；长稿必须达到与页数相称的配方多样性。系列页可以保留比较锚点，但
主体图形和解释结构仍应随数据关系变化。

最终节奏还必须基于真实渲染指纹检查。指纹忽略颜色并将左右镜像视为同一骨架，防止
仅改 recipe/variant 名称或把图表从左移到右来伪造多样性。明确的比较系列只有在声明
统一比较锚点、统一尺度和 series context 后才可共享页面网格；主叙事系列超过五页应
合并为小多图或移入附录。

Template 能力不得依赖特定模板。每次上传均从当前 PPTX 动态生成设计证据与 Atlas，
生产模块禁止品牌组件 ID、固定页码、固定颜色和样本报告特判。跨模板要求详见
[V4 Template 通用化合同](v4-template-generalization.md)。

最终报告必须给出 `eligible_component_coverage`：所有存在可行模板组件的页面中，实际复用
模板组件的比例。目标是 100%；低于 100% 必须阻断或逐页解释。

## 内容与备注

页面只承载一个完整判断和少量高价值内容。禁止 OCR 碎片、通用标签、自动省略号和微型
正文。每个正文页必须有 speaker notes，至少包含：

- 演讲叙事；
- 关键证据与来源锚点；
- 数据口径和限制；
- 对图表/插图的解释；
- 建议的讲述顺序。

## 图表、插图和截图

- 可恢复数据的图表、表格必须生成原生可编辑对象，并优先绑定模板图表组件；
- 非数据插图或无法重建的复杂视觉可使用图片，但只允许隔离插图本身；
- 禁止包含源页面正文、导航、页眉、页脚的大面积截图；
- 每幅插图必须有 Exhibit Interpretation Contract：结论、关键数字、说明、影响、限制、
  来源和 notes；
- “把源页裁下来贴进 PPT”不是 Template authoring。

## Fail-closed 门禁

交付候选必须同时通过：

- 内容与来源覆盖；
- 数字和图表数据 provenance；
- speaker-notes 覆盖；
- 可行模板组件复用率；
- 新组件模板风格一致性；
- 原生图表/表格编辑性；
- 无源页截图、无 OCR 碎片、无自动省略号；
- 无 `undefined`、`null`、`NaN`、TBD/TODO 等生成器残留；
- 无重复或重叠的页码对象；
- 正文不低于 12pt，来源、图片说明和页码按各自角色豁免；
- 模型声明的信息单元必须在实际 PPTX 中有足够的绑定语义对象；
- 外部视觉资产必须声明来源、授权状态和内容哈希；
- 页面密度、层级、节奏和全稿样式完整性；
- 页面构成完整性：单组件空壳、缺少解释/含义、定量页无关键数字或无标注均阻断；
- 结构检查、真实渲染、资产保真和 hash-bound 视觉复审。

机器门禁通过只产生 candidate。最终状态必须有人工或高能力视觉模型批准。

## 封面与尾页

封面和尾页是否存在，必须通过 reviewed `page_recipe` 与 `page_guidance` 检测，不能因为
模板中某个内页组件名称含 `cover` 或 `closing` 就误判。若模板没有可独立成页的对应
recipe，Template 路线必须使用 `style_derived_original`：模型从模板字体、色板、留白、
线条、图标和空间语法中自主设计封面/尾页，同时明确它们不是复用页面。

## 当前工程入口

- `component-atlas`：构建 reviewed Atlas；
- `component-inventory`：检查模板组件覆盖；
- `component-atlas-report`：输出适用场景、拓扑、数据类型、容量和限制的人类可读表格；
- `plan-model-template-components`：编译模型显式给出的逐页多组件方案；
- `compose-components`：生成 strict plan；
- `strict-template --final-delivery`：执行组件克隆、原生新组件脚本、备注写入和最终机器门禁；
- `review-template`：将人工或高能力视觉模型的逐页复核绑定到候选 PPTX 与真实渲染哈希。

当 `component_intent.mode=model_authored` 时，模型计划必须给出
`new_component_id`、`author_script`、目标区域和完整内容绑定。运行时调用
`build(slide, context)`，拒绝未绑定正文、区域越界、模板外字体/色彩，以及未在 IR 和
哈希清单中声明的图片。合规的独立源插图使用 `bind:image:<slide_id>:<block_id>`；源页
截图、含正文的裁剪和可重建数据图一律不允许通过该通道。

`template_composition` 也可包含一个显式 `model_authored` 辅助组件，用来补足 Atlas 没有
覆盖的标题条、注释或关系层；已存在可行模板组件的主体槽位仍必须复用，不能借混合编排
绕过候选审计。

旧的确定性长文自动规划和源页截图实验只作为失败样本，不属于正式交付路线。

## 逐页视觉复审记录

新构建报告标记 `visual_review_contract: page_visual_v1`。`review-template` 的外部审核 JSON
须提供 `pages`，逐页包含 slide_index、preview_sha256，以及 hierarchy、reading_order、
template_match、readability、content、editability 六项 `{status: pass|fail, observation: 具体观察}`。
全稿提供 `deck_rhythm` 观察。审核覆盖每个真实预览并绑定其字节哈希，批准时不得有失败项。
该记录证明审核对象与覆盖完整，不提供自动审美打分或审阅者身份认证。
