# Kimi API 参考文档

## 基本信息

- **API Base URL**: `https://api.moonshot.cn/v1`
- **文档**: https://platform.moonshot.cn/docs

## 认证

在请求头中添加:
```
Authorization: Bearer {KIMI_API_KEY}
```

## 联网搜索

Kimi K2.5 支持内置联网搜索工具:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_KIMI_API_KEY",
    base_url="https://api.moonshot.cn/v1"
)

response = client.chat.completions.create(
    model="kimi-k2-5",
    messages=[
        {"role": "system", "content": "你是一个新闻搜索助手..."},
        {"role": "user", "content": "搜索关于人工智能的最新新闻"}
    ],
    tools=[{
        "type": "builtin_function",
        "function": {"name": "web_search"}
    }]
)
```

## 支持的模型

| 模型 | 描述 |
|------|------|
| `kimi-k2-5` | 旗舰模型，支持联网 |
| `kimi-k2` | 标准模型 |

## 环境变量

```bash
export KIMI_API_KEY=sk-xxx
```

## 响应格式

模型会返回搜索结果的自然语言描述，通常包含:
- 新闻标题
- 来源网站
- URL 链接
- 发布时间
- 内容摘要
