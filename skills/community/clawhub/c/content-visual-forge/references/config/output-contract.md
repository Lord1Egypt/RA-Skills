# Output Contract

## 正式执行默认输出

### 1. Source Lock 报告

- 输入源类型
- 原始主题
- 核心观点
- 关键结构
- 可视化线索
- 内容边界
- 不确定项

### 2. 输出模式判定

- 输出模式名称
- 选择原因
- 不选择其他模式的原因

### 3. 内容脚本 / 结构化数据

#### 如果是 `cover-card`

输出字段：
- cover_title_loyal_version
- cover_title_marketing_version
- subtitle_optional
- cover_design_family
- theme_preset
- visual_concept
- title_safe_zone
- typography_overlay_spec
- background_image_prompt 或 direct_image_preview_prompt
- cover_pair（如用户要求公众号封面对）

#### 如果是 `wechat-inline-image`

每张输出：
- image_role
- target_paragraph_or_section
- reading_rhythm_purpose
- low_text_copy_optional
- visual_mood
- image_prompt 或 render_data
- no_page_badge

#### 如果是 `social-card`

整组输出：
- platform_spec
- safe_area
- file_naming_plan
- core_claim
- viewer_promise
- page_count
- visual_system

每页输出：
- page_index
- page_role
- hook
- body_fragments
- visual_evidence
- layout_role
- source_anchor

#### 如果是 `knowledge-carousel`

每页输出：
- 页码
- 主标题
- 副标题
- 核心文案
- 视觉元素
- 底部总结句
- 来源锚点

#### 如果是 `character-card`

输出字段：
- character
- pinyin
- meaning_en
- level_tag_optional
- common_words[]
- example_sentence_zh
- example_sentence_pinyin
- example_sentence_en
- useful_phrase_zh
- useful_phrase_pinyin
- useful_phrase_en
- memory_tip_en
- illustration_keywords[]

#### 如果是 `vocabulary-card` / `grammar-card` / `phrase-card`

输出字段：
- card_type
- item_id
- source_anchor
- display_term
- pinyin_or_pronunciation
- meaning_en
- usage_note
- example_sentence_zh
- example_sentence_pinyin
- example_sentence_en
- learner_level_optional
- forbidden_labels[]
- illustration_keywords[]
- mode_specific_fields
- batch

### 3B. 设计增强字段（可选）

仅当启用 `Design Enhancement Routing` 时输出：

- design_source：`default_rules` 或 `enhanced_review`
- design_intent
- preset
- visual_tokens
- layout_variants
- css_update_notes
- asset_requirements
- design_qa

设计增强字段不得覆盖 Source Lock、输出模式、执行模式、平台规格或内容事实。
没有额外设计能力时，`design_source` 应设为 `default_rules`，并继续输出完整设计增强字段。

### 3B-2. 视觉导演字段（社交平台组图默认）

当启用 `Visual Direction Routing`，尤其是 `social-card`、小红书 / Rednote 组图、3:4 图文规划或封面点击力优化时输出：

- visual_direction.content_type
- visual_direction.communication_goal
- visual_direction.reader_emotion
- visual_direction.information_density
- visual_direction.style_candidates.click_first
- visual_direction.style_candidates.save_first
- visual_direction.style_candidates.brand_first
- visual_direction.recommended_style
- visual_direction.not_recommended
- visual_direction.page_role_rhythm
- visual_direction.visual_tokens
- visual_direction.prompt_constraints
- visual_direction.anti_pattern_scan

视觉导演字段不得覆盖 Source Lock、输出模式、执行模式、平台规格、素材来源记录或内容事实。

### 3B-3. 插画语法字段（可选）

当启用 `Illustration Grammar Routing`，尤其是公众号文内配图、插画感封面背景、知识卡主视觉或社交卡场景化表达时输出：

- illustration_grammar.enabled
- illustration_grammar.intensity
- illustration_grammar.scene_family
- illustration_grammar.recurring_subjects
- illustration_grammar.visual_tokens
- illustration_grammar.blocked_mimicry
- illustration_shot_list[]

每个 `illustration_shot_list[]` 条目至少包含：

- scene_role
- subject_focus
- camera_distance
- composition_axis
- motion_state
- environment_density
- text_load
- source_anchor
- prompt_style_phrase

插画语法字段不得覆盖 Source Lock、输出模式、执行模式、平台规格、素材来源记录或内容事实。

### 3B-4. 创意微资产字段（可选）

当启用 `Creative Micro Assets Routing`，尤其是 ASCII / monospace、手绘图解、Excalidraw 草图源、p5.js / generative canvas、PixiJS canvas、DESIGN.md/token note 或局部创意视觉元素时输出：

- creative_micro_assets.enabled
- creative_micro_assets.trigger
- creative_micro_assets.asset_plan[]
- creative_micro_assets.medium
- creative_micro_assets.target_output_family
- creative_micro_assets.rendering_route
- creative_micro_assets.text_policy
- creative_micro_assets.asset_source_policy
- creative_micro_assets.anti_copy_boundary
- creative_micro_assets.quality_checks

每个 `asset_plan[]` 条目至少包含：

- id
- medium
- page_or_card
- purpose
- source_anchor
- rendering_route
- text_policy
- export_boundary

创意微资产字段不得覆盖 Source Lock、输出模式、执行模式、平台规格、素材来源记录、内容事实或精确文字边界。外部 creative skill / 仓库只能作为方法参考，不复制模板、代码、素材、CSS、配色或视觉签名。

### 3B-1. PixiJS 生图增强字段

当启用 `pixijs_generated_visual_layer`，尤其是用 AI 无文字背景 + PixiJS canvas 叠层弥补纯 HTML/CSS 工程渲染画质不足时输出：

- pixijs_generated_visual_layer.enabled
- pixijs_generated_visual_layer.trigger
- pixijs_generated_visual_layer.route
- pixijs_generated_visual_layer.target_output_family
- pixijs_generated_visual_layer.canvas_role
- pixijs_generated_visual_layer.ai_image_role
- pixijs_generated_visual_layer.text_policy
- pixijs_generated_visual_layer.asset_source_policy
- pixijs_generated_visual_layer.export_plan
- pixijs_generated_visual_layer.quality_checks
- pixijs_generated_visual_layer.anti_copy_boundary

PixiJS 生图增强字段不得覆盖 Source Lock、输出模式、执行模式、平台规格、素材来源记录、内容事实或精确文字边界。PixiJS 只作为浏览器 canvas 视觉层或 HTML 预览运行时；图片交付默认是静态截图，不能声称为可编辑设计源。

### 3C. 素材来源字段（使用外部素材时必填）

当渲染包、封面背景、社交卡、文内图或设计增强使用外部图片、纹理、logo、产品图或照片时输出：

- asset_source_record[]
- background_asset_plan
- attribution_plan
- license_risk_notes

无法确认来源、许可证或商用限制时，不得把素材用于正式交付；改用 CSS 纹理、抽象视觉、AI 生成无文字背景、prompt package 或请求用户补充授权素材。

### 4. 生图提示词

- 每页 / 每卡一条
- 默认附带风格锚点说明
- 默认附带反抄袭限制

### 5. 质检报告

- 通过项
- 风险项
- risk_action_blacklist_scan
- asset_source_policy_scan
- 是否建议重试
- 重试原因
- 重试策略

### 6. 工程化渲染建议

当内容字段稳定、需要批量量产时，必须追加工程化渲染建议。
