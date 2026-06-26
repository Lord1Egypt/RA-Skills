# MiniMax API 参考文档

## 基本信息

- **API Base URL**: `https://api.minimax.chat/v1`
- **文档**: https://www.minimaxi.com/document

## 认证

在请求头中添加:
```
Authorization: Bearer {MINIMAX_API_KEY}
```

## 联网搜索

MiniMax M2.5 支持联网搜索:

```python
import requests

response = requests.post(
    "https://api.minimax.chat/v1/text/chatcompletion_v2",
    headers={"Authorization": f"Bearer {MINIMAX_API_KEY}"},
    json={
        "model": "MiniMax-M2.5",
        "messages": [
            {"role": "system", "content": "搜索最新新闻..."},
            {"role": "user", "content": "搜索人工智能新闻"}
        ],
        "tools": [{"type": "web_search"}]
    }
)
```

## 支持的模型

| 模型 | 描述 |
|------|------|
| `MiniMax-M2.5` | 旗舰模型，支持联网 |

## 环境变量

```bash
export MINIMAX_API_KEY=xxx
```

## 响应格式

```json
{
  "choices": [{
    "message": {
      "content": "搜索结果..."
    }
  }]
}
```
