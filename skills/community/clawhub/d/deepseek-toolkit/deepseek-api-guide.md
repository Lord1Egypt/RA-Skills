# DeepSeek API 接入指南

> 最新更新：2026-05-25 | V4 Pro 永久降价 + Reasonix 发布

## API 端点

### Chat Completions（对话补全）
```
POST https://api.deepseek.com/chat/completions
```

### FIM Completions（代码补全）
```
POST https://api.deepseek.com/beta/completions
```

### 可用模型

| 模型 ID | 名称 | 上下文窗口 | 特点 | 定价（输入/输出）|
|---------|------|-----------|------|-----------------|
| `deepseek-chat` | DeepSeek-V3 | 64K | 日常对话、翻译、摘要 | ¥1/¥2 per 1M tokens |
| `deepseek-reasoner` | DeepSeek-R1 | 64K | 推理任务（内置 CoT） | ¥4/¥16 per 1M tokens |
| `deepseek-v4-pro` | V4 Pro | 128K | 综合最强，编码卓越 | 降价后约 ¥2/¥8 per 1M tokens |
| `deepseek-reasonix` | Reasonix | 128K | 原生编码 Agent | 最新发布，详见官方 |

> ⚠️ 价格可能已更新，使用前请确认 https://api-docs.deepseek.com/zh-cn/quick_start/pricing

## 认证

```bash
# API Key 设置
export DEEPSEEK_API_KEY="sk-your-key-here"
```

API Key 通过 Header 传递：
```
Authorization: Bearer sk-your-key-here
```

## 代码模板

### Python（推荐）

```python
from openai import OpenAI

# DeepSeek 兼容 OpenAI SDK，只需改 base_url
client = OpenAI(
    api_key="sk-your-key-here",
    base_url="https://api.deepseek.com"
)

# 基础对话
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "解释什么是 Prompt 缓存"},
    ],
    temperature=0.7,
    max_tokens=1024,
    stream=True  # 流式输出
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Python — 带错误处理和重试

```python
import time
from openai import OpenAI, APIError, RateLimitError, APITimeoutError

client = OpenAI(
    api_key="sk-your-key-here",
    base_url="https://api.deepseek.com",
    timeout=60.0,
    max_retries=3
)

def chat_with_retry(messages, model="deepseek-chat", max_retries=3):
    """带重试的 DeepSeek API 调用"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        
        except RateLimitError:
            wait_time = 2 ** attempt  # 指数退避
            print(f"触发限流，{wait_time}秒后重试...")
            time.sleep(wait_time)
        
        except APITimeoutError:
            print(f"请求超时，重试 {attempt + 1}/{max_retries}")
            time.sleep(1)
        
        except APIError as e:
            print(f"API 错误: {e}")
            if e.status_code >= 500:
                time.sleep(2 ** attempt)
            else:
                raise
    
    raise Exception(f"重试 {max_retries} 次后仍然失败")
```

### Node.js / TypeScript

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'sk-your-key-here',
  baseURL: 'https://api.deepseek.com',
});

async function chat(messages: Array<{role: string, content: string}>) {
  const response = await client.chat.completions.create({
    model: 'deepseek-chat',
    messages,
    temperature: 0.7,
    max_tokens: 1024,
  });
  
  return response.choices[0].message.content;
}

// 流式输出
async function chatStream(messages: Array<{role: string, content: string}>) {
  const stream = await client.chat.completions.create({
    model: 'deepseek-chat',
    messages,
    stream: true,
  });

  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}
```

### Java（Spring Boot）

```java
// 使用 RestTemplate 或 WebClient
RestTemplate restTemplate = new RestTemplate();

HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);
headers.setBearerAuth("sk-your-key-here");

Map<String, Object> body = Map.of(
    "model", "deepseek-chat",
    "messages", List.of(
        Map.of("role", "system", "content", "你是助手"),
        Map.of("role", "user", "content", "你好")
    ),
    "temperature", 0.7
);

HttpEntity<Map<String, Object>> request = new HttpEntity<>(body, headers);
ResponseEntity<Map> response = restTemplate.postForEntity(
    "https://api.deepseek.com/chat/completions",
    request,
    Map.class
);
```

### curl

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-key-here" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "system", "content": "你是助手"},
      {"role": "user", "content": "你好"}
    ],
    "stream": false
  }'
```

## 关键参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `temperature` | 随机性（0-2） | 编码 0.0，创意 0.7-1.0 |
| `max_tokens` | 最大输出长度 | 按需设置，节省成本 |
| `top_p` | 核采样 | 0.9（与 temperature 二选一调） |
| `frequency_penalty` | 频率惩罚 | 0.3（减少重复） |
| `presence_penalty` | 存在惩罚 | 0.3（增加多样性） |
| `response_format` | 输出格式 | `{"type": "json_object"}` 获取 JSON |
| `stop` | 停止序列 | 自定义结束标记 |

## Prompt 缓存机制

DeepSeek 支持 **前缀缓存（Prefix Caching）**，自动缓存相同前缀的 Prompt：

```
✅ 缓存命中（前缀相同）:
请求1: [system prompt A] + [user message 1]
请求2: [system prompt A] + [user message 2]  ← system prompt A 被缓存

❌ 缓存不命中（前缀不同）:
请求1: [system prompt A] + [user message]
请求2: [system prompt B] + [user message]  ← A 和 B 不同，无缓存
```

**最佳实践：**
1. 固定 system prompt 放在最前面
2. 把变化的部分放在消息末尾
3. 长文档/知识库放在 system prompt 中（会被缓存）
4. 缓存命中的 token 按 **1折** 计费

## 限流信息

| 等级 | RPM（每分钟请求数） | TPM（每分钟 Token） |
|------|-------------------|-------------------|
| 免费额度 | 10 | 100K |
| 标准付费 | 60 | 500K |
| 高并发 | 需联系商务 | 需联系商务 |

> ⚠️ 具体限流值可能已更新，请确认官方文档

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `401 Unauthorized` | API Key 无效 | 检查 Key 格式和有效性 |
| `429 Too Many Requests` | 超出限流 | 降低请求频率，加入指数退避 |
| `500 Server Error` | 服务端问题 | 重试（最多3次） |
| `超时` | 请求太复杂 | 减少 max_tokens，或切用更快的模型 |
| 输出截断 | max_tokens 不够 | 增大 max_tokens 或分步请求 |
| 中文乱码 | 编码问题 | 确保使用 UTF-8 |

## 从 OpenAI 迁移

DeepSeek API 兼容 OpenAI 格式，迁移只需改 2 行：

```python
# Before (OpenAI)
client = OpenAI(api_key="sk-openai-key")

# After (DeepSeek)
client = OpenAI(
    api_key="sk-deepseek-key",
    base_url="https://api.deepseek.com"  # ← 只加这一行
)

# model 参数改为 DeepSeek 模型名
# "gpt-4o" → "deepseek-v4-pro"
# "gpt-4o-mini" → "deepseek-chat"
# "o1" → "deepseek-reasonix"
```
