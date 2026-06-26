# 🌡️ 色温完整图表与情绪关联

> 从烛光到蓝天 — 每个色温段的视觉语言与 Prompt 写法

---

## 📊 色温总表

| 色温 | Kelvin | HEX 色码 | 颜色描述 | 典型场景 |
|------|--------|---------|---------|---------|
| 1700K | 烛光 | #FF9329 | 深橙红 | 蜡烛、篝火 |
| 1850K | 高压钠灯 | #FF9417 | 橙黄 | 路灯、钠灯 |
| 2700K | 白炽灯 | #FFB26B | 暖白 | 家用灯泡、烛光 |
| 3000K | 卤素灯 | #FFC48C | 暖黄 | 汽车大灯、卤素 |
| 3200K | 石英灯 | #FFD1A4 | 暖调白 | 专业摄影灯 |
| 4000K | 中性白 | #FFE8CC | 中性偏暖 | 荧光灯、商用 |
| 5000K | 日光 | #FFF5E6 | 纯白 | 正午柔光 |
| 5500K | 标准日光 | #FFF9F0 | 标准白 | 日光平衡点 |
| 6500K | 阴天 | #F0F4FF | 冷白 | 阴天、蓝调天空 |
| 7500K | 深阴天 | #E3EDFF | 冷蓝 | 树荫下、阴影蓝 |
| 9000K | 阴蔽处 | #D4E5FF | 蓝白 | 晴天阴影处 |
| 12000K+ | 清澈蓝天 | #C4D9FF | 纯蓝 | 北方天空、阴蔽 |

---

## 🎨 关键色码速记

```
金色时刻：  #D4A574  —  日落暖色，最安全的电影感色
蓝小时刻：  #8899BB  —  黄昏冷蓝，浪漫转紧张的分界色
阴影冷色：  #4A3F6B  —  蓝紫阴影，压郁悬疑的核心色
火光/灯笼： #FF6B35  —  橙红火焰，温暖但危险
月光：      #9BB5D4  —  银蓝月光，冷淡疏离
荧光灯：    #A8D5BA  —  绿调荧光，现代都市感
屏幕光：    #6B8DD6  —  蓝白屏幕，冷调科技感
```

---

## 🌅 按时段分类

### 🔥 1700K–2700K：暖色光（Warm）

#### 1700K：烛光 / Candlelight
- **颜色：** #FF9329，深橙红
- **情绪：** 亲密、浪漫、怀旧、神秘
- **场景：** 烛光晚餐、深夜独处、回忆段落
- **Prompt：**
  ```
  candlelight, warm 1700K, deep orange glow #FF9329,
  single point source, soft shadows, intimate,
  flickering light, volumetric smoke
  ```

#### 2700K：白炽灯 / Tungsten
- **颜色：** #FFB26B，暖白
- **情绪：** 家庭感、安全、温暖、怀旧
- **场景：** 室内生活、童年回忆、日常叙事
- **Prompt：**
  ```
  tungsten light, warm 2700K, soft amber #FFB26B,
  practical lamp visible, warm interior,
  bounced light, cozy, nostalgic mood
  ```

#### 3200K：卤素/家用灯 / Indoor Lamp
- **颜色：** #FFD1A4，暖调白
- **情绪：** 日常、真实、舒适
- **Prompt：**
  ```
  indoor lamp light, 3200K warm white,
  mixed with daylight from window,
  realistic, documentary feel
  ```

---

### ☀️ 4000K–5500K：中性光（Neutral）

#### 4000K：中性白 / Neutral White
- **颜色：** #FFE8CC
- **情绪：** 平衡、客观、真实
- **场景：** 商业广告、写实叙事
- **Prompt：** `neutral white 4000K, balanced, natural`

#### 5000K：正午柔光 / Soft Midday
- **颜色：** #FFF5E6
- **情绪：** 明亮、开放、日常感
- **场景：** 日间室内、日光环境
- **Prompt：** `soft midday light, diffused daylight, even exposure`

#### 5500K：标准日光 / Daylight
- **颜色：** #FFF9F0
- **情绪：** 标准、中性、公正
- **场景：** 新闻、证件照、商业（但也=无趣）
- **注意：** 5500K 是基准，但也是最"没有性格"的色温

---

### 🌑 6500K–12000K：冷色光（Cool）

#### 6500K：阴天 / Overcast
- **颜色：** #F0F4FF，冷白带蓝
- **情绪：** 压抑、平静、沉闷
- **场景：** 阴雨天气、情绪低落、孤独
- **Prompt：**
  ```
  overcast daylight, cool 6500K, blue-white #F0F4FF,
  flat light, soft shadows, melancholic,
  diffused through clouds
  ```

#### 7500K：阴影蓝 / Shadow Blue
- **颜色：** #E3EDFF，冷蓝
- **情绪：** 紧张、悬疑、未知
- **场景：** 夜间户外、悬疑探案
- **关键：** 阴影面偏蓝是电影感的重要标志
- **Prompt：**
  ```
  shadow areas blue tone, 7500K fill light,
  cool blue shadows #4A3F6B, high contrast,
  cinematic night scene, mysterious
  ```

#### 12000K+：清澈蓝天 / Clear Blue Sky
- **颜色：** #C4D9FF，纯蓝
- **情绪：** 科幻、未来、超现实
- **场景：** 赛博朋克、科幻、外星
- **Prompt：**
  ```
  clear blue sky light, 12000K, pure blue #C4D9FF,
  cold, futuristic, sci-fi, high-tech,
  cyberpunk atmosphere
  ```

---

## 🎬 场景应用指南

### 场景 1：日出/日落（Golden Hour）
```
色温：约 3000K–4500K
颜色：#D4A574（主），橙黄暖调
情绪：浪漫、怀旧、转瞬即逝
Prompt：
golden hour sunlight, warm 3500K, golden #D4A574,
long shadow, low angle sun, rim light,
volumetric dust particles, dreamy, nostalgic
```

### 场景 2：蓝色时刻（Blue Hour）
```
色温：约 7500K–9000K
颜色：#8899BB（主），蓝紫冷调
情绪：过渡、紧张、命运转折
Prompt：
blue hour, cool 8000K, blue-grey #8899BB,
sky reflection, long exposure feel,
melancholic, transitional moment
```

### 场景 3：夜晚月光（Moonlight）
```
色温：约 6500K–9000K
颜色：#9BB5D4（月光），#4A3F6B（阴影）
情绪：冷淡、疏离、孤独
Prompt：
moonlight, cool 7500K, silver-blue #9BB5D4,
deep blue shadow #4A3F6B, high contrast,
silence, lonely, cinematic night
```

### 场景 4：火光/篝火
```
色温：约 1700K–2000K
颜色：#FF6B35（橙红火焰）
情绪：温暖但危险，故事性
Prompt：
firelight, warm 2000K, orange #FF6B35,
flickering, single source,
deep shadow, warm/cool contrast,
dangerous warmth, campfire
```

---

## 🧠 色温与情绪映射

```
极暖（1700K）— 亲密、神秘、记忆 → 烛光、篝火
暖（2700K）— 温暖、安全、怀旧 → 室内灯、家用
中性暖（3200K）— 日常、舒适、真实 → 正常生活
中性（5000K）— 客观、平衡、开放 → 日光、广告
冷（6500K）— 压抑、沉闷、孤独 → 阴天、阴影
极冷（7500K+）— 紧张、科幻、超现实 → 夜晚、赛博
```

---

## ⚠️ 实用警告

**暖光=情绪光，冷光=信息光**

- 要情感表达 → 用暖色（2700K–4000K）
- 要客观记录 → 用冷色（5500K–6500K）
- 混用是高手操作：暖主体 + 冷背景 = 戏剧张力

**蓝色阴影是电影感的秘密**

- 自然光下，阴影不是"更暗的主光色"
- 阴影是天空的反射色 → 偏蓝
- Prompt 不说 "dark shadows"，说 "cool blue shadows #4A3F6B"

**色温不等同于色调**

- 色温：光的冷暖（蓝←→黄）
- 色调：画面整体的色彩倾向（偏绿、偏紫、偏橙）
- 两者可以独立控制，是调色的两个维度

---

> **核心记忆：**
> - 1700K = 烛光 = 浪漫/神秘
> - 3200K = 室内 = 日常/怀旧
> - 5500K = 日光 = 标准/安全
> - 7500K = 阴影蓝 = 紧张/悬疑
> - 12000K = 蓝天 = 科幻/超现实