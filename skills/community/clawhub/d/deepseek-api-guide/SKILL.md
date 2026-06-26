---
name: deepseek-api-guide
version: 1.0.24
description: DeepSeek API 完整指南 - 注册、配置、省钱技巧。适合：想用便宜 AI 的用户。
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: []
---

# DeepSeek API 完整指南

国产最强 AI，性价比之王。

## 为什么选 DeepSeek

| 对比项 | DeepSeek V3 | GPT-4o | Claude Sonnet |
|--------|-------------|--------|---------------|
| 价格（输入） | ¥0.27/百万 tokens | ¥18/百万 tokens | ¥21/百万 tokens |
| 价格（输出） | ¥1.08/百万 tokens | ¥108/百万 tokens | ¥105/百万 tokens |
| 性能 | 接近 GPT-4 | 顶级 | 顶级 |
| 中文能力 | 优秀 | 一般 | 一般 |
| 免费额度 | 每天 10 次 | 注册送 $5 | 注册送 $5 |

**结论：DeepSeek 比 GPT-4 便宜 100 倍，性能相当**

## 注册流程

### 步骤 1：注册账号

1. 访问：https://platform.deepseek.com/
2. 手机号注册（中国 +86）
3. 实名认证（身份证）

### 步骤 2：获取 API Key

1. 登录控制台
2. API Keys → 创建新 Key
3. 复制保存（只显示一次）

### 步骤 3：充值

- 最低充值：¥10
- 支付方式：支付宝/微信
- 建议：先充 ¥10 测试

## 配置方法

### OpenClaw

```yaml
# ~/.openclaw/config.yaml
model: deepseek-chat
api_key: ${DEEPSEEK_API_KEY}
base_url: https://api.deepseek.com/v1
```

### Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
```

### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'sk-xxx',
  baseURL: 'https://api.deepseek.com/v1'
});

const response = await client.chat.completions.create({
  model: 'deepseek-chat',
  messages: [{ role: 'user', content: '你好' }]
});
```

## 模型对比

### DeepSeek V3（deepseek-chat）

- **适合**：日常对话、写作、编程
- **价格**：¥0.27/¥1.08（输入/输出）
- **性能**：接近 GPT-4
- **推荐指数**：⭐⭐⭐⭐⭐

### DeepSeek R1（deepseek-reasoner）

- **适合**：复杂推理、数学、代码
- **价格**：¥1.35/¥5.4
- **性能**：推理能力强
- **推荐指数**：⭐⭐⭐⭐

## 省钱技巧

### 1. 使用免费额度

- 每天免费 10 次调用
- 适合日常简单对话

### 2. 控制上下文长度

```yaml
context:
  max_tokens: 4000  # 限制上下文
```

### 3. 批量处理

```yaml
batch:
  enabled: true
  size: 10
```

### 4. 缓存重复请求

```yaml
cache:
  enabled: true
  ttl: 3600
```

## 成本对比

**场景：每天 100 条消息，每条 1000 tokens**

| 模型 | 月成本 |
|------|--------|
| DeepSeek V3 | ¥3.24 |
| GPT-4o | ¥324 |
| Claude Sonnet | ¥378 |

**DeepSeek 比 GPT-4 省 ¥320/月**

## 常见问题

### Q: API Key 在哪里看？

A: 控制台 → API Keys，创建后复制

### Q: 免费额度用完了怎么办？

A: 第二天自动重置，或充值继续使用

### Q: 如何查看余额？

```bash
curl https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer $API_KEY"
```

### Q: 速度慢怎么办？

A: 国内访问较快，海外可能需要代理

### Q: 和 GPT-4 差多少？

A: 日常任务几乎无差，复杂任务略逊

## 需要帮助？

- DeepSeek 配置：¥99
- OpenClaw 集成：¥199
- 企业部署：¥999

联系：微信 yang1002378395 或 Telegram @yangster151

---
创建：2026-03-14
