# 元素融合完整案例

## 案例 1：日式侘寂街拍 → 连衣裙

### Stage 1：输入

用户提供一张日本京都街拍照片：穿着素色棉麻连衣裙的女性走在石板小巷中，背景是木格窗和苔藓石墙。

### Stage 1：提取结果

```json
{
  "source": "京都石板巷中的素色连衣裙女性街拍",
  "elements": {
    "color": {
      "primary": ["亚麻白 #EDE8E0", "石灰色 #A8A09A"],
      "accent": ["苔藓绿 #6B7C5E"],
      "relationship": "类比色调，低饱和度",
      "saturation": "低"
    },
    "texture": ["水洗棉麻质感", "轻微褶皱肌理", "粗糙石面与柔软织物的对比"],
    "style": ["日式侘寂", "自然主义", "慢生活美学"],
    "atmosphere": ["安静的午后光线", "石板巷的空间纵深", "温暖但不甜腻"],
    "pattern": ["无显著图案", "面料的自然垂坠褶皱作为纹理装饰"],
    "composition": ["纵深透视，小巷引导视线", "人物居中偏左", "前景虚化"]
  },
  "confidence": {
    "color": 0.92, "texture": 0.88, "style": 0.85,
    "atmosphere": 0.82, "pattern": 0.70, "composition": 0.88
  }
}
```

### Stage 2：元素搜品

用户目标品类：连衣裙（用户指定，灵感图中人物所穿连衣裙只是元素载体）
构建 query："棉麻 素色 连衣裙 日系"
搜索1688获取候选商品列表。

### Stage 3：商品调研 + 融合方案

调研发现：候选连衣裙以棉麻/亚麻面料为主（¥50-100），素色款比印花款少见；定制印花需额外工费。
融合方案：基底选白色棉麻 A 字连衣裙（¥68）；色彩和材质为核心（面料保持棉麻，配色调至亚麻白+石灰色、苔藓绿点缀）；风格弱化为侘寂点缀；放弃图案维度（素色面料成本更低）。

### Stage 4：概念图生成

**变体 A（忠实融合）prompt**：
```
Professional product photography concept.

[Product]
White linen A-line dress, women's casual dress.
Key visual features: A-line silhouette, midi length, relaxed fit, natural linen texture.

[Fusion Direction]
While preserving the dress's recognizable A-line silhouette and relaxed fit,
integrate the following creative elements:

Color: Shift palette to muted off-white (#EDE8E0) and warm stone grey (#A8A09A),
with subtle moss green (#6B7C5E) accents. Low saturation, Morandi-inspired muted tones.
Material: Emphasize washed linen texture with soft natural wrinkles and gentle drape.
Matte, non-reflective surface.
Style: Japanese wabi-sabi aesthetic — imperfect beauty, natural materials, restrained elegance.
Setting: Quiet afternoon light in a narrow stone-paved alley with wooden lattice windows
and moss-covered stone walls. Warm but not sweet atmosphere.
Composition: Subject slightly left of center, depth perspective leading the eye.

[Quality Constraints]
Professional product photography. Photorealistic with natural lighting.
Not an illustration or abstract art. Clean composition.
```

**变体 B（元素强化：色彩+材质）prompt**：
同变体 A，但 style 和 atmosphere 弱化为 "subtle hint of wabi-sabi"，
色彩和材质描述使用 "prominently"、"striking"、"clearly visible" 强化。

**变体 C（克制融合：仅色彩）prompt**：
仅保留 color 融合指令，删除材质/风格/氛围/构图，
添加 "Maintain the dress's original visual character as much as possible"。

### Stage 5：输出

用户选择变体 A，要求"氛围再安静一点"。微调 atmosphere 描述后重新生成，保存最终版。

---

## 案例 2：赛博朋克电影截图 → 蓝牙音箱

### Stage 1：输入

用户提供一张赛博朋克风格电影截图：雨夜东京街头，霓虹灯倒映在湿润的地面上，前景是一个金属质感的设备。

### Stage 1：提取结果

```json
{
  "source": "赛博朋克电影雨夜霓虹街景",
  "elements": {
    "color": {
      "primary": ["深靛蓝 #1A1A3E", "漆黑 #0D0D0D"],
      "accent": ["霓虹粉 #FF2D7B", "电光蓝 #00D4FF", "荧光绿 #39FF14"],
      "relationship": "深色底 + 高饱和点缀色，强对比",
      "saturation": "高"
    },
    "texture": ["磨砂金属", "湿润反光表面", "雨滴在光滑材质上的流淌感"],
    "style": ["赛博朋克", "未来主义", "暗黑科技美学"],
    "atmosphere": ["雨夜霓虹的反光", "科技感冷调", "潮湿都市的疏离感"],
    "pattern": ["无显著图案", "光线折射和雨丝形成视觉纹理"],
    "composition": ["低角度仰拍", "前景设备占据画面下三分之一", "霓虹光晕营造纵深"]
  },
  "confidence": {
    "color": 0.95, "texture": 0.85, "style": 0.92,
    "atmosphere": 0.90, "pattern": 0.65, "composition": 0.82
  }
}
```

### Stage 2：元素搜品

用户目标品类：蓝牙音箱（与灵感图的电影场景无关）
构建 query："金属 蓝牙音箱 科技感"

### Stage 3：商品调研 + 融合方案

调研发现：候选音箱以铝壳/网布为主（¥60-150），带 RGB 灯效款价格明显更高。
融合方案：基底选铝壳圆柱蓝牙音箱；color 与 style 为核心（深靛蓝底+霓虹点缀、赛博朋克）；放弃独立 RGB 灯效（成本高），用湿润反光表面细节替代灯光氛围。

### Stage 4：概念图生成

**变体 A prompt**：
```
Professional product photography concept.

[Product]
Portable Bluetooth speaker, compact cylindrical design.
Key visual features: cylindrical form, aluminum body, mesh grille, LED indicator ring.

[Fusion Direction]
While preserving the speaker's cylindrical form and compact proportions,
integrate the following creative elements:

Color: Deep indigo-black base (#1A1A3E to #0D0D0D) with striking neon accents —
hot pink (#FF2D7B), electric cyan (#00D4FF), and neon green (#39FF14) LED glow effects.
High saturation contrast between dark body and vivid light accents.
Material: Brushed matte metal body with wet-look reflective surface details.
Rain droplets on smooth metallic surface suggesting moisture and urban atmosphere.
Style: Cyberpunk aesthetic — futuristic, dark tech, high-tech meets gritty urban.
Setting: Rainy night urban street, neon reflections on wet ground,
cold technological atmosphere with a sense of urban isolation.
Composition: Low-angle shot, product prominent in foreground,
neon glow creating depth and atmosphere behind.

[Quality Constraints]
Professional product photography. Photorealistic. Dramatic lighting with neon reflections.
Not an illustration. Dark, moody, cinematic quality.
```

---

## 案例 3：小红书甜品图 → 陶瓷杯

### Stage 1：输入

用户提供一张小红书风格的甜品摆拍图：粉色马卡龙堆叠在大理石托盘上，背景是模糊的花束和金色餐具。

### Stage 1：提取结果

```json
{
  "source": "小红书马卡龙甜品摆拍",
  "elements": {
    "color": {
      "primary": ["樱花粉 #F4B8C1", "奶油白 #FFF5EE"],
      "accent": ["薄荷绿 #B2DFD0", "淡金 #D4AF37"],
      "relationship": "粉色系类比色搭配，高明度低饱和",
      "saturation": "低"
    },
    "texture": ["光滑釉面（马卡龙外壳）", "大理石纹理", "金属光泽（金色餐具）"],
    "style": ["法式优雅", "少女系", "精致生活美学"],
    "atmosphere": ["甜美精致的下午茶氛围", "柔和漫射光", "轻盈通透感"],
    "pattern": ["无显著图案", "马卡龙的圆形排列和色彩渐变形成视觉节奏"],
    "composition": ["俯拍45度角", "主体居中偏下", "浅景深虚化花束背景"]
  },
  "confidence": {
    "color": 0.93, "texture": 0.87, "style": 0.88,
    "atmosphere": 0.90, "pattern": 0.68, "composition": 0.85
  }
}
```

### Stage 2：元素搜品

用户目标品类：陶瓷杯/马克杯（灵感图中的马卡龙甜品不参与搜品）
构建 query："陶瓷杯 粉色 ins风 精致"

### Stage 3：商品调研 + 融合方案

调研发现：候选马克杯以标准釉面工艺为主（¥10-40），异形杯/手绘款价格翻倍；淡金描边需二次入窑。
融合方案：基底选标准直筒釉面马克杯；核心维度 color + style + atmosphere；材质调整为陶瓷釉面（匹配品类）；淡金描边改为贴花工艺（成本可控）。

### Stage 4：概念图生成

**变体 A prompt**：
```
Professional product photography concept.

[Product]
Ceramic mug, classic cylindrical shape with handle.
Key visual features: smooth ceramic body, C-shaped handle, 350ml capacity.

[Fusion Direction]
While preserving the mug's recognizable ceramic form and handle,
integrate the following creative elements:

Color: Cherry blossom pink (#F4B8C1) body with cream white (#FFF5EE) rim and interior.
Subtle mint green (#B2DFD0) accent on the handle. Faint gold (#D4AF37) rim detail.
High brightness, low saturation, pastel palette.
Material: Smooth glossy ceramic glaze finish, reminiscent of macaron shell surface.
Subtle marble veining pattern in the glaze. Polished, reflective surface.
Style: French elegance meets delicate feminine aesthetic. Refined, luxurious yet playful.
Instagram-worthy精致生活美学.
Setting: Soft diffused lighting, delicate afternoon tea atmosphere.
Background with blurred floral bouquet and gold cutlery hints.
Light, airy, and refined ambiance.
Composition: 45-degree overhead angle, subject centered,
shallow depth of field with soft bokeh floral background.

[Quality Constraints]
Professional product photography. Photorealistic with soft, even lighting.
Pastel color grading. Clean, elegant composition. Not an illustration.
```
