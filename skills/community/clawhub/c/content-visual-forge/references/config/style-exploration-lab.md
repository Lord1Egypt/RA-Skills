# Style Exploration Lab

本文件把“稀有视觉风格探索”沉淀为 `content-visual-forge` 的可选实验层。它只吸收外部教程中的方法：把风格拆成视觉变量、批量组合、筛选方向和沉淀命名，不复制外部风格库原文、示例图、prompt、文件命名体系或视觉签名。

## 何时启用

满足任一条件时启用：

- 用户明确要求风格探索、批量出图、prompt 变体、视觉实验、不要常见 AI 风格、不要通用极简 / 赛博朋克 / 电影感套路。
- 用户提供一个主体，希望看看它还能进入哪些视觉系统。
- `cover-card`、`wechat-inline-image`、`social-card` 或插画语法路线需要先做多方向样张，再决定最终视觉方向。
- 质量检查发现结果滑向通用平均值、AI 模板味、风格词过旧、同质化或主体辨识度下降。

如果任务是商业正式交付、文字必须精确、平台规格已经锁死，Style Exploration Lab 只能在正式生产前生成候选方向；最终文字、标题和精确数据仍走后期排版或工程化渲染。

## 前置条件

启用前必须已经完成：

1. Source Lock。
2. Output Mode Router。
3. Execution Mode Router。
4. 平台规格、安全区和文字精确性边界。
5. 主体或主题的 `subject_identity_lock`。

Style Exploration Lab 只改变视觉语法、材质、媒介、空间、光线和构图，不补充来源中没有的事实，不改变平台尺寸，不绕过版权和素材来源策略。

## 组合模型

默认使用 `style_exploration_matrix`：

```text
subject
+ base_style_axis: 1
+ surface_or_light_axis: 0-1
+ format_or_space_axis: 0-1
+ medium_or_defect_axis: 0-1
+ identity_lock
+ anti_drift_constraints
```

每个候选方向必须包含：

- `variant_id`：稳定编号，例如 `SX-01`。
- `direction_name`：短名称，便于文件命名和复盘。
- `subject`：被探索主体，必须保持可识别。
- `base_style_axis`：主风格轴，优先使用稀有、具体、可视化的媒介 / 年代 / 亚文化 / 工艺 / 场景线索。
- `surface_or_light_axis`：材质、光色、反射、颗粒、纸感、玻璃、金属、液体、低照度、棚拍等。
- `format_or_space_axis`：广告、包装、海报、橱窗、旧杂志、游戏道具、展览墙、咖啡馆桌面、产品摄影台等。
- `medium_or_defect_axis`：胶片颗粒、热敏纸、复印、扫描、低多边形、赛璐璐边线、印刷错位、折痕等。
- `prompt_style_phrase`：可执行提示词片段。
- `negative_constraints`：避免通用现代极简、随机文字、符号脏乱、主体身份丢失、风格盖过内容。
- `selection_note`：这个方向适合发展成封面、系列、图标、产品广告、情绪图还是放弃。

## 视觉轴池

使用自建概念轴，不复制外部列表。选择时优先让风格词指向可观察图像线索：

- `material`：陶瓷、铬、纸浆、热敏纸、丝网印刷、赛璐璐、搪瓷、霓虹玻璃、磨砂塑料、旧胶片。
- `era`：昭和商业摄影、八十年代电视动画、九十年代杂志广告、早期 3D 游戏、千禧年拟物 UI、世纪中叶说明书。
- `medium`：包装纸、唱片侧标、产品目录、展览墙标、电影剧照、街头传单、玩具摄影、游戏物品栏。
- `light_space`：棚拍、背光、咖啡馆桌面、橱窗、夜间便利店、剧场布景、暗房、博物馆展柜。
- `defect`：复印噪点、印刷套色偏移、扫描纹、胶片漏光、低多边形边缘、旧纸折痕、传真热敏颗粒。
- `subculture`：民艺包装、独立唱片、复古科教片、街机说明卡、玩具收藏、手作市集、地下传单。

每次实验从 3-8 个候选开始。除非用户要求自动化长跑，不要一次生成过量候选。

## Prompt 骨架

用于 `prompt_package` 或 `direct_image_preview`：

```text
{subject}, {base_style_axis}, {surface_or_light_axis}, {format_or_space_axis}, {medium_or_defect_axis},
clear silhouette, strong subject identity, readable composition, high detail,
avoid generic modern minimalism, avoid random extra text, avoid messy symbols,
avoid losing subject identity, avoid copying any referenced artist/template/brand signature
```

中文标题、口号、数据和小字号说明默认不进入图像模型；需要文字时只写占位或留白，交给后期排版或工程化渲染。

## 输出字段

启用后输出：

```json
{
  "style_exploration_lab": {
    "enabled": true,
    "trigger": "User asked for rare style exploration or the draft became generic.",
    "subject_identity_lock": {
      "subject": "The object, article theme, character, product, or scene being explored.",
      "must_preserve": ["recognizable shape", "core mood", "source facts"],
      "must_not_add": ["unsupported claims", "unlicensed brand marks", "precise text inside image model"]
    },
    "experiment_size": 5,
    "style_exploration_matrix": [
      {
        "variant_id": "SX-01",
        "direction_name": "short memorable name",
        "base_style_axis": "rare but legible style axis",
        "surface_or_light_axis": "material or lighting cue",
        "format_or_space_axis": "layout, object world, or spatial container",
        "medium_or_defect_axis": "print/media/camera/game defect if useful",
        "prompt_style_phrase": "subject plus visual axes and identity constraints",
        "negative_constraints": ["generic modern minimalism", "random text", "messy symbols", "lost subject identity"],
        "selection_note": "continue / merge / discard and why"
      }
    ],
    "batch_policy": {
      "naming": "include variant_id and direction_name in filenames when images are generated",
      "review_fields": ["identity_retention", "visual_surprise", "series_potential", "platform_fit", "text_safety"],
      "winner_policy": "Select 1-2 directions for production; do not ship the whole experiment by default."
    },
    "anti_copy_boundary": [
      "Do not copy external style libraries, sample images, prompt prose, filenames, templates, CSS, assets, or visual signatures.",
      "Use external tutorials only as method references for variable decomposition and experimentation."
    ]
  }
}
```

## 质量门禁

候选方向必须通过：

- 主体一眼可识别。
- 风格词能落到可见材质、媒介、空间、光线、构图或缺陷。
- 不出现随机大段文字、错误中文、伪 logo、乱码和无意义符号。
- 不把旧套路词作为唯一风格锚点，例如只写高级感、电影感、赛博朋克、极简主义。
- 不复制外部教程、风格库、艺术家、品牌或模板的可识别签名。
- 对正式发布物，胜出方向必须回到平台规格、文字安全区、素材来源记录和工程化 QA。

## 自动化边界

用户明确要求持续自动化风格探索时，才可以提出批量节奏，例如每轮 3-5 个候选、保存 prompt、样张、文件名和复盘表。自动化不等于自动发布；必须先经过人工或质量门禁筛选，再进入 production_cover、social-card 或 engineering_rendering。
