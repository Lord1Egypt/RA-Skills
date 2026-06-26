---
name: daily-tongjian
description: >
  Daily reading of Comprehensive Mirror to Aid in Government (资治通鉴) — all 294 volumes,
  with auto-tracked progress, full lecture text, image generation, and voice narration.
  每日通读《资治通鉴》——逐卷逐讲推进，自动追踪进度，默认生成完整讲稿、配图与语音。
  Triggers / 触发词: 「资治通鉴」「通鉴」「daily tongjian」「今日通鉴」「继续读通鉴」「tongjian」
---

# 每日通鉴 Daily Tongjian

逐卷逐段通读《资治通鉴》全书294卷，从周威烈王到后周世宗，横跨1362年。

每讲包含：原文精选 → 白话/英文翻译 → 深度点评 → 下期预告。
自动追踪进度，支持配图和语音朗读。

**默认交付要求（重要）**：
- 默认不要只给“短摘要版”；应交付一篇**完整讲稿**。
- 如用户未特别要求简版，中文正文目标长度建议 **1200-2500 字**；至少要让“原文 / 翻译 / 点评”三部分都有足够展开。
- 默认按 **三步交付**：
  1. **文字成稿**（完整讲稿，先产出这个）
  2. **配图**（从本讲最有画面感的场景生成）
  3. **语音**（基于成稿正文或精炼朗读稿生成）
- **只要用户当前配置或当前任务明确包含文字 / 图片 / 语音中的任一项，就必须把对应产物全部生成出来。**
- 不要为了赶图或赶语音，把正文压缩得过短。
- 如果用户明确只要文字，才可以跳过图和语音；否则默认图文语音都要有。
- 如果用户配置了图和语音，却只产出文字，视为本讲未真正完成。

---

## 首次使用 / First Run

第一次触发时，询问用户语言偏好：

> 欢迎来到「每日通鉴」！请选择语言 / Welcome! Choose your language:
> - **中文 (zh):** 原文 + 白话翻译 + 中文点评
> - **English (en):** Original text + English translation + English commentary

用户选择后，运行：

```bash
python3 SKILL_DIR/scripts/progress.py set-lang --lang zh  # 或 en
```

其中 `SKILL_DIR` 是本skill的安装目录。进度文件保存在 `~/.openclaw/workspace/daily-tongjian/progress.json`。

---

## 生成每日讲稿 / Generating a Lecture

### Step 1: 查看进度

```bash
python3 SKILL_DIR/scripts/progress.py status
```

获取当前卷次、讲次、语言偏好。

### Step 2: 查阅结构索引

读取 `SKILL_DIR/references/structure.md`，找到当前卷对应的时代和核心内容。
这告诉你"大概要讲什么"，作为内容生成的上下文。

### Step 3: 查阅风格指南

读取 `SKILL_DIR/references/style-guide.md`，了解讲稿格式和风格要求。

### Step 4: 生成讲稿内容

根据进度和语言偏好，生成一篇讲稿。**内容由AI根据对《资治通鉴》的知识生成**，不依赖预存文本。

#### 内容生成要点

- **选取范围：** 当前卷中一个完整的叙事段落（一个事件、一场战役、一个人物弧线）
- **原文：** 精选500-1000字经典段落，保留古文原味
- **翻译：** 流畅自然，中文避免翻译腔，英文避免直译
- **点评：** 有立场、有深度、有现代联系（但不强行）
- **断点：** 在叙事的自然悬念处结束，吊起下一讲的胃口
- **正文长度：** 默认写成一篇能单独成立的“当日讲稿”，不要只写成提纲或超短导读。若是中文，通常应至少覆盖：
  - 150-300 字开场/题眼
  - 500-1000 字原文节选
  - 400-900 字白话翻译
  - 300-800 字点评与提炼
  - 50-150 字下期预告

#### 中文模式输出格式

```markdown
## 📖 每日通鉴 · 第 X 讲

**卷次：** 卷X · [纪名]
**时代：** [朝代·年号（公元纪年）]
**本讲主题：** [一句话概括]

---

### 一、原文
> [精选原文]

### 二、白话翻译
[逐段翻译]

### 三、点评
[深度评析]

### 四、下期预告
[一句话勾起好奇心]

---
📍 进度：卷 X / 294 · 第 X 讲
```

#### English Mode Output Format

```markdown
## 📖 Daily Tongjian · Lecture X

**Volume:** Vol. X · [Annals name]
**Era:** [Dynasty, reign period (~year CE/BCE)]
**Today's Topic:** [One-line hook]

---

### I. Original Text
> [Selected classical Chinese]

### II. Translation
[English translation]

### III. Commentary
[Analysis and insight]

### IV. Next Time
[Teaser]

---
📍 Progress: Vol. X / 294 · Lecture X
```

### Step 5: 生成配图（默认执行）

在正文完成后，默认继续生成配图。

**配图要求：**
- 从本讲中选一个最有画面感的场景，不要画成“人物证件照”。
- 优先画：朝堂对峙、军阵、夜行、密谋、城门、流亡、使者入营、雨夜灯火、边塞军报等。
- 风格建议：水墨风、工笔历史画、或电影分镜感。
- 避免把历史人物画成高度可识别的固定脸谱；重点是氛围、动作、空间关系。

### Step 6: 生成语音（默认执行）

在配图完成后，默认继续生成语音。

**语音要求：**
- 中文模式默认生成一版适合朗读的中文语音稿；可以比全文略压缩，但不要只剩几十字。
- 语音稿建议长度：**300-800 字**。
- 优先保留：
  - 讲题
  - 事件主线
  - 一两个关键判断
  - 下期预告
- 中文讲稿建议使用浑厚稳重、讲史感较强的声音。
- 若有条件，可把原文中的一小段单独读得更庄重，增强仪式感。

### Step 7: 完成后再更新进度

**顺序要求：** 默认先完成文字，再完成配图，再完成语音，最后再推进进度。

- 若本讲配置为 **文字 + 图 + 语音**，则三者缺一不可。
- 不允许出现“先推进进度，图和语音以后再补”的默认行为。
- 只有用户明确接受缺项版本时，才允许跳过某一项。

讲稿、配图、语音都完成后，推进进度：

```bash
python3 SKILL_DIR/scripts/progress.py advance --title "本讲标题" --next "下讲预告标题"
```

如果图或语音因技术原因失败：
- 仍可先交付已经完成的内容
- 但不要因为失败而把正文缩成短摘要
- 只有在用户明确接受时，才把这一讲视为“文字版完成”并推进进度

---

## 进度管理 / Progress Management

进度脚本位于 `SKILL_DIR/scripts/progress.py`，数据存储在 `~/.openclaw/workspace/daily-tongjian/progress.json`。

### 可用命令

| 命令 | 说明 |
|------|------|
| `status` | 查看当前进度 |
| `advance --title "..." --next "..."` | 完成当前讲，推进到下一讲 |
| `set --volume N --lecture N --title "..."` | 跳转到指定位置 |
| `reset` | 从头开始 |
| `set-lang --lang zh\|en` | 切换语言 |

### 进度 JSON 格式

```json
{
  "currentVolume": 1,
  "currentLecture": 1,
  "lectureTitle": "三家分晋",
  "nextPreview": "魏文侯用人之道",
  "language": "zh",
  "history": [
    {
      "volume": 1,
      "lecture": 1,
      "title": "...",
      "completedAt": "2025-01-01T00:00:00+00:00"
    }
  ]
}
```

---

## 投递方式 / Delivery

本skill不绑定任何特定频道或定时任务。使用者可以：

- **手动触发：** 对话中说「今日通鉴」「继续读通鉴」等
- **定时任务：** 通过cron或heartbeat定时调用
- **指定频道：** 在cron/heartbeat配置中设置目标频道

示例cron配置（仅供参考，根据实际环境调整）：

```
每天早上8点生成通鉴讲稿，发送到指定频道
```

---

## 跳过/回看 / Skip & Review

- **跳到指定卷：** `python3 progress.py set --volume 50 --lecture 1 --title "淝水之战前夜"`
- **重新开始：** `python3 progress.py reset`
- **查看历史：** `python3 progress.py status` 中的 `history` 字段

---

## 注意事项 / Notes

- 每卷通常拆分为2-4讲，视内容密度调整
- 原文选段以叙事完整性为第一原则，不机械按字数切割
- 翻译力求信达雅，中文要像中文，英文要像英文
- 点评鼓励有立场、有温度，但避免说教
- 全书294卷读完约需600-1000讲，以每日一讲计约2-3年
