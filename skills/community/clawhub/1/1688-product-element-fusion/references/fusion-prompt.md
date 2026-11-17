# 融合 Prompt 模板与变体策略

## 基础 Prompt 模板

Stage 4 生成概念图时，使用以下模板构建 ImageGen 的 prompt。

### 中文模板（内部构建用）

```
产品摄影风格概念图。

[产品]
{product_title}，{category}。
核心视觉特征：{product_visual_features}。

[融合指令]
在保留产品基本形态和功能可识别性的前提下，将以下创意元素融入产品及其场景：

色彩：将产品配色和场景色调调整为 {color_description}。色彩饱和度 {saturation_level}。
材质：产品表面处理为 {texture_description}，呈现 {texture_finish} 的光泽效果。
风格：整体视觉对齐 {style_tags} 美学。
场景：产品置于 {atmosphere_description} 的环境中。
图案：产品表面融入 {pattern_description}。
构图：采用 {composition_description}。

[品质约束]
专业产品摄影级别。真实感，自然光影。不是插画、3D 渲染或抽象画。
画面干净，产品为主体，背景服务于氛围。
```

### 英文模板（传入 ImageGen）

ImageGen 对英文 prompt 的理解通常更好，以下是推荐的英文版本：

```
Professional product photography concept.

[Product]
{product_title}, {category}.
Key visual features: {product_visual_features}.

[Fusion Direction]
While preserving the product's recognizable form and functional identity,
integrate the following creative elements into the product and its environment:

Color: Shift the product's color palette and scene tones to {color_description}.
Saturation level: {saturation_level}.
Material: Apply {texture_description} surface finish with {texture_finish} sheen.
Style: Align overall visual aesthetic with {style_tags} design language.
Setting: Place the product in {atmosphere_description} environment.
Pattern: Incorporate {pattern_description} on the product surface.
Composition: Use {composition_description}.

[Quality Constraints]
Professional product photography. Photorealistic with natural lighting.
Not an illustration, 3D render, or abstract art.
Clean composition with the product as the focal subject.
```

---

## 变体策略

生成 2-3 张变体，每张在元素权重上有所不同。

### 变体 A：忠实融合（默认必生成）

所有六维度元素均匀应用。Prompt 中六个维度的描述完整保留，不额外强调或弱化任何一个。

**适用场景**：用户没有明确偏好时的默认选择。

### 变体 B：元素强化

从六维度中选出融合方案（Stage 3）确定的核心维度（默认取置信度最高的 2 个），在 prompt 中加强描述力度，其他维度弱化或删除。

**prompt 调整**：
- 核心维度：使用 "prominently"、"emphasizing"、"striking" 等强化词
- 非核心维度：使用 "subtly"、"hint of"、"touch of" 等弱化词，或直接删除

**适用场景**：用户希望某些元素在概念图中更突出。

### 变体 C：克制融合

只应用置信度最高的 1 个维度，其他维度不融入。保留更多原始产品的视觉特征。

**prompt 调整**：
- 核心维度：正常描述
- 其他维度：全部删除
- 添加约束："Maintain the product's original visual character as much as possible"

**适用场景**：用户希望最小化改动，只探索单一元素的影响。

---

## 元素维度 → Prompt 翻译规则

### 色彩

| 元素描述 | Prompt 翻译 |
|---------|------------|
| "雾霾蓝 #7BA7BC" | "muted dusty blue (#7BA7BC)" |
| "低饱和度" | "desaturated, muted tones" |
| "类比色调" | "analogous color scheme" |
| "莫兰迪色系" | "Morandi-inspired muted palette with grey undertones" |

### 材质

| 元素描述 | Prompt 翻译 |
|---------|------------|
| "水洗棉麻质感" | "washed linen texture with soft wrinkles" |
| "磨砂金属" | "brushed matte metal finish" |
| "哑光表面" | "matte, non-reflective surface" |
| "液态玻璃" | "liquid glass effect with transparent, flowing surface" |

### 风格

| 元素描述 | Prompt 翻译 |
|---------|------------|
| "日式侘寂" | "Japanese wabi-sabi aesthetic — imperfect beauty, natural materials, restrained elegance" |
| "Y2K" | "Y2K retro-futuristic style — chrome, glossy, early 2000s digital nostalgia" |
| "新中式" | "New Chinese style — modern reinterpretation of traditional Chinese elements" |

### 氛围

| 元素描述 | Prompt 翻译 |
|---------|------------|
| "安静的午后光线" | "quiet afternoon light, soft warm tones, peaceful atmosphere" |
| "雨夜霓虹街头" | "rainy night street scene with neon reflections on wet surfaces" |

### 图案

| 元素描述 | Prompt 翻译 |
|---------|------------|
| "不规则手工扎染纹" | "irregular hand-dyed shibori pattern" |
| "银杏叶" | "ginkgo leaf motif" |
| "无显著图案" | 不添加图案相关描述 |

### 构图

| 元素描述 | Prompt 翻译 |
|---------|------------|
| "大面积留白" | "generous negative space, minimalist composition" |
| "中心对称" | "centered, symmetrical composition" |
| "浅景深虚化背景" | "shallow depth of field with bokeh background" |

---

## ImageGen 参数选择

| 品类 | 推荐 size | 理由 |
|------|----------|------|
| 服装（连衣裙、外套） | `1024x1536` | 竖版，展示全身或半身效果 |
| 家居（沙发、桌椅） | `1792x1024` | 横版，展示产品在空间中的效果 |
| 小商品（杯具、文具） | `1024x1024` | 方形，产品居中展示 |
| 配饰（包、首饰） | `1024x1280` | 略竖版，突出产品细节 |
| 场景氛围为主 | `1792x1024` | 横版，强调场景而非单品 |

---

## 微调 Prompt 规则（Stage 5）

用户提出微调需求时，按以下规则调整 prompt：

| 用户说 | 调整方式 |
|--------|---------|
| "颜色再深/浅一点" | 在 color 描述中调整明度（darker/lighter） |
| "材质感再强一些" | 在 texture 描述中添加 "more pronounced" |
| "风格再明显一点" | 将 style 描述从 "hint of" 改为 "clearly" |
| "不太像我的产品" | 减少融合元素数量，只保留核心 1-2 个维度 |
| "太普通了" | 增加元素维度，或强化变体 B 的对比度 |
| "换个场景" | 修改 atmosphere 描述，其他维度不变 |

每次微调后重新生成时，在 prompt 末尾追加：
```
Adjustment notes: {用户的微调要求翻译为英文}
```
