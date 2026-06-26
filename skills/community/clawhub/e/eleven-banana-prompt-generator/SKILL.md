---
name: banana-prompt-generator
description: Google Banana（Imagen系列）AI文生图提示词生成技能。用于生成高质量角色图、场景图、分镜素材图、概念图的英文Prompt，同时提供中文说明、负面提示词和参数建议。触发词：Banana提示词、Banana作图、Google图片提示词、分镜素材图提示词。
---

# Banana 提示词生成器

> 专为 Google Banana（ Imagen 系列）文生图模型设计的高质量 Prompt 工程技能。

## 触发条件

用户说"生成Banana提示词"、"帮我写Banana的prompt"、"Banana作图"、"用Banana生成图片"、"帮我写个图片提示词"时激活。

同时适用于：生成角色图、场景图、概念图、分镜素材图。

## 核心原则

**Banana（Imagen/Google AI）擅长：**
- 超高真实感与光影质感
- 文字渲染能力（招牌、Logo）
- 复杂场景还原
- 摄影级画质

**Banana弱点：**
- 动漫/二次元风格（相对弱，建议用Vidu/即梦）
- 多人画面有时特征混淆

## 提示词结构（Banana标准格式）

```
[主体] + [场景/背景] + [风格/媒介] + [光线/氛围] + [构图] + [画质修饰]
```

## 输出规范

生成后提供：
1. **英文原版 Prompt**（用于直接输入）
2. **中文说明**（便于团队审阅）
3. **负面提示词（Negative Prompt）**
4. **参数建议**（分辨率、风格标签等）

## 参考格式

见 `references/banana-prompt-template.md`
