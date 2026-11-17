# Design Enhancement Routing

本文件定义 `content-visual-forge` 的设计增强能力。设计增强必须先使用默认基线完成；额外设计能力只能补充视觉方向、CSS 建议或评审，不能替代内容事实和平台约束。

## 何时启用

满足任一条件时启用：

- 用户明确要求“美化”“设计感”“高级感”“多做几个视觉方向”“评审一下好不好看”。
- 输出进入 `engineering_rendering`，需要更新 HTML / CSS 模板、视觉 token 或多 frame 版式。
- `social-card`、`cover-card`、`wechat-inline-image` 的交付需要更明确的风格系统，而不是默认模板。
- 质量检查发现通用 AI 味、信息层级弱、移动端可读性差、装饰过多或组图风格不统一。
- `social-card` 已完成 Visual Direction Routing，且需要把方向落成 HTML / CSS、视觉 token、模板变量或设计 QA。
- 需要把外部设计项目或额外设计能力的经验转成方法论，但不能复制模板、CSS 类名、素材或视觉签名。

不满足这些条件时，不要为了“显得更会设计”额外启用设计增强。

## 前置条件

启用前必须已经完成：

1. Source Lock。
2. Output Mode Router。
3. Execution Mode Router。
4. 平台规格与安全区声明。
5. 文字准确性与内容压缩边界。

设计增强不得补充来源中没有的事实，不得把文案压缩到失真，也不得为了版面美感删除关键证据。

## 能力降级

默认使用以下资料完成设计增强：

- `references/config/design-principles.md`
- `references/config/design-enhancement-routing.md`
- `references/config/visual-direction-system.md`
- `references/config/quality-checklist.md`
- `references/config/visual-style.md`
- `references/config/layout-system.md`
- `references/render-engine.md`
- `assets/render-engine/`

如果没有额外设计能力，继续使用默认 preset、visual tokens、layout variants、CSS notes 和 design QA。缺少增强能力不是失败条件。

## 可选增强能力

### `frontend-design`

可用于生产级 HTML / CSS 模板增强：

- 视觉 token：字体、字号阶梯、颜色、边距、圆角、阴影、边线、图片槽位。
- CSS 结构：变量、组件状态、多 frame 一致性、响应或截图尺寸稳定性。
- 反通用 AI 味：避免默认渐变、随机装饰、同质化卡片、无意义大圆角和低信息密度。
- 适合 `social-card`、`cover-card`、`wechat-inline-image` 的工程化渲染模板。

### `huashu-design`

可用于设计方向探索和评审：

- 生成 2-3 个差异化设计方向，供用户选择。
- 对已有 HTML / CSS 或截图做专家评审。
- 对涉及具体品牌、产品、软件、地点或人物的视觉物料，提醒先确认事实与核心资产。
- 适合封面、交互演示、品牌视觉方向、动效 Demo 或需要 Playwright 截图验证的任务。

### `notion-infographic`

可用于明确的松弛手绘信息图风格：

- 只在用户要求 Notion 风格、手绘信息图、轻松涂鸦、黄黑线稿等方向时启用。
- 可以作为 `social-card` 或 `knowledge-carousel` 的风格 preset。
- 不作为默认知识卡风格；不要把所有内容都改成 Notion 手绘。

### `creative-micro-assets`

可用于局部创意媒介选择：

- 只在用户要求 ASCII / monospace、手绘图解、Excalidraw 草图源、p5.js / generative canvas、PixiJS canvas、DESIGN.md/token note，或当前页面确实需要小型创意资产来解释内容时启用。
- 必须读取 `references/config/creative-micro-assets.md`，输出 `creative_micro_assets`，并保持 Source Lock、平台规格、输出模式和文字精确性边界不变。
- 不作为默认设计增强 preset；不要把所有卡片都改成手绘、ASCII 或 canvas 背景。

## 设计增强输出契约

设计增强层只输出下面这些内容：

- `design_intent`：目标观感和传播语气。
- `preset`：设计方向，如 `editorial-magazine`、`swiss-grid`、`notion-sketch`、`warm-literary`、`product-evidence`。
- `visual_tokens`：颜色、字体、字号阶梯、间距、边框、圆角、图片处理规则。
- `layout_variants`：封面页、观点页、证据页、清单页、总结页等 frame 结构。
- `css_update_notes`：可落到 render engine 的 CSS / HTML 改动建议。
- `asset_requirements`：需要用户提供或可验证来源支持的图片、截图、logo、产品图。
- `design_qa`：移动端缩略图、中文可读性、截图可读性、密度、风格一致性检查。

禁止输出或修改：

- Source Lock 事实。
- 未经来源支持的新论点。
- 平台规格。
- 输出模式和执行模式结论。
- 用户没有授权的品牌资产、图片或设计模板复制。

## 推荐 preset

### `editorial-magazine`

- 适合：公众号封面、文化 / 商业 / AI 观点文章、长文摘要组图。
- 特征：大标题、明确网格、少量副标题、主视觉或留白承重。
- 风险：标题过大遮挡主体；过度杂志化导致移动端副标题不可读。

### `swiss-grid`

- 适合：方法论、产品解释、技术概念、对比分析。
- 特征：强网格、少色彩、高对齐、规则线、编号系统。
- 风险：过冷、像模板；需要用内容证据或标题动词建立传播力。

### `notion-sketch`

- 适合：轻知识、学习笔记、松弛信息图。
- 特征：手绘线条、少色、留白、轻图标。
- 风险：小字不清、风格喧宾夺主、对严肃商业内容显得过轻。

### `warm-literary`

- 适合：中文阅读、散文、影评、文化随笔、教育内容。
- 特征：温暖纸感、书卷感、低对比图片、克制装饰。
- 风险：米色 / 棕色单调；需要用强调色和结构避免一页糊成背景。

### `product-evidence`

- 适合：工具介绍、产品更新、教程、案例复盘、截图驱动的社交组图。
- 特征：截图是证据层，局部放大、标注、对比、步骤与结论并行。
- 风险：截图被裁坏或被标题遮挡；正文必须减少以保截图可读。

## 工作流位置

```text
Source Lock
↓
Output Mode Router
↓
Execution Mode Router
↓
Content Analysis / Compression
↓
Style Atlas Routing（如需要）
↓
Visual Direction Routing（social-card 默认启用）
↓
Design Enhancement Routing（可选）
↓
Creative Micro Assets Routing（可选）
↓
Prompt / Render Package
↓
Batch Generation / Rendering
↓
Quality Gate
```

## 质量门禁

设计增强后的输出必须额外检查：

- 是否仍能追溯到 Source Lock。
- 是否保持平台尺寸、安全区和输出命名。
- 中文标题、正文、页脚、截图是否在手机缩略图上可读。
- 组图是否同一视觉系统，但页面角色有变化。
- 装饰是否有功能：分层、引导、证据标注或情绪控制。
- 是否存在复制外部模板、CSS 类名、素材或视觉签名的风险。
- 是否因“高级感”牺牲了内容密度、证据可见性或标题传播力。
- 启用创意微资产时，是否有用途、落点、渲染路线、文字策略、来源边界和质量检查，且没有复制外部 creative skill 的模板、代码、素材或视觉签名。
