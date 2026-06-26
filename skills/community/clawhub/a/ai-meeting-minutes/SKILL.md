---
name: ai-meeting-minutes
description: AI 会议纪要生成器 - 自动整理会议录音或文字记录，生成结构化会议纪要。支持提取待办事项、决策点、关键结论，输出专业格式的会议文档。
homepage: https://github.com/openclaw/ai-meeting-minutes
metadata:
  openclaw:
    emoji: 📝
    requires:
      bins: ["node"]
---

# AI 会议纪要生成器

自动整理会议内容，生成专业会议纪要。

## 功能特点

- 🎙️ **语音转文字** - 支持会议录音转录
- 📝 **智能摘要** - 自动生成会议摘要
- ✅ **待办提取** - 自动识别并提取待办事项
- 🎯 **决策记录** - 标记会议中的关键决策
- 📄 **多格式输出** - 支持 Markdown/Word/PDF

## 使用方法

### 从文字生成纪要

```bash
node scripts/minutes.mjs --input ./meeting.txt --output ./minutes.md
```

### 从录音生成纪要

```bash
node scripts/minutes.mjs --audio ./meeting.mp3 --output ./minutes.md
```

## License

MIT
