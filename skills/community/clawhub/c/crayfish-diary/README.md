# Crayfish Diary

[中文文档](README_CN.md) | English

A WorkBuddy skill for quick diary and memo recording with automatic year/month/day directory organization.

## Features

- 📝 **Quick Recording** - Simply say "帮我记一下" to start recording
- 📁 **Auto Organization** - Automatically organizes entries by year/month/day directory structure
- 🎯 **Smart Naming** - Extracts titles from content or uses user-specified titles
- 🏷️ **Tag Support** - Add tags to categorize your diary entries
- 💾 **Markdown Format** - All diaries stored in standard Markdown format
- 📊 **Daily Summary** - Generates a README.md summary for each day's entries

## Directory Structure

```
龙虾日记/
└── YYYY/           # Year directory (e.g., 2026)
    └── MM/         # Month directory (e.g., 03)
        └── DD/     # Day directory (e.g., 11)
            ├── README.md     # Daily summary
            └── *.md          # Diary entries
```

Example:
```
龙虾日记/
└── 2026/
    └── 03/
        └── 11/
            ├── README.md
            ├── 22-00-技能开发.md
            └── 22-30-会议纪要.md
```

## Usage

### Basic Recording

```
User: 帮我记一下
Agent: 好的，请继续说，我会记录下来。说"结束记录"完成记录。
User: 今天完成了技能开发任务，创建了一个龙虾日记技能
User: 结束记录
Agent: 已记录完成！日记保存在：龙虾日记/2026/03/11/22-00-技能开发.md
```

### With Title

```
User: 帮我记一下会议纪要
Agent: 好的，请继续说，我会记录下来。说"结束记录"完成记录。
User: 今天讨论了新产品的设计方案，确定了三个核心功能
User: 结束记录
```

### Specify Workspace

```
User: 在 Claw 空间帮我记一下
Agent: 好的，请继续说，我会记录下来。说"结束记录"完成记录。
User: 我的学习笔记：今天学习了 Python 异步编程
User: 结束记录
```

## Installation

### Via Skill Center
Search for "Crayfish Diary" in WorkBuddy Skill Center and install.

### Manual Installation
Extract the skill package to `.codebuddy/skills/crayfish-diary/` directory.

## Configuration

The skill can be configured through `clawhub.json`:

```json
{
  "name": "crayfish-diary",
  "version": "1.0.0",
  "author": "italks",
  "triggers": ["帮我记一下", "结束记录"]
}
```

## Technical Details

- **Skill Name**: crayfish-diary
- **Triggers**: 
  - Start: "帮我记一下", "help me record", "start recording"
  - End: "结束记录", "end recording", "finish recording"
- **File Format**: Markdown (.md)
- **Script Language**: Python 3

## Daily Summary Format

Each day's directory includes a `README.md` with a summary:

```markdown
# 2026-03-11 日记摘要

## 记录列表

1. **22:00 技能开发**: 今天完成了技能开发任务，创建了一个龙虾日记技能...
2. **22:30 会议纪要**: 今天讨论了新产品的设计方案，确定了三个核心功能...

---
*共 2 条记录*
```

## Changelog

### v1.0.0 (2026-03-11)
- Initial release
- Basic diary recording functionality
- Automatic year/month/day directory organization
- Tag categorization support
- Daily summary generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

**italks**

## Repository

GitHub: [https://github.com/italks/crayfish-diary.git](https://github.com/italks/crayfish-diary.git)

## Support

If you encounter any issues or have suggestions, please open an issue on GitHub.
