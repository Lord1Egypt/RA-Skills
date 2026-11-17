# 应用物料 · 生图提示词模板

## 写法规则（每段提示词都必须满足）

1. 显式写出主色 HEX 与色名、纸白、深灰，并声明「only these three colors」。
2. 写出留白比例硬指标（见规范模板第四节）。
3. 写出线条母题：one continuous rounded single line, uniform stroke, two solid end nodes。
4. 写出字体气质：clean grotesk sans-serif, uppercase display, generous letter-spacing；正文极少。
5. 写出材质与拍摄方式（产品图）：natural soft daylight, matte paper / canvas / enamel, no props。
6. 否定项固定：no gradients, no second accent color, no decorative patterns, no 3D, no glossy render, no stock photo people, no clutter, no lens flare。
7. 品牌名与 slogan 用英文原样写进提示词并加引号；中文品牌名另起一行声明「render Chinese text exactly」。

## 六件默认物料

把 `[BRAND]`、`[#HEX]`、`[COLOR]`、`[SLOGAN]` 替换后直接使用。

### 1. 独立站首屏 Website Hero（16:9）

```text
Minimal website hero section for "[BRAND]", 16:9. Paper-white background #FAFAF7. One large flat [COLOR] #[HEX] rectangle occupying the left 38% of the frame, edge to edge vertically. On the white side: "[BRAND]" in uppercase grotesk sans-serif, bold, generous letter-spacing, and one short line "[SLOGAN]" in small regular weight, dark grey #1A1A1A. A single continuous rounded line in #[HEX] starts from a solid dot inside the white area, curves twice, and ends at a solid dot on the color block. Whitespace at least 45% of the frame. No other elements. Only three colors: #[HEX], #FAFAF7, #1A1A1A. No gradients, no second accent color, no decorative patterns, no 3D, no glossy render, no photos, no icons, no clutter.
```

配套结构描述（交给前端）：12 栅格；色块占 col 1–5 全高；标题 col 7–11 垂直居中；slogan 在标题下 1.5 行距；线条为一个绝对定位的 SVG path，stroke-width 6，stroke-linecap round。

### 2. 社媒头像 + 封面 Avatar & Cover（1:1 与 3:1）

```text
Brand avatar for "[BRAND]", 1:1. Solid [COLOR] #[HEX] square filling the canvas. Centered: one line-drawn smiling face made of a single circle, two dots and one upward arc, drawn in paper-white #FAFAF7 with uniform rounded strokes. Nothing else. Flat, no gradients, no shadow, no texture.
```

```text
Social cover for "[BRAND]", 3:1. Paper-white #FAFAF7 background. A single continuous rounded line in [COLOR] #[HEX] travels from a solid dot at the far left, curves gently twice across the width, and ends at a solid dot at the far right. "[BRAND]" in small uppercase grotesk letters, dark grey #1A1A1A, placed lower-right with wide letter-spacing. Whitespace at least 50%. Only three colors. No gradients, no patterns, no photos, no extra graphics.
```

### 3. 名片 Business Card（正反两面，3.5:2）

```text
Two business cards for "[BRAND]" photographed flat on a matte paper surface in soft natural daylight, 3:2 photo. Front card: solid [COLOR] #[HEX] with "[BRAND]" in small uppercase paper-white grotesk letters in the lower-left corner. Back card: paper-white #FAFAF7 with one continuous rounded [COLOR] line from a dot at the top-left to a dot at the bottom-right, and a tiny dark grey #1A1A1A line of contact text at the bottom. Thick uncoated matte card stock, slight paper texture, no props, no hands, no gradients, no gloss, no second accent color.
```

### 4. 帆布袋 Tote Bag（3:4）

```text
Natural off-white cotton canvas tote bag hanging against a plain white wall, soft daylight, 3:4 product photo. Printed on the bag: one continuous rounded single line in [COLOR] #[HEX] running from a solid dot near the top to a solid dot near the bottom with two gentle curves, and "[BRAND]" in small uppercase grotesk letters at the lower edge. Print covers at most 20% of the bag; the rest is untouched canvas. Screen-print texture, matte ink. No other graphics, no gradients, no second color, no props, no people.
```

### 5. PIN 徽章 Enamel Pin（1:1）

```text
Round hard-enamel pin, 1:1 macro product photo on a paper-white #FAFAF7 surface, soft daylight. Pin face: solid [COLOR] #[HEX] enamel with a line-drawn winking face (one circle, one dot, one short dash, one upward arc) in paper-white enamel, uniform rounded strokes, thin silver metal edge. Slight matte reflection only. No gradients, no extra symbols, no text, no props.
```

### 6. 贴纸页 Sticker Sheet（3:4）

```text
Die-cut sticker sheet for "[BRAND]", 3:4, on a paper-white #FAFAF7 backing. Eight line-drawn expressions arranged in a loose grid: smile, wink, wow, thinking with a small bubble, thumbs-up inside a circle, waving hand, star eyes, sleeping with "z z". Each is one circle plus two to four strokes, uniform rounded [COLOR] #[HEX] lines, kiss-cut outlines with a thin white border. Plus one sticker of "[BRAND]" in uppercase grotesk letters. Whitespace at least 50%. Only #[HEX], #FAFAF7, #1A1A1A. No gradients, no shading, no extra decoration.
```

## 追加物料速查

| 物料 | 关键差异 |
|---|---|
| 信封 / 信纸 | 纸白为主，线条从信封口一角出发；品牌名 Micro 级字号 |
| 邮件签名 / 二维码卡 | 主色只用在一根线和一个点；二维码周围留白 ≥ 4 个模组 |
| 展会 KV（横幅） | 主色块 ≤ 40% 放一侧，标题一行，线条跨越色块与留白的边界 |
| 手机壁纸 | 主色块在底部 30%，线条从色块升起，顶部大留白 |
| T 恤 | 与帆布袋同规则；胸口一根线或一个 Emoji，不做满印 |
