# Social Card Schema

用于小红书 / Rednote / 社交平台 3:4 组图的结构化数据。

## 元数据

```yaml
output_mode: "social-card"
platform: "rednote" | "xiaohongshu" | "wechat-moments" | "generic"
dimensions:
  width: 1080
  height: 1440
  aspect_ratio: "3:4"
source_anchor: ""
batch_id: ""
total_pages: 0
style_family: "editorial-ink" | "swiss-grid" | "template-default"
visual_direction:
  content_type: ""
  communication_goal: ""
  reader_emotion: ""
  information_density: "low" | "medium" | "high" | "very_high"
  style_candidates:
    click_first: ""
    save_first: ""
    brand_first: ""
  recommended_style: ""
  not_recommended: []
  page_role_rhythm: []
  visual_tokens: {}
  prompt_constraints: []
  anti_pattern_scan: []
background_asset:
  asset_id: ""
  url: ""
  object_position: "center" | "top" | "bottom" | "left" | "right"
  opacity: "0.12"
  caption: ""
```

## 内容压缩阶梯输出

```yaml
content_compression:
  core_claim: ""
  viewer_promise: ""
  section_map: []
  page_hooks: []
  body_fragments: []
  visual_evidence: []
```

## 页面结构

```yaml
pages:
  - page_number: 1
    role: "cover" | "hook" | "problem" | "insight" | "method" | "evidence" | "action" | "misconception" | "checklist" | "comparison" | "screenshot" | "quote" | "flow" | "gear" | "summary" | "cta"
    hook: ""
    point: ""
    copy: ""
    visual: ""
    layout_role: "dense" | "sparse" | "hero" | "evidence" | "transition"
    image_asset:
      asset_id: ""
      source: ""
      type: "screenshot" | "photo" | "illustration" | "icon" | "none"
      object_fit: "contain" | "cover"
      object_position: "center" | "top" | "bottom" | "left" | "right"
    bottom_points: []
    
  - page_number: 2
    ...
```

## 平台规格声明

```yaml
platform_specs:
  safe_zone:
    left: 72
    right: 72
    top: 72
    bottom: 80
  file_format: "PNG"
  naming_pattern: "social-{page_number:02d}-{topic}.png"
```

## 质检字段

```yaml
quality_gate:
  density_check:
    segments: ["0-25%", "25-50%", "50-75%", "75-100%"]
    filled_segments: 0
    justified_empty_segments: 0
    under_filled_segments: 0
  text_legibility: "pass" | "risk" | "fail"
  visual_consistency: "pass" | "risk" | "fail"
  visual_direction_quality: "pass" | "risk" | "fail"
  image_source_recorded: true | false
  text_overlay_safe: true | false
```

## 素材来源记录

只要 `background_asset.url` 或 `pages[].image_asset.source` 指向外部图片、纹理、logo、产品图、截图或本地素材，都必须有对应 `asset_source_record[]`。

```yaml
asset_source_record:
  - asset_id: ""
    role: "background" | "evidence" | "logo" | "product_image" | "texture" | "screenshot"
    source_type: "generated_graphics" | "user_provided_owned" | "official_press_kit" | "public_domain_or_cc0" | "permissive_stock_license" | "cc_by_or_cc_by_sa" | "unknown_or_restricted"
    source_url: ""
    provider: ""
    creator_or_owner: ""
    license: ""
    attribution_required: true
    attribution_text: ""
    commercial_use_allowed: true
    transformation: "crop" | "color_overlay" | "blur" | "duotone" | "masked" | "none"
    checked_at: "YYYY-MM-DD"
    decision: "use" | "replace" | "request_confirmation" | "reject"
    notes: ""
```

渲染脚本会检查 `background_asset.asset_id` 与 `pages[].image_asset.asset_id` 是否存在对应记录。`unknown_or_restricted` 或 `reject` 的素材不得进入正式渲染。

## 工程化渲染字段

```yaml
render_package:
  template_html: ""
  stylesheet: ""
  frame_ids: []
  output_paths: []
  batch_render_command: ""
```

## 规则

- 每页只承载一个核心观点
- 标题控制在 12-30 个中文字符
- 正文以 2-4 个短句、短项目或一个短段落为主
- 截图页优先保证截图可读，文字随之减少
- 页码标签使用简洁的 page-label 形式，不使用 knowledge-carousel 的页码胶囊样式
- 页面角色要有变化，不要每页都套同一张卡片
- 默认包含视觉导演字段：内容类型、传播目标、读者情绪、信息密度、三套风格方向、推荐方案、页面角色节奏和反模式扫描
- 不用随机装饰圆点、贴纸、渐变团块或嵌套卡片填空
- 不在 HTML / CSS 中硬编码来源不明的远程背景图；素材 URL 必须来自数据层并绑定 `asset_source_record[]`
