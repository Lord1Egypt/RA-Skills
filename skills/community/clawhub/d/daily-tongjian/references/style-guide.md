# Daily Tongjian Style Guide

## Core Tone

This is not a dry textbook. It should feel like:
- a learned storyteller in a teahouse,
- a history podcaster with literary taste,
- or a seasoned lecturer who knows the text by heart and enjoys retelling it.

The voice should be:
- **clear** (easy to follow)
- **vivid** (scene-driven, not abstract)
- **insightful** (show why it matters)
- **human** (not robotic or overly academic)

---

## Chinese Mode (zh)

### Language
- Use modern, elegant Chinese.
- Avoid stiff textbook prose.
- Avoid internet slang unless used very sparingly for effect.
- Let the commentary sound like a smart, thoughtful person talking to another thoughtful person.
- **默认写成长讲稿，不写成朋友圈摘要。** 如果用户没要求精简，正文应有完整起承转合，能单独读下来，不依赖图片或语音补信息。

### Structure

```markdown
## 📖 每日通鉴 · 第 X 讲

**卷次：** 卷X · [纪名]
**时代：** [朝代·年号（公元纪年）]
**本讲主题：** [一句话概括]

---

### 一、原文
> [Selected classical Chinese]

### 二、白话翻译
[Modern Chinese translation, paragraph by paragraph]

### 三、点评
[Why this matters, what the characters were doing, what changed]

### 四、下期预告
[One-line teaser]

---
📍 Progress: 卷 X / 294 · 第 X 讲
```

### Commentary style

A good commentary should answer:
1. **发生了什么？**
2. **为什么会这样？**
3. **关键人物在想什么？**
4. **这件事后来影响了什么？**

默认应把这四个问题在正文里真正展开，而不是一句话带过。读者看完这一讲，应该能明白事情的来龙去脉，而不只是记住一个结论。

It may also include:
- a sharp judgment of a decision
- a reflection on power, strategy, or human nature
- a subtle resonance with modern life (but not forced)

Example tone:

> 这一段最厉害的，不是兵力多寡，而是谁先看穿了对方真正害怕什么。很多历史转折点，表面看是“谁更强”，其实是“谁更懂人心”。

> 李斯这封上书，表面是替客卿说话，骨子里是在救自己。但高明之处就在于：他把个人利益说成了国家利益。这套话术，两千年来从没过时。

---

## English Mode (en)

### Language
- Write in polished, readable English.
- Avoid overly academic jargon.
- Avoid awkward literal translation from Chinese.
- The voice should feel like a good history narrator or essayist.

### Structure

```markdown
## 📖 Daily Tongjian · Lecture X

**Volume:** Vol. X · [Annals name]
**Era:** [Dynasty, reign period (~year CE/BCE)]
**Today's Topic:** [One-line hook]

---

### I. Original Text
> [Selected classical Chinese]

### II. Translation
[English translation, paragraph by paragraph]
[Annotate key names/places on first appearance]

### III. Commentary

[Why does this matter? What turned?]
[Character analysis: who chose what, and why?]
[Historical lessons: downstream consequences]
[Modern parallels: optional, only if genuinely resonant]

### IV. Next Time

[One-line teaser]

---
📍 Progress: Vol. XXX / 294 · Lecture X
```

---

## 如何选择讲次边界 / Choosing Lecture Boundaries

好的断点：
- 一个完整事件的结束（一场战役、一次政变、一个人物的起落）
- 自然的叙事悬念点（"这个决定的后果，下回分解"）
- 一卷中 2-4 讲为宜，视内容密度调整

Bad breakpoints:
- Mid-sentence or mid-event
- Arbitrary word count cutoffs
- Splitting a coherent argument across lectures

A single volume typically yields 2-4 lectures. Dense political volumes (e.g., late Han factional struggles) may need more; sparse transitional passages can be combined.

---

## 点评风格 / Commentary Style

### DO ✅

- **讲故事**：用"于是""谁知""偏偏"这类词让叙事有节奏
- **有立场**：可以说"这个决策很蠢""此人确实有远见"
- **连古通今**：但只在自然联想时才做，不要每讲都硬扯
- **提问引思**：偶尔留一个问题让读者自己想
- **人物立体化**：不要脸谱化，好人也有私心，坏人也有逻辑

### DON'T ❌

- 学术八股：避免"由此可见""综上所述"
- 道德说教：不要居高临下地教育读者
- 过度解读：不是每件事都有深刻意义
- 维基百科式罗列：不要堆砌人物关系，用叙事带出来
- 翻译腔：中文要像中文，英文要像英文

### 好的点评示例

> 李斯这封上书，表面是替客卿说话，骨子里是在救自己。但高明之处在于：他把个人利益完美包装成了国家利益。这套话术两千年来从未过时。

> Sima Guang records this exchange almost verbatim — unusual for the Mirror. He wants you to hear it yourself and draw your own conclusions. And the conclusion is uncomfortable: the emperor knew exactly what would happen, and chose it anyway.

---

## 配图建议 / Image Suggestions

When generating an accompanying image, consider:
- **场景画面**：选讲稿中最有画面感的一个瞬间
- **风格**：水墨风、工笔历史画、或电影分镜感均可
- **避免**：不要画真实历史人物的"肖像"，画场景和氛围

Prompt structure: `[Style], [Scene description from the lecture], [Mood/atmosphere], Chinese historical setting, [Era-appropriate details]`

---

## TTS 建议 / Voice Delivery Tips

- 原文部分可以用更沉稳的语调
- 点评部分可以更口语化、更有感情
- 预告部分语气上扬，制造期待感
- 建议使用与其他节目不同的声音，增强辨识度
