# Render Engine Skeleton

这是 V2.1 新增的工程化渲染骨架，用于把 Skill 从“策略闭环”推进到“生产闭环”。

## 适合场景

- 批量单字卡
- 批量知识卡
- 公众号正式封面
- 中文文字必须准确的商业交付
- 公众号文内图的文字叠层、素材来源校验和截图导出

## 推荐流程

```text
AI 生成结构化数据
↓
HTML/CSS 模板渲染
↓
Playwright 截图
↓
输出 PNG / JPG
↓
质检
```

当纯 HTML/CSS 模板的视觉质感不足时，可以升级为：

```text
AI 生成无文字主体 / 背景
↓
PixiJS canvas 渲染粒子 / 光效 / 程序化纹理 / 抽象数据流
↓
HTML/CSS 精确文字与安全区叠层
↓
Playwright 截图
↓
输出 PNG / JPG / PDF 静态图
↓
质检
```

这条路线只解决视觉质量和可控截图问题，不改变文字边界：中文标题、数据、标签和正文仍由工程排版或后期叠字控制。

社交组图和公众号封面对优先使用单 HTML 多 frame：

```text
index.html
├── social-01-cover
├── social-02-point
├── wechat-21x9-cover
├── wechat-1x1-cover
└── wechat-cover-pair-preview
```

同一 HTML 便于检查组图一致性、封面对是否同一视觉系统，以及每个 frame 的真实尺寸。

## 目录

```text
assets/render-engine/
├── html-templates/
├── css/
└── data/

scripts/render-engine/
└── render-with-playwright.js
```

## 说明

这里提供的是轻量模板渲染骨架。使用时把 AI 生成的 JSON 数据传给渲染脚本，脚本会替换 `{{field}}` 占位符，再用 Playwright 截图导出。

如果是公众号文内插画序列，插画主体应来自 AI 生图、用户授权素材或已记录来源的图片；HTML 只承担文字层、版式层、安全区和导出流程。数据层可以拆成 `frames[]` 或按帧分别导出，`illustration_grammar` 只用于生成前约束、提示词和质检，不由 HTML 模板直接显示，也不代表 HTML/CSS 能生成插画本体。

渲染模板只负责：

- 使用已经生成或已授权的 `background_asset`。
- 放置极少量可控中文短句。
- 执行素材来源记录和截图导出。
- 作为 AI 生图之后的文字和安全区承载层。

渲染模板不负责：

- 生成插画主体。
- 用 CSS 图形冒充插画成图。
- 把 `illustration_grammar` 字段作为可见标签放进图片。
- 把 PixiJS canvas 输出承诺成可编辑设计源或可编辑 PPT 对象。

## PixiJS canvas enhancement

PixiJS 适合在工程化渲染里承担高质量浏览器视觉层：

- 粒子、光场、流体感、噪声纹理、数据流、sprite 编排、抽象场景。
- 封面、社交卡首图、文内图视觉锚点、motion study 的静态关键帧。
- 与 AI 无文字背景组合，弥补纯 HTML/CSS 模板缺乏画面质感的问题。

使用时必须声明 `pixijs_generated_visual_layer`，并遵守：

- 最终默认导出静态 PNG/JPG/PDF；HTML 预览可以保留 canvas，但图片交付不承诺动画。
- 不复制 PixiJS 官方或第三方 demo 的源码、shader、贴图、配色、构图或视觉签名。
- 关键文字、精确数据和截图标注不进入 PixiJS canvas，也不交给图像模型生成。
- Playwright 截图前检查 canvas 非空、目标尺寸正确、无遮挡、移动端缩略图可读。

## 素材来源校验

渲染数据可以包含：

```yaml
background_asset:
  asset_id: ""
  url: ""
  object_position: "center"
asset_source_record:
  - asset_id: ""
    source_type: ""
    source_url: ""
    license: ""
    commercial_use_allowed: true
    decision: "use"
```

`background_asset.asset_id` 与 `pages[].image_asset.asset_id` 必须在 `asset_source_record[]` 中有对应记录。渲染脚本会阻止缺失记录、`unknown_or_restricted` 或 `reject` 的素材进入截图流程。

HTML / CSS 模板不得硬编码来源不明的远程背景图。背景图片、纹理、截图、logo 和产品图都应从 JSON 数据层传入，并按 `references/config/asset-source-policy.md` 记录来源。

```bash
node content-visual-forge/scripts/render-engine/render-with-playwright.js \
  content-visual-forge/assets/render-engine/html-templates/character-card.html \
  content-visual-forge/.render-output/character-card.png \
  900 1200 \
  content-visual-forge/assets/render-engine/data/character-card.sample.json
```

推荐尺寸：

- `cover-card` / `wechat-inline-image`：`1200 675`
- `social-card`：`1080 1440`
- `wechat-cover-pair` 主封面：`2100 900`
- `wechat-cover-pair` 方封面：`1080 1080`
- `character-card`：`900 1200`

运行依赖声明在 `content-visual-forge/package.json`。在没有全局 Playwright 的环境中，先在该目录安装依赖。

## wechat-inline-image 插画数据合同

当 `wechat-inline-image` 使用插画语法时，数据层可额外提供：

```yaml
illustration_grammar:
  enabled: true
  intensity: scene
  scene_family: ""
  recurring_subjects: []
  scene_role: ending
  subject_focus: ""
  composition_axis: right-weighted
  camera_distance: medium
  motion_state: still
  environment_density: sparse
  palette_temperature: warm-neutral
  line_character: soft hand-drawn edges
  texture_level: paper-grain
  text_load: very_low
  prompt_style_phrase: ""
  blocked_mimicry: []
```

这组字段是给生图提示词、素材筛选和质检使用的合同字段。渲染模板不得显示这些字段；最终画面的插画主体必须来自已生成图、用户授权图或记录清楚来源的素材。
