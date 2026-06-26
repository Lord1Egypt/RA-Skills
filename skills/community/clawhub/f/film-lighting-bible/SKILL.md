---
name: film-lighting-bible
description: 影视级灯光圣经 — AI生成画面的灯光设计参考手册。触发场景：打光、光影、侧光、逆光、灯光设计、影视灯光、柔光、硬光、轮廓光、戏剧光、伦勃朗光、日出日落光、金色时刻、蓝色时刻、体积光、丁达尔效应。用于AI生图/生视频时的灯光方向、色温、阴影逻辑提示词构建。
---

# 🎬 影视级灯光圣经

> 让 AI 生成的每一帧，都拥有摄影棚级别的光影品质。

---

## ⚡ 快速查询

| 场景 | 灯光方向 | 色温 | 情绪 |
|------|---------|------|------|
| 浪漫/怀旧 | 侧逆光+金色 | 2800K–3500K | 温暖、追忆 |
| 悬疑/紧张 | 硬侧光+低角度 | 5500K–6500K | 压迫、未知 |
| 梦幻/唯美 | 柔光+轮廓光 | 5500K–7500K | 轻盈、空灵 |
| 现实/纪录 | 平光+自然 | 5000K–6000K | 真实、克制 |
| 科幻/未来 | 蓝调+边缘光 | 7000K–12000K | 冷峻、高科技 |

---

## 📐 光线方向 — 五条铁律

### 规则 1：一个主光原则
**始终只设定一个主光源。** 次级光只做补光，不能喧宾夺主。
- AI 对多光源场景理解不稳定，单一主光最容易出电影感
- 补光强度建议：主光的 1/4 至 1/2

### 规则 2：具体方向，不能模糊
用精确的角度描述，而非"侧面光"这种模糊词：

| 中文描述 | 英文 | 用途 |
|---------|------|------|
| 正侧光（90°） | hard side light, 90-degree angle | 戏剧冲突、审讯场景 |
| 侧逆光（135°） | backlight, rear backlight | 轮廓、分层、神秘感 |
| 正面 45° | 45-degree front light, bank light | 安全打光、大众脸 |
| 低角度仰光 | low-angle uplighting, chiaroscuro | 压迫感、恐怖、权力 |
| 顶光 | top light, overhead lighting | 审讯、精神压迫 |

### 规则 3：接触阴影
阴影是电影感的来源。不是消灭阴影，是**控制阴影的落点**。

- 鼻阴影落在脸颊（伦勃朗三角光）
- 眼窝阴影（眼神光缺失=死鱼眼）
- 下颌阴影（防止面部"贴纸感"）

### 规则 4：逆光与侧光优先
**背景光（逆光/侧逆光） > 正面光。**

- 逆光分离主体与背景，解决 AI 生成的"抠图感"
- 侧光制造立体感，防止扁平
- 正面光只用于信息传达场景（新闻、证件照）

### 规则 5：光物理一致
光从窗口来，影子就朝一个方向。
同一场景内：所有物件的光源方向、高度、色温必须统一。

---

## 🌡️ 色温速查表

| 色温 | 颜色代码 | 场景 | Prompt 关键词 |
|------|---------|------|-------------|
| 1700K | #FF9329 | 烛光 | candlelight, warm glow |
| 2700K | #FFB26B | 白炽灯 | tungsten, soft white |
| 3200K | #FFD1A4 | 家用灯 | indoor lamp, cozy |
| 4000K | #FFE8CC | 中性白 | neutral white |
| 5000K | #FFF5E6 | 正午柔光 | diffused daylight |
| 5500K | #FFF9F0 | 日光 | daylight, daylight balance |
| 6500K | #F0F4FF | 阴天 | overcast, cool daylight |
| 7500K | #E3EDFF | 阴影蓝 | shadow blue, sky fill |
| 12000K+ | #C4D9FF | 清澈蓝天 | clear blue sky, shade |

### 关键 HEX 色码（背下来）

```
金色时刻：  #D4A574  （日落暖色）
蓝小时刻：  #8899BB  （黄昏冷蓝）
阴影冷色：  #4A3F6B  （蓝紫色阴影）
火光/灯笼： #FF6B35  （橙红火焰）
月光：      #9BB5D4  （银蓝月光）
```

---

## 🔲 阴影逻辑

### 主光 vs 补光比例（光比）

| 光比 | 比值 | 画面感 |
|------|------|--------|
| 平调 | 1:1 | 纪录片、新闻 |
| 柔和 | 1:2 | 青春偶像、广告 |
| 电影 | 1:4 | 剧情片、叙事感 |
| 戏剧 | 1:8 | 黑色电影、悬疑 |
| 高对比 | 1:16+ | 德国表现主义、恐怖 |

**Prompt 写法：**
- 高对比：`low key lighting, high contrast, chiaroscuro`
- 柔和：`soft fill, diffused light, low ratio`

---

## ✨ 体积光与特殊效果

### 丁达尔效应（Tyndall Effect）
光线穿过介质（尘埃、烟雾、水雾）时可见的光束。

**Prompt：** `volumetric light, god rays, light beams through dust, fog illuminated, atmospheric haze, crepuscular rays`

### 边缘光/轮廓光（Rim Light）
从主体背后打过来，分离前景与背景。

**Prompt：** `rim lighting, backlight, hair light, silhouette edge light, separation light`

### 眼神光（Eye Light）
让人物眼睛有生命感的关键。

**Prompt：** `catchlight, eye reflection, specular highlight in eyes, eyes lit`

### 柔光箱效果
模拟摄影柔光箱的散射光。

**Prompt：** `softbox light, diffused light, wraparound light, feathered light`

---

## 🎯 典型场景 Prompt 模板

### 室内窗景（日景）
```
cinematic lighting, single window light from left 45°, 
hard light with shadows, warm golden hour sunlight #D4A574, 
soft fill from ceiling bounce, contact shadow on floor, 
volumetric dust particles in light beams
```

### 夜景月光
```
cinematic night scene, cool moonlight from above right,
blue shadow tone #4A3F6B, rim light on subject edge,
moonlight #9BB5D4, subtle fill from ambient city glow,
high contrast shadows, volumetric fog
```

### 烛光/火光
```
warm candlelight, firelight orange #FF6B35, 
single point light source, high contrast,
deep shadow, warm color temperature 2700K,
flickering light effect, volumetric smoke
```

### 汽车戏剧光
```
German Expressionist lighting, low angle key light,
hard side light 90°, single source right,
deep shadow half face visible, chiaroscuro,
desaturated cold tone, high contrast 1:8
```

---

## 📚 参考文件

| 文件 | 内容 |
|------|------|
| `references/lighting-terminology.md` | 中英灯光术语大全 |
| `references/color-temperature.md` | 色温完整图表与情绪关联 |

---

## 🔑 核心原则

> **光不是用来照亮主体的。光是用来雕刻主体的。**
> 
> AI 生成最大的问题之一是"扁平感"。解决方式：逆光分离 + 侧光立体 + 阴影控制。