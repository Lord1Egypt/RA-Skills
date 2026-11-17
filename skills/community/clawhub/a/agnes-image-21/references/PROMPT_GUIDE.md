# Agnes Image 2.1 Flash 提示词指南

## 提示词结构

高质量的图像生成提示词应包含以下要素：

```
[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求]
```

### 各要素说明

| 要素 | 作用 | 示例 |
|------|------|------|
| 主体 | 描述画面中的主要对象 | "A young woman" |
| 场景/环境 | 描述环境或背景 | "in a cozy coffee shop" |
| 风格 | 指定艺术风格 | "painterly, impressionist" |
| 光照 | 描述光线条件 | "warm afternoon sunlight" |
| 构图 | 指定拍摄角度 | "close-up portrait" |
| 质量要求 | 指定图像质量 | "high detail, professional photography" |

## 高信息密度提示词

2.1 版本特别优化了高信息密度图像的生成，提示词应强调：

### 复杂场景描述

```
A bustling futuristic marketplace with multiple levels, 
holographic advertisements floating in the air, 
diverse crowd of people in various outfits, 
neon signs and digital displays everywhere, 
cinematic wide angle, detailed and vibrant, 
high information density, rich composition
```

### 精细细节强调

```
An ancient library interior with towering bookshelves, 
thousands of books with detailed spines, 
dust particles floating in sunbeams, 
ornate architectural details, 
warm candlelight and ambient glow, 
intricate textures, masterpiece level detail
```

### 多元素构图

```
A fantasy tavern scene with multiple characters, 
each with unique outfits and expressions, 
wooden tables with food and drinks, 
warm fireplace lighting, 
hanging lanterns and candles, 
detailed background with maps and weapons, 
rich atmosphere, high detail
```

## 文生图示例

### 高信息密度场景

```
A luminous floating city above a misty canyon at sunrise, 
cinematic realism, wide angle composition, 
rich architectural details, 
soft golden light, high visual density
```

### 复杂环境

```
A cyberpunk street market at night, 
neon signs in multiple languages, 
crowds of people with diverse appearances, 
food stalls with detailed displays, 
wet pavement reflecting lights, 
rain-soaked atmosphere, cinematic lighting, 
high information density
```

## 图生图示例

### 风格转换（保留构图）

```
Transform this photo into a vibrant anime style, 
maintain the original pose and facial features, 
bright colors, cel shading, manga aesthetic, 
preserve composition and layout
```

### 背景替换（保留主体）

```
Change the background to a futuristic city at night, 
neon lights and skyscrapers, 
keep the person's face, outfit, and pose unchanged, 
cinematic lighting, cyberpunk atmosphere, 
maintain original composition
```

### 场景增强

```
Enhance this scene with magical elements, 
add floating particles and ethereal light, 
fantasy art style, dreamy atmosphere, 
maintain the original composition and subjects
```

## 多图合成示例

### 角色融合

```
Combine these two characters in a fantasy adventure scene, 
epic landscape with mountains and forests, 
dynamic action pose, cinematic lighting, 
high fantasy art style, detailed and vibrant
```

### 场景融合

```
Merge these two environments into a single cohesive scene, 
seamless transition, consistent lighting, 
wide angle composition, photorealistic style
```

## 风格关键词

### 摄影风格

- `professional photography` - 专业摄影
- `commercial photography` - 商业摄影
- `portrait photography` - 人像摄影
- `landscape photography` - 风景摄影
- `macro photography` - 微距摄影
- `street photography` - 街头摄影

### 艺术风格

- `oil painting` - 油画
- `watercolor` - 水彩
- `digital art` - 数字艺术
- `anime` - 动漫
- `manga` - 漫画
- `concept art` - 概念艺术
- `illustration` - 插画
- `impressionist` - 印象派
- `realism` - 写实主义
- `surrealism` - 超现实主义

### 光照效果

- `golden hour` - 黄金时刻
- `blue hour` - 蓝色时刻
- `soft lighting` - 柔光
- `dramatic lighting` - 戏剧性光照
- `backlit` - 逆光
- `rim light` - 轮廓光
- `volumetric lighting` - 体积光
- `cinematic lighting` - 电影级光照

### 构图技巧

- `close-up` - 特写
- `wide angle` - 广角
- `portrait orientation` - 竖构图
- `landscape orientation` - 横构图
- `rule of thirds` - 三分法
- `centered composition` - 中心构图
- `dynamic angle` - 动态角度
- `low angle` - 低角度
- `high angle` - 高角度

## 质量关键词

- `high detail` - 高细节
- `8K resolution` - 8K 分辨率
- `professional quality` - 专业质量
- `masterpiece` - 杰作
- `award-winning` - 获奖作品
- `sharp focus` - 锐利对焦
- `bokeh` - 散景
- `depth of field` - 景深
- `high information density` - 高信息密度
- `rich composition` - 丰富构图

## 负面提示词

某些元素可能需要排除，可以在提示词中明确说明：

- `no text` - 无文字
- `no watermark` - 无水印
- `clean background` - 干净背景
- `simple composition` - 简单构图

## 提示词优化技巧

1. **具体化**：使用具体的形容词和名词
2. **层次化**：先描述主体，再描述环境
3. **风格化**：明确指定艺术风格或摄影风格
4. **质量化**：添加质量相关的关键词
5. **参考化**：引用知名艺术家或摄影作品风格
6. **密度化**：对于复杂场景，强调信息密度和细节
