---
name: daily-report
description: "Daily report generator - automatically summarizes today's tasks and generates formatted daily reports. Use when user asks for daily report, work summary, or 'today report'. Supports Word export and custom templates."
---

# Daily Report Generator (每日日报生成器)

自动汇总今日任务，生成格式化日报。

## Features

- 📋 **自动汇总** - 从 memory 文件提取今日任务
- 📝 **格式化输出** - 生成结构化日报
- 📄 **Word导出** - 支持导出 .docx 格式
- ⚙️ **自定义模板** - 可配置日报模板

## Quick Start

### Generate Today's Report

```
生成今日日报
```

```
帮我写个日报
```

```
今天的日报
```

### Export to Word

```
生成日报并导出Word
```

```
导出今日日报到桌面
```

## Commands

```bash
# 生成今日日报（纯文本）
python3 {baseDir}/scripts/generate_report.py

# 生成今日日报（Markdown格式）
python3 {baseDir}/scripts/generate_report.py --format md

# 生成并导出Word文档
python3 {baseDir}/scripts/generate_report.py --format docx --output daily_report.docx

# 指定日期
python3 {baseDir}/scripts/generate_report.py --date 2026-03-17
```

## Output Format

### 默认格式

```
【日报】2026-03-17

一、今日完成
- [x] 任务1
- [x] 任务2
- [ ] 任务3 (进行中)

二、工作总结
...

三、明日计划
- 任务A
- 任务B

四、备注
...
```

### Markdown格式

```markdown
# 每日日报 - 2026年03月17日

## ✅ 今日完成
- 任务1
- 任务2

## 📊 工作总结
...

## 📅 明日计划
- [ ] 任务A
- [ ] 任务B

## 📝 备注
...
```

## Configuration

配置文件：`~/.openclaw/daily-report-config.json`

```json
{
  "template": "default",
  "output_dir": "~/Desktop",
  "include_time": true,
  "include_stats": true,
  "language": "zh-CN"
}
```

## Data Sources

日报内容来源（按优先级）：

1. **memory/YYYY-MM-DD.md** - 今日记忆文件
2. **PROJECTS.md** - 项目任务清单
3. **用户输入** - 即时提供的任务列表

## Custom Templates

模板文件：`~/.openclaw/templates/daily-report.md`

```markdown
# {{date}} 工作日报

## 今日完成
{{completed_tasks}}

## 工作内容
{{work_summary}}

## 明日计划
{{tomorrow_plan}}

## 备注
{{notes}}
```

## Example Usage

**场景1：快速生成**
```
生成今日日报
```

**场景2：导出分享**
```
生成日报导出到桌面，我要发给领导
```

**场景3：自定义内容**
```
帮我生成日报，今天完成了：1.写完效果图 2.和客户沟通 3.整理文件
```

## Notes

- 默认从 memory 文件自动提取内容
- 支持手动补充任务
- Word 导出需要安装 `python-docx`
- 模板支持自定义变量替换
