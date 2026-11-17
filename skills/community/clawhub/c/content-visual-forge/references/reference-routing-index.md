# Reference Routing Index

本文件只做路由索引，不复制规则正文。运行时以 `SKILL.md` 为入口，根据任务类型读取下列最小必要文件。

## Core Workflow

- 输入识别：`references/workflows/00-input-router.md`
- Source Lock：`references/workflows/01-source-lock.md`
- 输出模式路由：`references/workflows/02-output-mode-router.md`
- 执行模式路由：`references/workflows/03-execution-mode-router.md`
- 内容分析：`references/workflows/04-content-analysis.md`
- 插画语法路由：`references/workflows/04E-illustration-grammar-routing.md`
- 创意微资产路由：`references/config/creative-micro-assets.md`
- PixiJS 生图增强层：`references/config/pixijs-generated-visual-layer.md`
- 稀有风格探索：`references/config/style-exploration-lab.md`
- 内容压缩阶梯：`references/config/content-compression-ladder.md`
- 内置设计原则：`references/config/design-principles.md`
- 设计增强路由：`references/config/design-enhancement-routing.md`
- 插画语法：`references/config/illustration-grammar.md`
- 视觉导演系统：`references/config/visual-direction-system.md`
- 分页脚本：`references/workflows/05-carousel-script.md`
- 公众号文内配图路由：`references/workflows/06-wechat-inline-image-routing.md`
- 卡片字段填充：`references/workflows/07-card-data-fill.md`
- 封面概念：`references/workflows/08-cover-concept.md`
- 图像提示词：`references/workflows/09-image-prompt-generation.md`
- Prompt / Render Package：`references/workflows/10-prompt-and-render-package.md`
- 批量生成：`references/workflows/11-batch-generation.md`
- 质量复核与重试：`references/workflows/12-quality-review-retry.md`
- 工程化渲染升级：`references/workflows/13-engineering-rendering.md`

## Output Families

- 公众号封面：`references/template-families/cover-card/README.md`
- 公众号文内配图：`references/template-families/wechat-inline-image/README.md`
- 社交平台组图：`references/template-families/social-card/README.md`
- 系列知识卡：`references/template-families/knowledge-carousel/README.md`
- 单字卡：`references/template-families/character-card/README.md`
- 词汇 / 语法 / 短语卡：`references/template-families/learning-card/README.md`

## Family-Specific Style And Layout

- 知识卡默认视觉：`references/config/visual-style.md`
- 知识卡 / 社交卡页面结构：`references/config/layout-system.md`
- 单字卡视觉规则：`references/config/character-card-style.md`

## Source Adapters

- 适配器总览：`references/source-adapters/README.md`
- PDF：`references/source-adapters/pdf-adapter.md`
- 网页：`references/source-adapters/webpage-adapter.md`
- 文本：`references/source-adapters/text-adapter.md`
- 图片 / 截图：`references/source-adapters/image-adapter.md`
- 视频转写稿：`references/source-adapters/video-adapter.md`
- 音频转写稿：`references/source-adapters/audio-adapter.md`
- PPT / Slides：`references/source-adapters/slides-adapter.md`
- 多源混合：`references/source-adapters/mixed-media-adapter.md`

## Quality And Constraints

- 输出契约：`references/config/output-contract.md`
- 平台规格：`references/config/platform-specs.md`
- 设计原则：`references/config/design-principles.md`
- 设计增强边界：`references/config/design-enhancement-routing.md`
- 创意微资产边界：`references/config/creative-micro-assets.md`
- PixiJS 生图增强边界：`references/config/pixijs-generated-visual-layer.md`
- 风格探索实验边界：`references/config/style-exploration-lab.md`
- 视觉导演系统：`references/config/visual-direction-system.md`
- 素材来源策略：`references/config/asset-source-policy.md`
- 风险动作黑名单：`references/config/risk-action-blacklist.md`
- 内容忠实度：`references/config/content-fidelity-checklist.md`
- 视觉质量：`references/config/quality-checklist.md`
- 反抄袭：`references/config/anti-plagiarism.md`
- 中文排版：`references/config/typography-rules.md`
- 公众号配图数量：`references/config/wechat-image-count-rules.md`
- 最大闭环检查：`references/config/maximum-closure-checklist.md`
- 单字卡 Schema：`references/schemas/character-card-schema.md`
- 学习卡 Schema：`references/schemas/learning-card-schema.md`

## Cover Engine

- 封面内容意图：`references/cover-engine/tasks/content_intent_analysis.md`
- 封面风格路由：`references/cover-engine/tasks/style_routing.md`
- 封面视觉概念：`references/cover-engine/tasks/visual_concept.md`
- 封面标题排版任务：`references/cover-engine/tasks/layout_typography.md`
- 封面 Prompt Builder：`references/cover-engine/tasks/prompt_builder.md`
- 封面输出契约：`references/cover-engine/tasks/output_contract.md`
- 封面质量任务：`references/cover-engine/tasks/quality_gate.md`
- 封面审美原则：`references/cover-engine/rules/aesthetic_principles.md`
- 封面风格分类：`references/cover-engine/rules/style_taxonomy.md`
- 封面生产 / 预览边界：`references/cover-engine/rules/production_vs_preview.md`
- 文本渲染策略：`references/cover-engine/rules/text_rendering_strategy.md`
- 封面排版：`references/cover-engine/rules/typography_layout.md`
- 杂志 / 瑞士网格封面设计系统：`references/cover-engine/rules/editorial-design-system.md`
- 画家风格图鉴转译：`references/cover-engine/rules/painter-style-atlas.md`
- 画家风格图鉴数据：`assets/style-atlas/qiaomu-style-atlas.snapshot.json`
- 画家风格图鉴刷新脚本：`scripts/style-atlas/fetch_qiaomu_style_atlas.py`
- 视觉复杂度预算：`references/cover-engine/rules/visual_complexity_budget.md`
- 生成后质量门禁：`references/cover-engine/rules/post_generation_quality_gate.md`
- 安全与版权：`references/cover-engine/rules/safety_copyright.md`

## Production Rendering

- 工程化渲染总览：`references/render-engine.md`
- PixiJS 生图增强：`references/config/pixijs-generated-visual-layer.md`
- HTML 模板：`assets/render-engine/html-templates/`
- CSS 样式：`assets/render-engine/css/`
- 示例数据：`assets/render-engine/data/`
- 渲染脚本：`scripts/render-engine/render-with-playwright.js`

## Run Log And Regression

- 运行记录规范：`references/run-log/RUN_LOG_SPEC.md`
- 回归用例：`tests/regression-suite/`
- benchmark eval：`evals/evals.json`
