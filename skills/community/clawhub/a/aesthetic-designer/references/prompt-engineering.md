# AI 生图 Prompt 工程

## 结构公式

```
[主体] + [风格/流派] + [构图] + [色调/光照] + [材质/细节] + [氛围] + --参数
```

### 参数说明
- **主体**：清晰描述核心对象
- **风格/流派**：1-2个美学流派，或知名艺术家
- **构图**：镜头角度、取景、布局
- **色调/光照**：主色调、光源方向、氛围光
- **材质/细节**：质感、表面处理、纹理
- **氛围**：情绪词（dramatic / serene / chaotic / elegant）

## Midjourney 参数速查

| 参数 | 用法 | 说明 |
|------|------|------|
| `--ar 16:9` | 横屏 | 宽屏 |
| `--ar 9:16` | 竖屏 | 手机/海报 |
| `--ar 1:1` | 方形 | 头像/图标 |
| `--s 50-1000` | 风格化 | >500 = 更艺术化 |
| `--iw 1-2` | 图权重 | 参考图影响度 |
| `--v 6.1` | 版本 | 默认最新 |
| `--stylize` | s的别名 | 同上 |
| `--no` | 排除项 | `--no text watermark` |

## 流派关键词表

| 流派 | 核心词 |
|------|--------|
| 巴洛克 | Baroque painting, chiaroscuro, tenebrism, dramatic lighting, Caravaggio |
| 新艺术 | Art Nouveau, Alphonse Mucha, whiplash curves, organic frames, stained glass |
| 浮世绘 | Ukiyo-e, woodblock print, Hokusai, flat colors, bold outlines |
| 极简主义 | minimalist, white space, single color, precise geometry, Donald Judd |
| 装饰艺术 | Art Deco, geometric ornament, gold and black, stepped forms, Roaring Twenties |
| 包豪斯 | Bauhaus, primary colors, geometric abstraction, functionalist |
| 构成主义 | Constructivism, red and black, diagonal, dynamic, Rodchenko |
| 超现实主义 | surrealist, dreamlike, Salvador Dali, impossible juxtaposition |
| 赛博朋克 | cyberpunk, neon noir, Blade Runner, rain-soaked, high tech low life |
| 波普艺术 | Pop Art, Andy Warhol, screen print, Ben-Day dots, bold comic colors |
| 蒸汽波 | vaporwave, pink purple gradient, glitch, retro digital, 1990s CGI |
| 酸性图形 | acid graphics, liquid chrome, fluorescent, melting, psychedelic |
| 生物朋克 | biopunk, organic mechanical hybrid, H.R. Giger, translucent tissues |
| 侘寂 | wabi-sabi, imperfect, natural materials, patina, tranquil |
| 生态美学 | bio-organic, ecosystem design, living materials, symbiotic |

## 实例

**请求：巴洛克风格天才龙虾**

```
A majestic lobster in Baroque style, dramatic chiaroscuro lighting,
golden carapace with deep crimson highlights, diagonal dynamic pose,
one claw raised triumphantly, oil painting texture, Caravaggio-inspired,
dark background with warm amber light from above, luxurious velvety shadows --ar 16:9 --s 750 --v 6.1
```

**请求：赛博朋克龙虾**

```
A cyberpunk lobster in neon-lit rain, chrome and bioluminescent
mechanical left claw, reflections of holographic billboards on carapace,
Blade Runner aesthetic, deep blue and pink noir lighting,
high detail, volumetric fog, wet surfaces --ar 16:9 --s 600 --v 6.1
```

**请求：侘寂 × 生态美学混合**

```
Wabi-sabi meets eco-aesthetic, an old lobster resting on a rough ceramic plate,
carapace covered with delicate moss and small coral growths,
gold kintsugi repair on a broken claw, natural daylight, organic textures,
tranquil, imperfect beauty, earthy tones --ar 4:3 --s 500 --v 6.1
```
