# CLI-Notion SKILL.md

**Version**: 1.0.0  
**Type**: CLI Tool  
**Interface**: Command Line + JSON  

---

## Description

CLI-Notion 是 Notion 的命令行接口，让 AI Agent 可以直接操作 Notion。

---

## Installation

设置环境变量：
```bash
export NOTION_API_KEY=your_integration_secret
```

---

## Commands

```bash
# 创建页面
python cli-notion.py create-page --parent DB_ID --title "Task"

# 列出页面
python cli-notion.py list-pages --database DB_ID

# 获取页面
python cli-notion.py get-page PAGE_ID

# 状态检查
python cli-notion.py status
```

---

## License

商业许可 - ¥68
