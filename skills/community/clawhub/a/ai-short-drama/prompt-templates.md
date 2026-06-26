# 🤖 AI短剧 Prompt 模板库

> 20+ 专业Prompt模板，覆盖角色设计/场景生成/视频合成/声音克隆全流程

---

## 一、角色设计 Prompt

### 1.1 角色一致性设定（核心技巧）

> **角色一致性是AI短剧的最大难点**。以下模板帮助保持角色在不同画面中的一致性。

```
【角色卡模板】

角色名称：[名字]
基础描述：[性别]，[年龄段]，[种族]，[体型]
面部特征：[眼睛颜色/形状]，[发型/发色]，[特殊标记（痣/疤痕等）]
常驻服装：[日常穿着描述]
风格关键词：[如：semi-realistic, cinematic lighting, soft focus, Asian beauty]

AI绘图Prompt（通用）：
"A [年龄段] [性别] [种族], [发型发色], [眼睛描述], wearing [服装], [表情], [姿势], semi-realistic style, cinematic lighting, detailed face, high quality, consistent character design"

Midjourney版本：
"[角色完整描述], cinematic portrait, soft natural lighting, shallow depth of field, photorealistic, 8k --ar 9:16 --v 6 --s 250"

Stable Diffusion版本：
"[正向: 角色描述], (masterpiece, best quality, ultra-detailed:1.3), realistic, cinematic lighting, (detailed face:1.2) --Negative: (worst quality, low quality:1.4), deformed, blurry"
```

### 1.2 角色情绪变化 Prompt

```
【情绪系列Prompt】

快乐版：
"[角色卡描述], bright genuine smile, eyes sparkling with joy, warm golden hour lighting, natural and candid moment"

悲伤版：
"[角色卡描述], teary eyes, slightly downturned mouth, melancholic expression, cold blue-tinted lighting, rain drops on window"

愤怒版：
"[角色卡描述], furrowed brows, clenched jaw, intense piercing gaze, dramatic harsh lighting from below"

惊讶版：
"[角色卡描述], wide eyes, slightly open mouth, raised eyebrows, frozen in shock moment, spotlight effect"

坚定版：
"[角色卡描述], determined unwavering gaze, set jaw, slight confident smile, strong directional lighting, heroic angle"
```

---

## 二、场景生成 Prompt

### 2.1 都市场景

```
【都市甜宠场景】

豪华办公室：
"Modern luxury CEO office, floor-to-ceiling windows overlooking city skyline at sunset, mahogany desk, leather chair, warm golden light streaming in, cinematic composition, 8k --ar 16:9"

咖啡厅偶遇：
"Cozy aesthetic coffee shop, warm amber lighting, rain outside the window, two people at adjacent tables with accidental eye contact, bokeh background, romantic atmosphere, shot on 35mm lens --ar 16:9"

雨中告白：
"Heavy rain pouring at night, city street lights reflecting on wet ground, one person holding umbrella over another, emotional cinematic moment, dramatic lighting, puddle reflections --ar 9:16"
```

### 2.2 古风场景

```
【古风仙侠场景】

仙界大门：
"Magnificent celestial palace gates, swirling clouds and mist, golden light radiating from within, ethereal jade pillars carved with ancient runes, floating mountains in background, Chinese xianxia fantasy art style, epic scale --ar 16:9"

竹林对决：
"Ancient bamboo forest, two figures in traditional Chinese martial arts robes facing each other, wind blowing bamboo leaves, swords drawn, dramatic shafts of light filtering through, ink wash painting style with photorealistic detail --ar 16:9"

雪崖离别：
"Snow-covered cliff edge at twilight, lone figure in white robes standing at precipice, vast mountain range below, cherry blossom petals mixed with falling snow, melancholic beauty, Chinese fantasy art --ar 9:16"
```

### 2.3 悬疑场景

```
【悬疑推理场景】

密室：
"Dark claustrophobic room, single flickering light bulb, dusty old furniture, locked door with scratches, ominous shadows on walls, noir style, high contrast, film grain effect --ar 16:9"

监控室：
"Banks of CRT monitors showing surveillance feeds, green-tinted screens, one screen showing something that shouldn't be there, nervous operator, cold institutional lighting, 1990s aesthetic --ar 16:9"

深夜办公室：
"Empty office building at 3am, one desk lamp still on, scattered documents, coffee cup with lipstick stain, figure visible through frosted glass, unsettling atmosphere, Dutch angle --ar 16:9"
```

---

## 三、视频合成 Prompt

### 3.1 Runway/Pika 视频生成

```
【基础镜头运动】

推镜头（强调情绪）：
"Slow push-in on [角色/场景描述], camera moving forward gradually, increasing emotional intensity, cinematic 24fps"

跟镜头（行走场景）：
"Following shot tracking [角色描述] walking through [场景], steady smooth camera movement, natural motion blur"

航拍（宏大场景）：
"Aerial drone shot slowly revealing [场景描述], sweeping landscape, golden hour lighting, epic scale"

旋转镜头（对峙场景）：
"360-degree orbit shot around two figures facing each other, dramatic tension building, slow rotation, cinematic lighting"
```

### 3.2 关键帧转场 Prompt

```
【转场效果】

时间流逝：
"Time-lapse transition, sun moving across sky, shadows shifting, [场景] changing from day to night, smooth 3-second transition"

情绪转变：
"Match cut from [场景A特写] to [场景B特写], similar composition but contrasting mood, sharp transition"

空间切换：
"Whip pan transition from [地点A] to [地点B], motion blur connecting two distinct locations"
```

---

## 四、配音与声音 Prompt

### 4.1 ElevenLabs 声音克隆

```
【声音设定模板】

甜宠女主角声音：
- 年龄感：22-28岁
- 音色：清澈甜美，略带沙哑
- 语速：中等偏快，紧张时加快
- 情感：自然不做作，哭戏有层次
- ElevenLabs Prompt: "Young Chinese female, sweet and natural voice, 25 years old, slightly husky undertone, clear pronunciation, emotional range from cheerful to heartbroken"

霸总男主角声音：
- 年龄感：28-35岁
- 音色：低沉磁性，略带冷淡
- 语速：中等偏慢，强调时停顿
- 情感：克制为主，爆发时有力
- ElevenLabs Prompt: "Deep mature Chinese male voice, calm and authoritative, 32 years old, slight warmth hidden beneath cool exterior, measured pace with dramatic pauses"

旁白声音：
- 音色：中性沉稳
- 语速：中等
- 情感：客观叙述，关键时刻带情感
- ElevenLabs Prompt: "Chinese narrator, gender-neutral warm voice, storytelling quality, measured pace, can shift between neutral and emotionally engaged"
```

### 4.2 音效与配乐

```
【配乐场景匹配】

开场/钩子：紧张悬疑 BGM + 心跳音效渐强
甜宠互动：轻快钢琴/吉他 + 环境音（鸟鸣/风铃）
反转时刻：静默1秒 + 低音鼓点 + 弦乐骤起
悲伤场景：缓慢大提琴 + 雨声/钢琴单音
高潮对决：快节奏鼓点 + 电子音效 + 渐强至顶点
结尾钩子：音乐突然停止 + 一个特殊音效（门响/电话/脚步）
```

---

## 五、字幕与后期 Prompt

### 5.1 字幕样式

```
【短剧字幕规范】

位置：底部居中，距离底边15%
字体：思源黑体/苹方 Bold
大小：屏幕宽度的4-5%
描边：2px黑色描边（保证可读性）
颜色：白色为主，强调词用黄色/红色
动画：逐字显示（打字机效果）或淡入
每条字幕：最长2行，每行最多14个汉字
持续时间：正常语速每字0.3秒
```

### 5.2 封面图 Prompt

```
【短剧封面设计】

封面图Prompt：
"Chinese short drama poster, [主要角色描述], dramatic pose, [情绪], [场景背景], title text space at top, vertical composition, high contrast, cinematic poster style, trending on Douyin --ar 3:4"

九宫格封面Prompt：
"9-grid drama preview poster showing key moments from an 8-episode short drama, each grid showing a different dramatic scene, cohesive color palette, [题材] genre, Chinese short drama style, social media optimized --ar 1:1"
```

---

## 六、批量生产 Prompt 模板

### 6.1 一键生成完整分镜

```
【分镜生成 Prompt（输入剧本后使用）】

"请根据以下短剧剧本，为每一集生成完整分镜表：

剧本：[粘贴剧本]

每集分镜表格式：
| 镜头# | 时长 | 景别 | 画面描述 | AI绘图Prompt | 对白/旁白 | 配乐/音效 | 字幕 |

要求：
1. 每集8-15个镜头
2. 景别交替使用（远景/中景/近景/特写）
3. 每个画面提供可直接使用的AI绘图Prompt
4. 标注镜头运动（推/拉/摇/移/跟）
5. 配乐标注情绪关键词"
```

### 6.2 批量角色表情包

```
"基于角色卡：[角色描述]
生成以下8种表情的AI绘图Prompt，保持角色一致性：
1. 开心大笑
2. 生气怒视
3. 害羞低头
4. 哭泣落泪
5. 惊讶张嘴
6. 深情凝视
7. 坚定前望
8. 邪魅一笑

每个Prompt格式：
表情：[名称]
情绪：[描述]
Prompt：[完整Prompt]
适用场景：[剧本中的哪个镜头]"
```
