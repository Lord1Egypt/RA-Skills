# CLI-Notion 🔷

**让 AI Agent 直接操作 Notion**

## 快速开始

```bash
# 设置 API Key
export NOTION_API_KEY=your_api_key

# 创建页面
python cli-notion.py create-page --parent DATABASE_ID --title "New Task"

# 列出页面
python cli-notion.py list-pages --database DATABASE_ID

# 获取页面
python cli-notion.py get-page PAGE_ID

# 检查状态
python cli-notion.py status

# JSON 输出 (Agent 使用)
python cli-notion.py --json list-pages --database DATABASE_ID
```

## 功能

- ✅ 创建页面
- ✅ 列出页面
- ✅ 获取页面详情
- ✅ API 状态检查
- ✅ JSON 输出 (AI Agent 集成)

## 获取 Notion API Key

1. 访问 https://www.notion.so/my-integrations
2. 创建新的 Integration
3. 复制 Internal Integration Secret

## 价格

- 早鸟价：¥48 (前 20 名)
- 正常价：¥68
