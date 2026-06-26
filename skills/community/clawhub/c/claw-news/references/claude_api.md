# Claude API 参考文档

## 基本信息

- **API Base URL**: `https://api.anthropic.com`
- **文档**: https://docs.anthropic.com

## 认证

在请求头中添加:
```
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01
```

## 联网搜索

Claude 3.5 Sonnet 支持 Web Search 工具:

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    tools=[{"type": "web_search"}],
    messages=[{
        "role": "user",
        "content": "搜索关于人工智能的最新新闻"
    }]
)
```

## 支持的模型

| 模型 | 描述 |
|------|------|
| `claude-3-5-sonnet-20241022` | 支持联网搜索 |
| `claude-3-opus-20240229` | 旗舰模型 |

## 环境变量

```bash
export ANTHROPIC_API_KEY=sk-ant-xxx
```

## 响应格式

```python
{
  "content": [
    {"type": "text", "text": "搜索结果..."}
  ]
}
```

## 注意事项

- Claude API 需要特定模型版本才支持联网
- 部分地区的 API Key 可能不支持 web_search 工具
