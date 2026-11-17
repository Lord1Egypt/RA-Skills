# Workflow 10 · Prompt and Render Package

在脚本或数据准备完成后，生成可执行的提示词或渲染包。

## 全局 Style Atlas 插槽

当 `style_routing` 提供 `atlas_snapshot`、`atlas_family` 或 `style_factors` 时，所有图片提示词 / 渲染包都必须包含：

- `atlas_snapshot`：本地 snapshot 路径与日期
- `atlas_family`：宽风格家族
- `style_factors`：线条、色彩、光线、空间、材质、构图、情绪等可控因子
- `prompt_style_phrase`：可直接进入模型的安全风格短语
- `blocked_mimicry`：不得复制的画家签名、名作构图、IP、品牌或装饰组合

没有用户风格要求时，不强行套用图鉴；保持模板族默认风格。

## cover-card
输出：
- 背景图提示词
- 标题排版规范
- 预览图提示词（如需要）
- 质量检查清单
- 风格因子说明（如使用画家图鉴）

## wechat-inline-image
输出：
- 文内图角色
- 对应段落或阅读节奏位置
- 低文字或无文字图像提示词
- 插画语法块：scene_role、subject_focus、composition_axis、camera_distance、texture_level、text_load、blocked_mimicry
- 可渲染数据块：background_asset、optional_text、text_visibility、asset_source_record
- 不使用页码胶囊的约束
- 公众号文内图数量与用途说明

## social-card
输出：
- 平台规格和安全区
- 内容压缩阶梯结果
- 视觉导演报告：内容类型、传播目标、读者情绪、信息密度、三套风格方向、推荐方案和不推荐方向
- 页面角色列表
- 每页 hook、正文碎片、视觉证据和来源锚点
- 每页视觉关系：与上一页 / 下一页如何递进或变化
- 每页提示词约束：画幅、布局、文字安全区、字体、配色、主视觉、留白和负面提示
- 单 HTML 多 frame 或逐页提示词方案

## knowledge-carousel
输出：
- 每页独立提示词
- 风格锚点说明
- 批量生成顺序建议
- 风格因子说明（如使用画家图鉴）

## character-card
输出：
- 单卡提示词
- 字段填充结果
- 插画关键词
- 工程化渲染字段块
- 风格因子说明（仅当用户要求图鉴风格时）

## vocabulary-card / grammar-card / phrase-card
输出：
- 学习卡字段块
- 模式专项字段
- 批量 style_anchor
- 单卡提示词或工程化渲染数据
- 不自动加入考试 / 等级标签的限制
- 风格因子说明（仅当用户要求图鉴风格时）

## Design Enhancement Routing（可选）
输出：
- `design_source`：`default_rules` 或 `enhanced_review`
- `design_intent`
- `preset`
- `visual_tokens`
- `layout_variants`
- `css_update_notes`
- `asset_requirements`
- `design_qa`

这些字段只能进入提示词或渲染包的视觉层，不得改写 Source Lock、平台规格和内容事实。
没有额外设计能力时，必须用 `design-principles.md` 和 `design-enhancement-routing.md` 继续完成，不得中断。

## PixiJS Generated Visual Layer（可选）
当工程化渲染需要保证文字准确，但纯 HTML/CSS 画面质量过平、模板味强或无法形成高级视觉锚点时，读取
`references/config/pixijs-generated-visual-layer.md`，输出：

- `pixijs_generated_visual_layer.enabled`
- `pixijs_generated_visual_layer.trigger`
- `pixijs_generated_visual_layer.route`
- `pixijs_generated_visual_layer.canvas_role`
- `pixijs_generated_visual_layer.ai_image_role`
- `pixijs_generated_visual_layer.text_policy`
- `pixijs_generated_visual_layer.export_plan`
- `pixijs_generated_visual_layer.quality_checks`
- `pixijs_generated_visual_layer.anti_copy_boundary`

提示词 / 渲染包必须把 AI 生图主体、PixiJS canvas 叠层和文字排版层拆开描述。AI 生图默认生成无文字或低文字背景；PixiJS 只负责粒子、光效、纹理、抽象数据流、sprite 组合或 motion-study 静态帧；中文标题、数据、标签和正文仍交给工程排版或后期叠字。

## Asset Source Policy（使用外部素材时必选）
输出：
- `asset_source_record[]`
- `background_asset_plan`
- `attribution_plan`
- `license_risk_notes`
- `fallback_asset_plan`

HTML / CSS 渲染可以使用背景图片、纸张纹理、照片、截图和 logo，但每个外部素材都必须有来源、许可证、署名要求和商用限制记录。无法确认时，改用 CSS 纹理、抽象图形、AI 生成无文字背景或请求用户补充授权素材。
