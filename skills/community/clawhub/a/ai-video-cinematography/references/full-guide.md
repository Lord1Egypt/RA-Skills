# AI 视频创作完整指南

## 概述

本教程来自 Xuan 酱的 AI 视频真实感人物篇教程，提供了一套将**抽象情绪**转化为**具体视觉语言**的完整方法论。

**核心公式**: 想要某种情绪 = 对应的摄影参数 + 对应的运动轨迹

---

## 使用流程

### 步骤 1: 确定情绪目标
首先要明确你想在视频中传达什么情感/情绪。

常见情绪分类：
- 压抑/恐惧
- 孤独/渺小
- 权力/自信
- 混乱/紧张
- 内心挣扎
- 浪漫心动
- 神圣/史诗
- 精神失常
- 敌意/对峙

### 步骤 2: 选择运镜方式
根据情绪目标，从情绪表中选择对应的运镜方式。

参考 [emotion-table.md](emotion-table.md)

### 步骤 3: 组合英文提示词
将运镜词 + 速度词 + 光效词组合成完整的英文提示词。

**运镜词示例**:
- Dutch angle (德式倾斜)
- Handheld shaky cam (手持晃动)
- Dolly zoom (推拉变焦)
- Tracking shot (跟拍)
- Crane shot (摇臂)

**速度词示例**:
- Slowly, Gradually (慢)
- Fast, Rapidly (快)
- Extreme (极端)

**光效词示例**:
- Cinematic lighting (电影光效)
- Golden hour (黄金时刻)
- Lens flare (镜头炫光)

### 步骤 4: 添加皮肤质感（人物视频）
如果是人物视频，添加皮肤质感提示词：

参考 [skin-prompts.md](skin-prompts.md)

**必填项**:
- Visible pores
- Detailed skin texture

**推荐项**:
- Subsurface Scattering (SSS)
- Peach fuzz

### 步骤 5: 排除负面词
在 Negative 提示词框中添加：

```
airbrushed, smooth skin, plastic, fake skin, cartoon, doll, wax figure
```

---

## 工具适配

### 可灵 (Kling)
- 支持运镜关键词
- 推荐: Slow motion, Tracking shot, Dolly zoom

### 即梦
- 国产工具，中文友好
- 运镜支持较好

### Runway Gen-3
- 英文提示词效果最佳
- 支持 Camera movement 关键词

### Luma
- 运镜关键词支持
- 物理效果出色

### Veo3
- Google 最新视频生成
- 理解复杂运镜描述

---

## 实战示例

### 示例 1: 孤独的宇航员
```
Prompt: A lone astronaut sitting on a desolate red planet, 
extreme long shot, camera slowly pulls back, subject becomes 
a tiny dot in the vast desert, cinematic lighting, melancholy 
atmosphere, 8k

中文: 一名孤独的宇航员坐在荒凉的红色星球上，极远景，镜头缓慢拉后，
主体在广袤沙漠中变成一个小点，电影光效，忧郁氛围，8K
```

### 示例 2: 英雄登场
```
Prompt: Warrior walking toward camera, low-to-high crane shot, 
dramatic lighting, epic music, slow motion at end

中文: 战士朝镜头走来，摇臂升起，电影级光效，史诗配乐，结尾慢动作
```

### 示例 3: 浪漫相遇
```
Prompt: Two people meeting for the first time, quick pan-to-reveal, 
rack focus between characters, soft handheld, golden hour lighting, 
romantic atmosphere

中文: 两人初次相遇，快速摇镜揭示，焦点在两人间切换，
柔和手持，黄金时刻光效，浪漫氛围
```

### 示例 4: 写实人像
```
Prompt: Portrait of woman, detailed skin texture, visible pores, 
subsurface scattering, peach fuzz, rim lighting, macro photography, 
raw photo, 8k uhd

Negative: airbrushed, smooth skin, plastic, fake skin, wax figure

中文: 女性肖像，详细皮肤纹理，可见毛孔，次表面散射，
面部绒毛，轮廓光，微距摄影，原片，8K超高清
```

---

## 常见问题

### Q: 运镜词不起作用怎么办?
A: 
1. 尝试更通用的词 (tracking shot > dolly)
2. 放在提示词开头
3. 配合速度词使用

### Q: 皮肤还是像蜡像?
A: 检查负面提示词是否包含:
- smooth skin
- plastic
- airbrushed
- wax figure

添加必填项:
- Visible pores
- Detailed skin texture

### Q: 视频不够真实?
A:
1. 添加 Raw photo, Unedited
2. 添加 Film grain
3. 降低画质描述 (有时 8k 反而太假)

---

## 更多资源

- 情绪表: [references/emotion-table.md](references/emotion-table.md)
- 皮肤提示词: [references/skin-prompts.md](references/skin-prompts.md)
