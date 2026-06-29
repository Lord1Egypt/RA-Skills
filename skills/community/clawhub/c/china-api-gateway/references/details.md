# 中国AI API统一网关 - 详细内容

## 输入参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| action | string | 必须 | - | 操作：recommend/deploy/configure/test/health |
| use_case | string | 推荐时 | - | 用途：chat/embedding/image |
| budget | string | 推荐时 | free | 预算：free/low/any |
| deployment | string | 部署时 | local | 部署方式：local/vps |
| platform | string | 可选 | - | 指定平台：xiaomi/deepseek/ali/zhipu |

## 平台特性对比

| 平台 | 模型 | 额度 | 中文 | 推理 | 适合场景 |
|------|------|------|------|------|---------|
| 小米MiMo | mimo-v2.5 | 免费无限 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 日常对话、高频调用 |
| DeepSeek | deepseek-chat | 免费额度 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 复杂推理、代码、数学 |
| 阿里百炼 | qwen-turbo | 100万tokens/月 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 稳定生产环境 |
| 智谱AI | glm-4-flash | 免费额度 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 综合对话、稳定性 |
| 零一万物 | yi-lightning | 免费额度 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 英文为主场景 |

## 推荐决策树

```
预算=free AND 用途=chat AND 高频调用?
  → 是 → 推荐小米MiMo
  → 否 → 推荐DeepSeek

需要强推理能力?
  → 推荐DeepSeek-Coder/DeepSeek-math
```

## API调用示例

```bash
# 基础对话（curl）
curl http://localhost:18080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "你好"}],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:18080/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

## 网关配置示例

```yaml
providers:
  - name: xiaomi-mimo
    base_url: https://api.xiaomimimo.com/v1
    api_key: ${MIMO_API_KEY}
    models:
      - mimo-v2.5
    priority: 1
    max_rpm: 1000

routing:
  strategy: priority
  fallback: true
  timeout: 30
  retry: 2
```

## 边界条件与异常处理

| 场景 | 处理方式 |
|------|---------|
| 平台API Key无效 | 返回详细错误信息和获取指引 |
| 平台服务不可用 | 自动标记为不可用，推荐备用平台 |
| 网络连接失败 | 检查本地网络和配置，列出诊断步骤 |
| 并发请求过高 | 建议配置速率限制 |

## 正向示例

```
用户：我想找个免费的中文AI API，用于Agent对话

助手：
💡 推荐方案：

🥇 小米MiMo（推荐）
- 模型：mimo-v2.5
- 额度：免费无限（当前）
- 特点：中文优化极好、响应快、高频调用无压力
- 适合：日常对话、高频Agent调用

🥈 DeepSeek
- 模型：deepseek-chat
- 额度：免费额度
- 特点：推理能力强、代码/数学优秀
- 适合：需要复杂推理的场景
```

## 反向示例

```
用户：帮我训练一个专属的医疗问答模型
助手：抱歉，这个需求我无法支持。❌ 不支持：模型训练、Fine-tuning
ℹ️ 支持：调用已有模型进行对话/问答
```
