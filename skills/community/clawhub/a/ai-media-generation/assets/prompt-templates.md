# AI 媒体生成 — Prompt 模板库

> 可直接套用的图像/视频生成提示词模板。配合 [references/image-generation-playbook.md](../references/image-generation-playbook.md)（五段式结构）与 [references/video-generation-playbook.md](../references/video-generation-playbook.md)（视频参数）使用。

## 图像 — 文生图（SDXL/FLUX 通用五段式）

```
[主体与构图] {subject}, {pose/composition}
[细节] {detail_1}, {detail_2}
[环境] {environment}, {lighting}
[风格] {style}, {quality_anchor}
```

负面词三件套（15 词基线）：

```
worst quality, low quality, blurry, deformed, distorted, extra fingers,
bad anatomy, watermark, text, logo, jpeg artifacts
```

### 模板实例：产品宣传图

```
正面: minimalist {product} on a clean pedestal, centered composition,
soft studio lighting, gentle gradient background, premium commercial photography,
sharp focus, 8k detail
负面: worst quality, low quality, watermark, text, logo, cluttered background,
oversaturated
参数: SDXL, 1024x1024, steps 28, CFG 6, euler, seed 固定
```

### 模板实例：二次元插画

```
正面: {character} dynamic pose, detailed anime illustration,
vibrant color palette, dramatic lighting, intricate background,
high quality, detailed face
负面: worst quality, low quality, blurry, bad anatomy, deformed hands
参数: SDXL 二次元微调模型, 1024x1024, steps 25, CFG 5.5
```

## 图像 — 图生图（编辑场景）

| 场景 | 模板要点 | denoise |
|------|----------|---------|
| 局部重绘 | 原图 + mask；prompt 只描述替换区域 | 0.5-0.8 |
| 扩图 | 原图 + 扩图方向；prompt 描述新增区域与风格延续 | 0.6-0.9 |
| 风格迁移 | 原图 + 目标风格描述 | 0.4-0.6 |
| 细节增强 | 原图 + "sharp focus, more detail" + tile ControlNet | 0.3-0.5 |

## 视频 — 文生视频

```
[主体] {subject} in {environment}
[动作] {motion_description}, {camera_movement}
[氛围] {mood}, {lighting}, {color_palette}
[技术] {fps_hint}, {shot_type}, {style}
```

### 模板实例：产品动态展示

```
正面: a sleek {product} rotating on a turntable, studio lighting,
white seamless background, smooth rotation, cinematic product commercial,
slow camera push-in, 8k detail
参数: 图生视频（先用文生图出产品图）; frames 32, fps 16, CFG 5, motion scale 中
```

### 模板实例：环境氛围短片

```
正面: aerial drone shot over misty mountains at sunrise, golden light,
slow forward drift, volumetric fog, cinematic color grade, photorealistic
参数: 文生视频; frames 49, fps 16, CFG 6, motion scale 低（稳定优先）
```

## 使用纪律

- 正面词**全英文**；中文只出现在注释
- 每次只动一个变量（prompt 或参数），固定 seed 对比
- 视频 prompt 的 `[动作]` 段是质量关键：写清"什么在动、怎么动"，比堆风格词有效
- 交付前按 playbook 交付清单逐条过
