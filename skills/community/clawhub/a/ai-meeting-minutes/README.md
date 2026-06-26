# 📝 AI 会议纪要生成器

自动整理会议内容，生成专业会议纪要。

## ✨ 功能特点

- 🎙️ **语音转文字** - 支持会议录音转录
- 📝 **智能摘要** - 自动生成会议摘要
- ✅ **待办提取** - 自动识别并提取待办事项
- 🎯 **决策记录** - 标记会议中的关键决策
- 📄 **多格式输出** - 支持 Markdown/Word/PDF

## 🚀 快速开始

### 安装

```bash
clawhub install ai-meeting-minutes
```

### 从文字生成纪要

```bash
node scripts/minutes.mjs --input ./meeting.txt --output ./minutes.md
```

### 从录音生成纪要

```bash
node scripts/minutes.mjs --audio ./meeting.mp3 --output ./minutes.md
```

## 📋 输出示例

```markdown
# 会议纪要 - 2026-03-20

## 会议信息
- **时间**: 2026-03-20 14:00-15:30
- **地点**: 会议室A
- **参会人**: 张三、李四、王五

## 会议摘要
本次会议主要讨论了...

## 关键决策
1. ✅ 确定产品方向为...
2. ✅ 下季度预算为...

## 待办事项
- [ ] 张三负责... (截止日期: 2026-03-27)
- [ ] 李四负责... (截止日期: 2026-03-30)

## 详细记录
...
```

## 🛠️ 技术架构

- **语音识别**: Whisper API
- **文本分析**: GPT API
- **输出格式**: Markdown

## 📄 许可证

MIT License
