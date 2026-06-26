---
name: audio-note-taker
description: 语音笔记助手：录音自动转文字并整理成结构化笔记，支持说话人识别，自动总结要点和行动项
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { "python": "3.7+", "env": ["OPENAI_API_KEY"] },
      },
  }
---

# audio-note-taker - 语音笔记助手

智能语音笔记助手——自动将录音转成结构化文字笔记。

## 适用场景

- 🎙️ **会议记录**：自动转录会议内容，提炼行动项
- 🎓 **讲座笔记**：课堂/讲座录音转文字，自动整理要点
- 📰 **采访整理**：语音采访转文字稿，快速生成报道素材
- 💼 **工作复盘**：项目复盘录音 → 结构化记录
- 📝 **日常笔记**：快速语音记录 → 文字存档

## 核心功能

- ✅ **高精度转写**：基于 OpenAI Whisper API，支持多种语言
- ✅ **结构化输出**：自动划分段落，识别关键信息
- ✅ **智能摘要**：提取核心观点、决策、待办事项
- ✅ **说话人区分**：可选说话人识别和标记
- ✅ **Markdown 格式**：输出易读、易编辑的笔记
- ✅ **多种输入**：支持音频文件或直接录音

## 快速开始

### 基础转写

```bash
audio-note-taker /path/to/recording.m4a
# 输出：recording_notes.md
```

### 指定主题和格式

```bash
audio-note-taker /path/to/meeting.mp3 \
  --title "2026-Q1 产品规划会" \
  --language zh \
  --output meeting_notes.md
```

### 启用说话人识别

```bash
audio-note-taker /path/to/interview.wav \
  --detect-speakers true \
  --output interview_transcript.md
```

### 生成深度摘要（需配置 LLM）

```bash
audio-note-taker /path/to/lecture.mp3 \
  --summarize true \
  --extract-action-items true \
  --output lecture_summary.md
```

## 参数说明

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `input` | 路径 | 必填 | 音频文件路径（支持 mp3, m4a, wav, ogg 等） |
| `--title` | 字符串 | 自动生成 | 笔记标题 |
| `--language` | 代码 | auto | 音频语言（en, zh, ja, auto 等） |
| `--output` | 路径 | `{input}_notes.md` | 输出文件路径 |
| `--detect-speakers` | 布尔 | false | 是否识别不同说话人 |
| `--summarize` | 布尔 | false | 生成摘要（需 OPENAI_API_KEY） |
| `--extract-action-items` | 布尔 | false | 提取行动项 |
| `--model` | 字符串 | whisper-1 | Whisper 模型（whisper-1） |
| `--format` | 字符串 | markdown | 输出格式（markdown, txt, json） |

## 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | ✅ |
| `OPENAI_BASE_URL` | 自定义 API 地址（可选） | ❌ |
| `NOTE_TAKER_MODEL` | 摘要模型（默认 gpt-4-turbo） | ❌ |

## 输出内容示例

```markdown
# 会议记录：2026-Q1 产品规划会
**时间**：2026-03-15 14:00-15:30  
**地点**：线上  
**参会人**：张三、李四、王五

---

## 📝 会议纪要

### 讨论要点

1. Q1 产品上线延期原因分析
2. Q2 核心功能优先级排序
3. 资源分配调整

### ✅ 决议事项

- [x] 确定 Q2 三大核心功能
- [x] 批准额外 2 名开发人力
- [x] 下周三前发布详细排期

### 📋 待办事项

| 负责人 | 任务 | 截止时间 |
|--------|------|---------|
| 张三 | 完成 PRD 文档 | 2026-03-18 |
| 李四 | 技术方案评审 | 2026-03-20 |
| 王五 | 资源配置协调 | 2026-03-17 |

---

## 📄 完整转录（可折叠）

<details>
<summary>展开查看完整对话</summary>

[14:00] 张三：大家好，我们今天...
[14:05] 李四：关于延期，我觉得...
...
</details>
```

## 与其他技能集成

- **social-publisher**：将会议纪要直接整理成公众号/小红书文章
- **summarize**：对长录音先提取关键信息，再生成摘要
- **wechat-formatter**：将会议纪要快速格式化为公众号可发内容

## 技术细节

- 使用 OpenAI Whisper API 进行语音转文字
- 可选集成 GPT 模型进行摘要和行动项提取
- 支持中英文混合识别
- 音频预处理：自动降噪、格式转换（通过 ffmpeg）
- 输出 UTF-8 编码，支持中文排版

## 安装依赖

```bash
# 系统依赖
apt install -y ffmpeg

# Python 依赖（自动安装）
pip install openai>=1.0.0
```

## 许可证

MIT
