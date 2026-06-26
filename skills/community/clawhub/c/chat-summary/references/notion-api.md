# Notion API 使用指南

## 认证

```bash
API_KEY="ntn_xxx"  # 从 skills.entries.notion.apiKey 读取
```

## 创建页面

```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": { "type": "page_id", "page_id": "DRAFTS_PAGE_ID" },
    "properties": {
      "title": [{ "type": "text", "text": { "content": "页面标题" } }]
    },
    "children": [
      { "object": "block", "type": "heading_2", "heading_2": { "rich_text": [{ "type": "text", "text": { "content": "话题标题" } }] } },
      { "object": "block", "type": "paragraph", "paragraph": { "rich_text": [{ "type": "text", "text": { "content": "摘要内容" } }] } }
    ]
  }'
```

## 常用 Block 类型

| 类型 | 用途 |
|------|------|
| `heading_2` | 话题标题 |
| `paragraph` | 摘要段落 |
| `bulleted_list_item` | 要点列表 |
| `divider` | 分隔线 |

## 错误处理

- 400: 请求格式错误
- 401: API Key 无效
- 404: 父页面不存在
- 429: 频率限制
