# 电商套图：7种图片类型规格与 Prompt 模板

每种图类型均包含：视觉规格、文案规范、Prompt 模板（可编辑）。
**核心原则**：严格保持商品一致性，不得改动商品结构、颜色、比例及细节。

---

## 图1：白底主图（White Background Hero）

### 视觉规格
- **背景**：纯白（RGB 255,255,255），绝对纯净
- **商品占比**：90% 画面，居中
- **拍摄角度**：正面或轻微 45° 角
- **灯光**：干净工作室灯光，仅在商品下方有极轻微自然阴影
- **禁止**：任何环境、道具、装饰、文字水印

### 文案
- 无文字

### Prompt 模板
```
[PRODUCT_DESCRIPTION], displayed centered on pure white background (RGB 255,255,255), 
product occupies 90% of frame, front view or slight 45-degree angle, 
clean studio lighting with very subtle natural shadow underneath, 
no props, no decorations, no text, photorealistic, high detail, commercial product photography, 8K quality.
CRITICAL: keep the product EXACTLY the same — same print, same proportions, same color, do not modify any design detail.
```

### 替换变量
- `[PRODUCT_DESCRIPTION]`：如 "white loose-fit round-neck short-sleeve T-shirt with cute cartoon dog and 'CUTE' print"

---

## 图2：核心卖点图（Key Features / Icons）

### 视觉规格
- **背景**：浅色干净背景（米白/浅灰）
- **左侧**：商品完整正面外观，清晰展示（占画面 45-50%）
- **右侧**：3个现代极简线框图标，纵向排列
- **图标风格**：细线条 outline 风格，简洁现代

### 文案（英文版）
```
右上角：WHY CHOOSE US（主标题）
图标1副标题：Combed Cotton
图标2副标题：Loose & Breathable
图标3副标题：Cute Design
```

### 文案（中文版）
```
右上角：为什么选择我们
图标1副标题：精梳棉面料
图标2副标题：宽松透气
图标3副标题：萌趣设计
```

### Prompt 模板
```
Clean product feature infographic with light background. 
Left side shows complete front view of [PRODUCT_DESCRIPTION] (45% of frame). 
Right side has 3 minimalist outline icons vertically arranged representing [FEATURE1], [FEATURE2], [FEATURE3].
Balanced layout, clean typography space for labels, modern commercial design style.
CRITICAL: keep the product EXACTLY the same — same print, same proportions, same color, do not modify any design detail.
```

---

## 图3：卖点图（Single Feature Highlight）

### 视觉规格
- **背景**：温馨舒适室内卧室，适度虚化（景深处理）
- **商品呈现**：平铺于柔软床铺 OR 隐藏面部模特穿着展示
- **重点**：宽大衣摆、落肩袖型，凸显宽松版型与休闲质感
- **光线**：柔和明亮，温馨感

### 文案（英文版）
```
左上方：LOOSE FIT DESIGN（主标题）
左下方1：Unrestricted Movement
左下方2：Comfortable and Flattering
```

### 文案（中文版）
```
左上方：宽松版型设计
左下方1：活动自如无束缚
左下方2：显瘦舒适两不误
```

### Prompt 模板
```
Cozy bedroom interior, soft bokeh background. 
[PRODUCT_DESCRIPTION] laid flat on soft bed OR worn by faceless model showing oversized silhouette.
Focus on loose fit, dropped shoulders, relaxed drape.
Soft warm lighting, casual lifestyle mood.
CRITICAL: keep the product EXACTLY the same — same print, same proportions, same color, do not modify any design detail.
Text overlay space on left side.
```

---

## 图4：材质图（Material / Texture Close-up）

### 视觉规格
- **风格**：微距特写摄影
- **构图**：商品部分折叠放置画面中央
- **灯光**：侧光打入，展现面料针织纹理与手感
- **道具**：可点缀纯净棉花植物，强化材质属性
- **焦点**：柔软织物表面的纹理细节

### 文案（英文版）
```
右上方：PREMIUM COMBED COTTON（主标题）
右中：Soft and Skin-friendly
右下：Keep Dry and Breathable
```

### 文案（中文版）
```
右上方：优质精梳棉
右中：亲肤柔软不刺激
右下：干爽透气，全天舒适
```

### Prompt 模板
```
Macro photography style, [PRODUCT_DESCRIPTION] partially folded at center.
Directional side lighting highlighting knit fabric texture and softness.
Cotton plant props in background to emphasize natural material.
High clarity, sharp fabric surface texture, soft focus bokeh background.
CRITICAL: keep the product EXACTLY the same — same print, same proportions, same color, do not modify any design detail.
Commercial product photography, ultra-detailed, 8K. Text overlay space on right side.
```

---

## 图5：场景展示图（Lifestyle Scene）

### 视觉规格
- **场景**：阳光明媚的校园绿地 OR 咖啡馆木质桌面
- **氛围**：轻松惬意，景深处理
- **搭配道具**：帆布包、笔记本电脑、复古耳机等年轻生活物件
- **商品呈现**：与道具自然搭配摆放或模特穿着
- **色调**：明亮，有活力

### 文案（英文版）
```
左上方：CASUAL EVERYDAY STYLE（主标题）
左下方1：Perfect for School
左下方2：Easy to Match
```

### 文案（中文版）
```
左上方：日常减龄穿搭
左下方1：校园首选
左下方2：百搭轻松
```

### Prompt 模板
```
Sunny campus green lawn or café wooden table surface, shallow depth of field lifestyle scene.
[PRODUCT_DESCRIPTION] paired with canvas bag, laptop or vintage headphones.
Young, casual, carefree atmosphere, bright natural lighting.
Scene conveys youthful everyday styling.
CRITICAL: keep the product EXACTLY the same — same print, same proportions, same color, do not modify any design detail.
Text overlay space on left side.
```

---

## 图6：模特展示图（Model Showcase）

### 视觉规格
- **场景**：阳光充沛的户外公园
- **模特**：典型年轻中国面孔女性，面带灿烂微笑
- **穿搭**：商品（白色T恤）+ 浅蓝色牛仔短裤
- **姿态**：自信漫步，洋溢青春活力
- **焦点**：衣服是绝对视觉中心

### 文案
- 无文字

### Prompt 模板
```
Outdoor park with abundant sunlight. 
Young Chinese female model with bright smile, confidently walking.
Wearing [PRODUCT_DESCRIPTION] with light blue denim shorts.
Product is absolute visual focus, youthful and energetic mood.
CRITICAL: keep the product EXACTLY the same — same print, same proportions, same color, do not modify any design detail.
Natural lighting, commercial fashion photography style.
```

---

## 图7：多场景拼图（Multi-Scene Split）

### 视觉规格
- **构图**：左右两个等比例分镜（各 50% 宽度）
- **左侧**：居家休闲穿搭，光影柔和温馨
- **右侧**：户外出游穿搭，阳光明丽活力
- **商品**：贯穿两幅画面，保持一致性

### 文案（英文版）
```
上方居中：VERSATILE FOR ANY OCCASION（主标题）
左下方：Home Lounging
右下方：Outdoor Outings
```

### 文案（中文版）
```
上方居中：一件多穿，随心切换
左下方：居家慵懒风
右下方：出游活力风
```

### Prompt 模板（单张 split-screen，内置左右两场景）
```
Split-screen image divided by a clean white vertical line at center.
LEFT HALF: cozy warm home interior, soft diffused lighting, [PRODUCT_DESCRIPTION] in relaxed lounging setting.
RIGHT HALF: bright outdoor park, abundant natural sunlight, [PRODUCT_DESCRIPTION] in vibrant outdoor setting.
CRITICAL: keep the product EXACTLY the same in both halves — same print, same proportions, same color, do not modify any design detail.
Keep top-center and bottom corners lighter for text overlay.
Photorealistic, commercial product photography, 8K quality.
```

**拼图方式**：直接使用此单张 Prompt 生成分屏效果，无需两张區分押合。

---

## 通用品质 Prompt 词库

### 画面品质
```
photorealistic, ultra-high definition, 8K resolution, commercial photography quality, 
sharp details, professional lighting
```

### 服装类专用
```
fabric texture visible, natural drape, true-to-life colors, 
no distortion of garment structure, consistent with original product
```

### 禁用词（避免AI改变商品）
```
CRITICAL: keep the product EXACTLY the same.
Do NOT alter the clothing design, color, print pattern, proportions, or any structural detail.
Same print, same proportions, same color throughout all images.
```
