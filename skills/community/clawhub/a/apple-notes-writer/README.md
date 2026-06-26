# Apple Notes Writer

完美格式写入Apple备忘录的OpenClaw技能。

## 快速开始

```bash
# 克隆到OpenClaw技能目录
cd ~/.openclaw/workspace/skills
git clone <repository> apple-notes-writer

# 测试运行
cd apple-notes-writer
python scripts/apple_notes.py write \
    --title "测试笔记" \
    --content "<div><h1>Hello</h1><p>World</p></div>"
```

## 功能特点

- ✅ HTML格式完美支持
- ✅ Markdown自动转换
- ✅ 特殊字符自动转义
- ✅ 多文件夹管理
- ✅ 更新或创建模式

## 文档

- [使用指南](SKILL.md) - 完整使用文档
- [基础示例](examples/example_basic.py) - 基础用法示例
- [Markdown示例](examples/example_markdown.py) - Markdown转换示例

## 系统要求

- macOS 10.14+
- Python 3.7+
- Apple Notes.app

## 许可证

MIT
