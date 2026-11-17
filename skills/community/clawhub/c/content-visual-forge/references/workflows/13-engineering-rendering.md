# Workflow 13 · Engineering Rendering

当需要商用稳定交付时，优先采用工程化渲染。

## 适合场景

- 大批量单字卡
- 大批量词汇卡
- 小红书 / Rednote 社交组图
- 公众号封面对
- 公众号文内配图模板化输出
- 需要真实背景、照片、纹理或品牌素材的 HTML / CSS 输出
- 纯 HTML/CSS 模板视觉质量不足，需要 AI 生图主体或 PixiJS canvas 叠层增强的正式输出
- 教学资产库
- 课程配套卡片
- 需要 100% 控制中英文字段的正式交付

## cover-card
- 背景图由图像模型生成
- 标题、副标题、标签通过 HTML/CSS、Canvas、PPT 或设计工具叠加
- 公众号封面对必须分别渲染 `2100 x 900` 与 `1080 x 1080`，不得硬裁

## social-card
- 优先使用单 HTML 多 frame
- 每个 frame 遵守 `1080 x 1440`、安全区和稳定命名
- 截图、代码、表格等证据素材优先保证可读性
- 设计增强默认使用设计原则；缺少额外设计能力时不影响渲染
- 设计增强只改视觉 token、layout variants 和 CSS，不改来源事实
- 背景照片、纹理、logo 或产品图必须按 `asset-source-policy.md` 写入 `asset_source_record[]`

## wechat-inline-image
- 保持低文字或无文字
- 不使用页码胶囊
- 根据文章类型和阅读节奏决定数量

## character-card / knowledge-carousel / learning-card
- AI 负责脚本、字段和风格说明
- 程序负责固定模板排版与批量导出

## background assets
- 优先使用 CSS 纹理、抽象图形、AI 生成无文字背景或用户授权素材。
- 使用公共图片、免费图库、官方 press kit 或 CC 素材时，必须记录来源 URL、许可证、署名要求、商用限制和访问日期。
- 授权不明时不得硬编码远程 URL；改为本地占位、抽象背景或请求用户确认。

## PixiJS enhanced export

当 `pixijs_generated_visual_layer.enabled=true`：

- 工程渲染不再承担“用 HTML/CSS 画出高级主视觉”的全部责任；HTML/CSS 主要负责安全区、精确文字、平台尺寸和截图导出。
- AI 生图负责无文字主体、情绪背景或场景底图。
- PixiJS canvas 负责粒子、光效、流体感、抽象数据流、sprite 组合、景深感或 motion-study 静态帧。
- Playwright 截图导出 PNG/JPG/PDF；除非最终交付是 HTML，否则不要承诺动画或可编辑 canvas。
- 精确中文、数字、标签、引用、截图标注必须留在工程文字层或后期排版层。
- 任何外部纹理、字体、logo、截图、产品图都必须进入 `asset_source_record[]`；自生成的程序化视觉可记为 `generated_graphics`。

## 推荐技术路线

- HTML + CSS + Playwright 截图
- SVG 模板渲染
- Canvas 模板渲染
- PixiJS canvas scene + Playwright 静态截图
- PPT 模板批量导出
- Python PIL 批量生成
