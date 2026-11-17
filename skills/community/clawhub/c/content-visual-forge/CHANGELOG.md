# Changelog

## V2.7.2

- 新增 `PixiJS Generated Visual Layer`：
  - `references/config/pixijs-generated-visual-layer.md`：定义 AI 无文字生图主体 + PixiJS canvas 视觉叠层 + 工程文字排版 + 静态截图导出的混合路线。
  - `references/workflows/03-execution-mode-router.md`、`10-prompt-and-render-package.md`、`13-engineering-rendering.md`、`references/render-engine.md`：补齐执行路由、输出字段和工程化渲染边界。
  - `references/config/quality-checklist.md`、`references/core/hard-rules.md`：新增静态导出、文字边界、canvas 非空检查和反复制门禁。
- 扩展创意微资产与元数据：把 PixiJS 纳入局部浏览器视觉层，但不承诺可编辑设计源、可编辑 PPT 或图片交付中的原生动画。
- 新增 pixijs-generated-visual-layer eval，覆盖“纯 HTML/CSS 工程渲染画质差，但中文标题必须精确”的混合生产场景。
- 版本提升到 `v2.7.2`

## V2.7.0 - P2 架构重构

- 解决系统架构师发现的 85% 内容重复问题
- 实施"基类工作流 + 域配置"架构：
  - 提取 `base-card-workflow.md`（450 行，所有域共享）
  - 创建 4 个域配置文件（每个约 50 行，仅差异化内容）：
    - `domain-configs/language-card-config.md`
    - `domain-configs/cover-card-config.md`
    - `domain-configs/carousel-config.md`
    - `domain-configs/social-card-config.md`
  - 重构 4 个完整 workflow 为精简版（从 500 行降至 80 行）
  - 备份原完整版到 `legacy/` 目录
- 架构优势：
  - 通用流程只需维护 1 个文件
  - 新增域只需添加 50 行配置
  - 修改通用逻辑自动影响所有域
  - 解决维护成本高的问题
- 系统架构师评分预估：30/60 → 50/60

## V2.6.1

- P1 改进（基于专家审查反馈）：
  - 在 language-card-workflow.md 添加术语映射说明，明确 language-card（领域层）vs learning-card（模板层）的关系
  - 在 SKILL.md 添加"⚡ 5 分钟快速开始"章节，提供 4 个最小可运行示例
  - 补充 pronunciation-card（发音卡）和 translation-card（翻译卡）类型：
    - 完整的字段定义和数据填充示例
    - 更新路由逻辑和输出模式
    - 覆盖完整的语言学习闭环
  - 降低新用户入门门槛，提升文档易读性

## V2.6.0

- 修复版本号不一致问题：统一 VERSION、SKILL.md、README.md 到 v2.6.0
- 补充缺失的 workflow 文件：
  - `references/workflows/execution-overview.md`：总流程概览，串联 00-10 阶段
  - `references/workflows/cover-workflow.md`：封面生成完整流程
  - `references/workflows/carousel-workflow.md`：系列知识卡流程
  - `references/workflows/social-card-workflow.md`：社交平台组图流程
  - `references/workflows/language-card-workflow.md`：语言学习卡统一流程（单字/词汇/语法/短语）
- 架构优化：
  - 重命名 `learning-card-workflow.md` → `language-card-workflow.md`，明确领域边界
  - 补充领域定位说明，区分语言学习域与其他学习域（STEM、人文社科等）
  - 在 SKILL.md 添加"未来发展路线"章节，预留 STEM、人文社科扩展空间
- 增强 `agents/openai.yaml`：补充 trigger_phrases、examples、capabilities 字段
- 扩充 `evals/evals.json`：补充 social-card、style-exploration、illustration-grammar、creative-micro-assets、engineering-rendering 场景
- 修复所有悬空引用，确保所有链接可达
- 版本提升到 `v2.6.0`

## V2.5.0

- 新增 `Creative Micro Assets Routing`：
  - `references/config/creative-micro-assets.md`：把 ASCII / monospace、手绘图解、Excalidraw 草图源、p5.js / generative canvas 与 DESIGN.md/token note 统一为局部创意媒介层。
  - `SKILL.md`：新增 4F 路由阶段、非协商硬规则和创意微资产视觉系统。
  - `references/config/output-contract.md`、`references/config/quality-checklist.md`、`references/config/design-enhancement-routing.md`：补齐输出字段、质量门禁和设计增强边界。
  - `references/reference-routing-index.md`：加入创意微资产路由入口。
- 新增 creative-micro-assets eval，防止跳过 Source Lock / 平台规格，或复制外部 creative skill 的模板、代码、素材、CSS、配色和视觉签名。
- 版本提升到 `v2.5.0`

## V2.4.2

- 新增插画语法层：
  - `references/config/illustration-grammar.md`：把 scene role、subject focus、composition axis、camera distance、texture level、text load 与 blocked mimicry 统一成插画语法
  - `references/workflows/04E-illustration-grammar-routing.md`：在 Source Lock 和内容分析之后，为文内配图、插画感封面背景和场景化主视觉提供独立路由
- 扩展文内配图与提示词链路：
  - `references/workflows/06-wechat-inline-image-routing.md`：新增何时启用插画语法的判断
  - `references/workflows/09-image-prompt-generation.md`：补充 `illustration_grammar` 输入
  - `assets/templates/image-prompt-template.md`：增加插画语法字段占位
  - `assets/templates/wechat-inline-image-template.md`：新增插画语法块与渲染数据块
- 增强 `wechat-inline-image` 工程化渲染模板：
  - `assets/render-engine/data/wechat-inline.sample.json`：补充 `illustration_grammar`
  - `assets/render-engine/data/wechat-inline-sequence.sample.json`：新增多帧文内插画序列样例
  - `assets/render-engine/html-templates/wechat-inline-image.html`：接入场景语法字段
  - `assets/render-engine/css/wechat-inline-image.css`：新增插画场景约束层样式
  - `references/template-families/wechat-inline-image/README.md`、`references/render-engine.md`：补充插画增强版模板族说明
- 补齐输出契约与质检：
  - `references/config/output-contract.md`：新增插画语法字段
  - `references/config/quality-checklist.md`、`references/workflows/12-quality-review-retry.md`：新增插画语法检查与回退逻辑
- 更新入口与元数据：
  - `SKILL.md`、`references/reference-routing-index.md`、`agents/openai.yaml`
- 版本提升到 `v2.4.2`

## V2.4.1

- 修复数据与流程一致性问题：
  - `wechat-inline.sample.json`: 补充 `background_asset` 和 `asset_source_record`，与 asset-source-policy 要求一致
  - `wechat-inline-image.html`: 背景图改为从 `background_asset.url` 读取，与其他模板的 `background_asset` 模式统一
  - `quality-checklist.md`: 补充 `visual_direction_quality` 检查项
  - `12-quality-review-retry.md`: 通用检查补充视觉导演检查项，决策表新增 `visual_direction_risk` 行
- 删除过时的 `references/run-log/example-run-log.md`，运行记录示例由 `RUN_LOG_SPEC.md` 的最小模板统一承接。
- 删除旧版内部测试报告与 `tests/regression-cases.md`，并将覆盖关系迁移到 `tests/regression-suite/README.md` 的标准测试入口说明。

## V2.4.0

- 修复逻辑一致性问题：
  - `social-card-schema.md`: 修正页码胶囊规则，改为"使用简洁 page-label 形式"，与 HTML/CSS 模板一致
  - `04-content-analysis.md`: 补充 Content Compression Ladder 的触发条件和执行位置
  - `00-input-router.md`: 新增"单字 / 词表 / 结构化表格"输入类型，并提供短路路由提示
  - `manifest.yaml`: social_card 路由补充 style_atlas_assets.qiaomu_snapshot 引用

## V2.3.9

- 新增 `references/config/visual-direction-system.md`，把小红书 / Rednote 视觉导演方法沉淀为受控路由：内容类型、传播目标、读者情绪、信息密度、三套风格方向、页面角色节奏、提示词约束与反模式扫描。
- 将 Visual Direction Routing 接入 `SKILL.md`、reference routing、manifest、social-card 模板族、输出契约、提示词 / 渲染包流程和质量门禁。
- 强化社交平台组图要求：封面更冲击、内页更结构化、截图 / 产品图作为证据层，且必须检查 PPT 感、廉价 AI 科技风、信息过载、伪高级、文字不可读和风格断裂。
- 明确外部小红书视觉 Skill 只能作为方法参考，不复制模板、风格库原文、示例图、素材、CSS 或视觉签名。

## V2.3.8

- 修复 CSS 模板中的文字遮盖和溢出问题：
  - `wechat-cover.css`: 添加 `z-index: 0` 建立层叠上下文，确保文字层正确显示
  - `wechat-inline-image.css`: 增强文字对比度，添加半透明背景和更强的 text-shadow
  - `social-card.css`: 为截图说明添加 `line-clamp` 限制，为总结列表添加 `max-height`
  - `character-card.css`: 优化大字号字符显示，添加 `overflow: hidden` 和 `word-break`

## V2.3.7

- 重新发布公开入口为 `content-visual-forge`，承接已合并的公众号封面、文内配图、社交组图、知识卡与工程化渲染能力。
- 确认旧公开入口 `wechat-cover-generator` 已由 `cover-card` 输出模式承接，公开分发时不再保留独立旧 Skill。
- 同步发布元数据版本，便于 public distribution 覆盖旧公开包。

## V2.3.6

- 将素材来源策略落到 render engine 数据层，`wechat-cover` 与 `social-card` 样例数据新增 `background_asset` 与 `asset_source_record[]`。
- 更新 HTML / CSS 模板，从 JSON 数据读取背景素材和页面视觉素材，不再依赖模板内硬编码背景 URL。
- 强化 `render-with-playwright.js`，渲染前校验素材引用必须存在对应 `asset_source_record`，并阻止 `unknown_or_restricted` 或 `reject` 素材进入截图流程。
- 更新社交卡与封面 schema / render engine 文档，并新增 render asset plumbing eval，覆盖模板真实消费素材来源记录的回归场景。

## V2.3.5

- 新增 `references/config/asset-source-policy.md`，定义 HTML / CSS 背景图、纹理、照片、logo、产品图和公共素材的来源优先级、授权记录和降级策略。
- 将素材来源策略接入 reference routing、manifest、输出契约、质量检查、工程化渲染、Run Log 和风险动作黑名单。
- 明确免费图库素材不是“无版权素材”；正式交付必须记录来源 URL、许可证、署名要求、商用限制和访问日期。
- 新增 asset-source-policy eval，防止渲染包硬编码来源不明远程背景图或跳过公共素材授权记录。

## V2.3.4

- 新增 `references/config/risk-action-blacklist.md`，集中记录 Source Lock、输出路由、文字排版、平台构图、设计增强、版权素材与工程化渲染的高风险动作。
- 将风险动作黑名单接入 `SKILL.md` 硬规则、reference routing、manifest prompt routing、输出契约、质量检查与复核重试工作流。
- 新增 `blacklisted_action_hit` 质量状态，命中时回到对应路由、切换工程化渲染或停止交付。
- 新增 risk-action blacklist eval，覆盖不可读来源硬生成、微信封面对硬裁、复制参考模板和商用精确文字直接生图等失败模式。

## V2.3.3

- 新增 `design-principles.md`，沉淀设计方向、组图结构、Typography First、反通用 AI 味、资产优先级、轻手绘信息图和工程化设计输出原则。
- 将设计增强调整为“默认设计规则 + 非阻断增强能力”，缺少额外设计评审时仍继续生成视觉 token、版式变体、CSS 建议与设计 QA。
- 更新 `design-enhancement-routing.md`、`manifest.yaml`、输出契约、工作流和质量检查，统一使用能力降级表述，减少运行规则中的维护者视角说明。
- 新增 design fallback eval，防止后续把额外设计能力误写成阻断条件。

## V2.3.2

- 新增 `design-enhancement-routing.md`，把本地 `frontend-design`、`huashu-design`、`notion-infographic` 作为受控设计增强层接入。
- 在 `SKILL.md` 中新增 `Design Enhancement Routing` 可选阶段，明确设计增强不能改写 Source Lock、平台规格或内容事实。
- 更新质量门禁，增加设计增强检查，覆盖视觉 token、布局变体、反通用 AI 味、外部设计借鉴边界与移动端可读性。
- 更新 `manifest.yaml`、reference routing 与 eval，补齐设计增强的路由资产和回归用例。
- 梳理业务流程引用关系，把知识卡视觉、单字卡视觉和封面任务文件接入 `reference-routing-index.md` 与 `manifest.yaml`，删除不再被执行路径使用的旧版 cover YAML 配置。

## V2.3.1

- 修复 `02-output-mode-router.md` 遗漏 `social-card` 的问题，补充判定逻辑和与 `knowledge-carousel` 的区别说明
- 修复 `03-execution-mode-router.md` 缺少 `social-card` 执行模式判定的问题
- 修复 `input.schema.json` 执行模式 enum 不完整的问题，补充 `background_then_layout`、`direct_image_preview`、`engineering_rendering`
- 修复 `output.schema.json` 缺少封面对字段的问题，新增 `square_short_title` 和 `cover_pair` 对象
- 修复 `package.json` 版本滞后的问题（2.2.5 → 2.3.1）
- 修复 `SKILL.md` 第 6 节和第 9 节重复的问题，删除重复章节并调整后续编号
- 新增 `social-card-schema.md`，定义社交平台组图的数据结构
- 新增 `social-card` 工程化渲染模板（HTML/CSS/JSON），支持 1080×1440 平台规格
- 更新 `manifest.yaml` 和 `package.json`，添加 `social-card` 渲染资源引用和示例命令

## V2.3.0

- 新增 `social-card` 输出族，用于小红书 / Rednote / 社交平台 3:4 组图，明确它与 `knowledge-carousel` 的边界。
- 新增平台规格规则，覆盖小红书 `1080 x 1440`、微信公众号 `21:9` 主封面 `2100 x 900` 与 `1:1` 方封面 `1080 x 1080`。
- 新增内容压缩阶梯，将长文和转写稿压缩为 `core_claim`、`viewer_promise`、`section_map`、`page_hooks`、`body_fragments` 与 `visual_evidence`。
- 强化质量门禁，加入 3:4 四段密度检查、微信方封面短标题检查、图片来源记录与叠字安全检查。
- 明确借鉴外部社交卡 Skill 时只吸收平台规格、内容压缩、工程化渲染和 QA 机制，不复制 HTML 模板、CSS 类名、WebGL 背景、素材或视觉签名。

## V2.2.5

- 新增 `editorial-design-system` 封面规则，吸收杂志化与瑞士网格设计方法，用于公众号封面的主题预设、标题轴线、字号阶梯、图片槽位与质量门禁。
- 将 editorial / Swiss 封面设计系统接入 manifest、style routing、layout typography、prompt builder、reference routing 与 eval。
- 明确外部设计项目只作为方法借鉴，不复制 HTML 模板、CSS 类名、shader、slide layout ID、素材或视觉签名。

## V2.2.4

- 删除未被运行契约、manifest、references、scripts 或 eval 引用的 `assets/cover-engine/examples/` 遗留演示样例目录。
- 同步根 `README.md` 与 `skills-index.json` 版本信息，恢复 repo 级 validation。
- 补齐 `vocabulary-card`、`grammar-card`、`phrase-card` 的 learning-card 共享契约、schema、模板与 eval 覆盖。
- 将 render engine 升级为 `HTML template + JSON data -> PNG` 的轻量数据驱动渲染，并补充 Playwright 集成测试与依赖声明。
- 增加 Source Lock、质量门禁、Style Atlas 失败路径、生产文字风险的状态字段和 stop / retry / upgrade 决策表。

## V2.2.3

- 将 Qiaomu 画家风格图鉴改为本地 snapshot 数据源，运行时默认读取 `assets/style-atlas/qiaomu-style-atlas.snapshot.json`，不再要求每次生成查询外部网站。
- 新增图鉴刷新脚本 `scripts/style-atlas/fetch_qiaomu_style_atlas.py`，只在维护时抓取元数据；不下载或入库外部生成图片。
- 更新风格路由、Prompt Builder、反抄袭规则、manifest 与 eval，明确 `local_snapshot` 是默认运行策略。
- 将 Style Atlas 设为全生图流程可选模块，补齐知识卡、字卡、批量生成、质量复核、路由 schema 与封面输出 schema 的接口。

## V2.2.2

- 新增画家风格图鉴转译规则：外部图鉴只作为风格观察参考，先提取线条、色彩、光线、空间、材质、构图与情绪等因子，再生成提示词。
- 更新封面风格路由、图像提示词、Prompt Package、反抄袭与版权边界，避免直接仿写具体艺术家或复制图鉴构图。
- 增加图鉴风格回归 eval，防止后续把画家名直接塞进正式生图 Prompt。

## V2.2.0

- 将目录整理为标准 skill 结构：入口与元数据保留在根目录，规则和路由进入 `references/`，可复用模板、提示词、示例与静态渲染资源进入 `assets/`，可执行渲染脚本进入 `scripts/`。
- 合并重复 workflow，形成 `00` 到 `13` 的唯一执行链，避免质量复核和工程化渲染阶段出现双版本。
- 将封面引擎规则目录从 `cover-engine/references/` 规范为 `references/cover-engine/rules/`，避免嵌套 `references` 命名。
- 更新 `SKILL.md`、README 和 `references/reference-routing-index.md`，同步标准路径与资源路由。

## V2.1.2

- 新增 `references/reference-routing-index.md`，把跨模块工作流、模板族、输入适配器、质量门禁、封面引擎与工程化渲染资源集中路由。
- 更新 `SKILL.md` 与 README 的主要目录说明，明确 `references/` 作为索引层而非规则正文堆叠区。

## V2.1.1

- 删除顶层 `examples/` 目录；示例语义已由 `tests/regression-suite/`、`evals/evals.json`、`run-log/` 与各专用模块样例承接。
- 更新 README 目录结构，避免把非运行资产标记为主要目录。

## V2.1

- 删除旧版 `wechat-cover-generator` 独立入口；公众号封面能力统一并入 `content-visual-forge` 的 `cover-card` 输出模式。
- 旧版封面 eval 场景迁移到根级 `evals/evals.json` 的 `wechat-cover` 用例，后续封面回归以 `content-visual-forge` benchmark 为准。
- 新增 `wechat-inline-image` 模板族，专门处理公众号文内配图 / 情绪过渡图 / 分节图 / 尾图。
- 新增公众号配图数量判断规则：根据文章类型、长度、阅读节奏决定生成几张图，而不是默认生成固定数量。
- 新增 `run-log` 运行记录规范，记录输入源、路由决策、生成结果、质检结果与重试建议。
- 新增真实案例回归测试集，覆盖影评随笔、PDF 方法论、单字卡、网页文章、产品介绍、视频转写稿。
- 新增工程化渲染模板骨架，包括 HTML/CSS 模板、示例数据、Playwright 截图脚本与使用说明。
- 强化公众号输出边界：公众号文内图默认无页码、少文字或无文字，重点服务阅读节奏；小红书知识卡才使用页码与高信息密度。

## V2.0

- 融合“多源内容卡片生成 Skill V1.2”与“公众号封面生成器 Skill V2.1”。
- 新增统一总 Skill：`content-visual-forge`。
- 新增 `cover-card` 模板族。
- 新增 `Execution Mode Router`，统一预览、正式封面、提示词包、工程化渲染等执行路径。
- 保留并集成封面生成的风格路由、视觉概念、中文排版策略、质量门禁模块。
- 保留并集成内容卡片的 Source Lock、Output Mode Router、Character Card、Knowledge Carousel 模块。
- 统一反抄袭与内容忠实度规范。
