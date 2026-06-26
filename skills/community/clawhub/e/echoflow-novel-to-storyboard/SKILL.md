---
name: echoflow-novel-to-storyboard
description: >
  将小说章节转换为电影分镜剧本。用户上传小说文本（txt/md/docx），AI 分析场景、角色、
  情绪、镜头语言，输出专业分镜脚本。Also use when the user mentions "分镜", "storyboard",
  "小说转分镜", "影视改编", "镜头脚本", or wants to convert a novel chapter into a
  cinematic shot list. No external API key required; uses the current conversation model.
---

# Novel to Storyboard | 小说分镜生成器

Transform novel chapters into professional film storyboard scripts.

---

## Input | 接收文本

Accept novel text via:
- Paste directly into chat
- Upload `.txt`, `.md`, or `.docx` file
- Screenshot via browser tool (only extracted text is used; image is not uploaded)

---

## Generation Approach | 生成方式

Analyze the novel excerpt and produce a shot-by-shot storyboard script.

For each shot include:

1. **SHOT NUMBER** + SCENE HEADING (INT./EXT. LOCATION - TIME)
2. **VISUAL** — Camera angle, movement, composition, lighting mood
3. **ACTION/DIALOGUE** — Key events (paraphrased from the novel; quote when present)
4. **AUDIO** — Sound design, music cues, dialogue
5. **EDITING** — Shot duration estimate, transition type

Guidelines:
- Each shot: 3-8 seconds of screen time
- Target 15-40 shots per chapter
- Use film industry standard format; be cinematic, not theatrical

---

## Output Format | 输出格式

```markdown
# 《书名》— 第X章 分镜脚本
**Storyboard Script**

---

## ACT I

### SHOT 001 | EXT. CITY SKYLINE - DAWN
**镜头**: Drone aerial, slow push-in
**摄影**: Wide shot, golden hour, lens flare on frame edges
**画面**: City panorama, smog layers, first light cutting through
**声音**: City hum, distant train, wind howl
**剪辑**: 6s | CUT TO

> "城市的天际线像一头沉睡的巨兽。" — 原文

---

## ACT II
...
```

---

## Shot Types | 镜头类型

| Shot | 中文 | Use |
|------|------|-----|
| ECU | 极特写 | Emotion amplified |
| CU | 特写 | Micro-expressions |
| MCU | 中特写 | Neck to crown |
| MS | 中景 | Knees up |
| WS | 全景 | Full body |
| EWS | 超全景 | Epic scale |
| OTS | 过肩 | Dialogue scenes |
| POV | 主观镜头 | Immersion |
| Tracking | 跟踪镜头 | Follow subject |
| Crane | 升降镜头 | Grand movements |

---

## Quality Standards | 质量标准

- Prioritize visually striking, emotionally intense passages for detailed storyboarding
- Dialogue scenes: use OTS shots, avoid repetitive shot/reverse-shot
- Action/chase: cut every 2-3 seconds, vary angles
- Emotional peaks: long take + close-up + visual silence

---

## Reference | 参考

- Detailed film terminology: `references/shot-glossary.md`
- Data handling: `references/privacy.md`
