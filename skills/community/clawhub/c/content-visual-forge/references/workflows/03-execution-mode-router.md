# Workflow 03 · Execution Mode Router

在 Output Mode Router 之后，必须判断本次任务的执行路径。

## 可选执行模式

- `preview_image`
- `production_cover`
- `background_then_layout`
- `direct_image_preview`
- `prompt_package`
- `engineering_rendering`

`pixijs_generated_visual_layer` 不是独立执行模式，而是
`prompt_package` / `background_then_layout` / `engineering_rendering` 的可选增强层：
当纯 HTML/CSS 工程渲染画面质量差、缺乏深度或模板味明显，但又需要保留精确中文和稳定导出时，读取
`references/config/pixijs-generated-visual-layer.md`，采用“AI 无文字主视觉 + PixiJS canvas 视觉叠层 + 工程文字排版 + 静态截图导出”的混合路线。

## 判定逻辑

### cover-card
- 需要正式公众号封面：优先 `production_cover` 或 `background_then_layout`
- 需要明显画面感、背景主视觉或插画主体：优先 `prompt_package` 生成图像提示词或生图数据，再进入 `background_then_layout`
- 需要更高级的抽象氛围、光效、粒子、数据流或动态帧质感，且 HTML/CSS 渲染显得粗糙时：启用 `pixijs_generated_visual_layer`，只把 PixiJS 作为视觉叠层或静态帧导出
- 只要快速看效果：`preview_image` 或 `direct_image_preview`
- 仅需文字叠层、版式或安全区：`engineering_rendering`
- 无图像能力：`prompt_package`

### wechat-inline-image
- 正文配图快速出样：优先 `direct_image_preview`
- 需要手绘/插画感主体：优先 `prompt_package` 生成图像提示词或生图数据，再进入 `background_then_layout` / 后期排版
- 需要抽象光影、粒子、信号、流动线条或高质量纹理作为文内图视觉锚点时：可启用 `pixijs_generated_visual_layer` 导出静态图，正文文字仍由后期排版控制
- 需要低文字、可发布配图：`prompt_package` 或 `background_then_layout`
- 需要批量稳定版式或精确叠字：`engineering_rendering`
- 不要用 HTML 直接模拟手绘主体；HTML 只负责文字层、版式层和安全区

### social-card
- 快速出样、验证 hook 和页面角色：`direct_image_preview`
- 需要场景感主视觉、插画感封面或情绪化背景：优先 `prompt_package` 生成图像提示词或生图数据，再回到后期排版
- 封面页或关键页需要高质量 canvas 质感，而普通 HTML/CSS 视觉不够时：启用 `pixijs_generated_visual_layer`，通常只用于封面或少数视觉锚点页，不默认套满全套组图
- 需要平台规格声明、内容压缩阶梯和分页脚本：`prompt_package`
- 批量、商用、截图必须精确、中文准确：`engineering_rendering`
- 优先使用单 HTML 多 frame 渲染，确保组图风格一致性

### knowledge-carousel / character-card
- 快速出样：`direct_image_preview`
- 如果某一页更像插画页面而不是信息卡页面，先拆出该页作为 AI 生图内容，再用工程层叠字
- 批量、稳定、商用：`engineering_rendering`
- 无图像能力：`prompt_package`

### vocabulary-card / grammar-card / phrase-card
- 单张快速预览：`direct_image_preview`
- 批量、商用、中文字段必须精确：`engineering_rendering`
- 无图像能力：`prompt_package`
- 不允许把大量中文小字默认交给图像模型排版

## 必须输出

- 执行模式：
- 选择原因：
- 交付物类型：
- 风险提醒：

## 硬性降级 / 升级

- `source_lock.allow_generation = false` 时，不得进入生图；只能要求补充来源或输出带风险标注的 `prompt_package`。
- 文字必须精确且数量超过 8 张时，强制升级到 `engineering_rendering`。
- 本地 Style Atlas 不可用时，不查询外部网站，改用模板族默认风格。
