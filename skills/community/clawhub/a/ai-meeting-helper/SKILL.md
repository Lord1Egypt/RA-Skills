---
name: ai-meeting-helper
version: 1.0.0
description: 会议纪要生成器 - 自动将会议录音转为结构化纪要
author: 小叮当
tags:
  - meeting
  - transcription
  - summarization
  - audio
---

# AI Meeting Helper - 会议纪要生成器

自动将会议录音转换为结构化会议纪要，包括行动项、决策点和待办事项。

## 功能

- 🎙️ **语音转文字**：使用 OpenAI Whisper API 将会议录音转为文本
- 📋 **自动总结**：使用 LLM 分析对话内容，生成结构化纪要
- ✅ **提取要点**：自动识别行动项、决策点、待办事项
- 📤 **多格式输出**：支持 Markdown、纯文本、JSON 格式
- 🔄 **批量处理**：一次处理多个会议录音文件
- 👀 **预览模式**：不实际生成文件，只显示预览
- ↩️ **撤销功能**：自动备份原始文件，可撤销操作

## 快速开始

### 1. 安装技能

```bash
clawhub install ai-meeting-helper
cd ~/.openclaw/workspace/skills/ai-meeting-helper
./install.sh
```

### 2. 配置 OpenAI API

```bash
export OPENAI_API_KEY="your-api-key"
```

### 3. 使用示例

```bash
# 单个文件处理
ai-meeting-helper process meeting_recording.mp3 --output meeting_notes.md

# 批量处理文件夹
ai-meeting-helper batch ./meetings/ --output ./notes/ --format markdown

# 预览模式（不生成文件）
ai-meeting-helper process meeting.mp3 --preview

# 启用撤销功能
ai-meeting-helper process meeting.mp3 --output notes.md --backup
```

## 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `input` | 路径 | 是 | 输入音频文件或目录 |
| `--output` | 路径 | 否 | 输出纪要文件路径（默认：当前目录） |
| `--format` | 选项 | 否 | 输出格式：markdown/text/json（默认：markdown） |
| `--model` | 字符串 | 否 | Whisper 模型：tiny/base/small/medium/large（默认：base） |
| `--llm-model` | 字符串 | 否 | 总结使用的 LLM 模型：gpt-4o/gpt-4o-mini（默认：gpt-4o-mini） |
| `--preview` | 布尔 | 否 | 预览模式，不生成文件 |
| `--backup` | 布尔 | 否 | 启用备份（原始文件保存到 .ai_meeting_backup/） |
| `--help` | 布尔 | 否 | 显示帮助信息 |

## 输出格式

### Markdown（默认）

```markdown
# 会议纪要

**日期**：2026-03-15  
**时长**：45分钟  
**参会人数**：5人

## 讨论要点

1. 讨论了Q1产品发布计划
2. 确定了市场营销策略
3. 分配了开发任务

## 行动项

- [ ] @张三：完成用户文档（3月20日前）
- [ ] @李四：设计海报素材（3月18日前）

## 决策点

- 采用A方案作为最终设计
- 预算增加10%

## 待办事项

- 下周一下午2点开会复盘
```

### JSON

```json
{
  "date": "2026-03-15",
  "duration": "45分钟",
  "participants": 5,
  "summary": "讨论了Q1产品发布计划...",
  "action_items": [
    {"assignee": "张三", "task": "完成用户文档", "due": "2026-03-20"}
  ],
  "decisions": ["采用A方案", "预算增加10%"],
  "todo": ["下周一下午2点开会复盘"]
}
```

## 技术栈

- **语音识别**：openai-whisper-api（需 OPENAI_API_KEY）
- **文本处理**：Python 标准库 + 正则
- **LLM 总结**：OpenAI GPT-4o-mini（默认）或 GPT-4o
- **文件处理**：glob, json, pathlib

## 依赖

```bash
pip install openai python-dotenv
```

## 注意事项

- 需要有效的 OpenAI API key
- 音频文件支持：MP3, WAV, M4A, FLAC, OGG
- 较大文件处理时间较长（建议 < 30 分钟音频）
- 建议使用高质量录音以提高识别准确率

## 与其他技能配合

- **audio-note-taker**：类似功能，但 ai-meeting-helper 专为会议场景优化，输出更结构化
- **wechat-formatter**：生成的纪要可直接排版发布到公众号
- **social-publisher**：纪要内容可一键分发到多平台

## License

MIT