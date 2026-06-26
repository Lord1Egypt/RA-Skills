# 国内 AI 模型 Provider 配置详情

## OpenClaw 配置格式

所有配置位于 `models.providers` 下，兼容 OpenAI API 的厂商用 `"api": "openai-completions"`。

---

## DeepSeek

**推荐指数：⭐⭐⭐⭐⭐**（性价比最高）

### 可用模型
| 模型 | 上下文 | 输入价格 | 输出价格 | 特点 |
|---|---|---|---|---|
| deepseek-chat | 64K | ¥1/M | ¥2/M | 通用对话，日常首选 |
| deepseek-reasoner | 64K | ¥2/M | ¥16/M | 深度推理，R1 架构 |

### OpenClaw 配置（config.patch 格式）
```json
{
  "models": {
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "DeepSeek Chat",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 65536,
            "maxTokens": 8192
          },
          {
            "id": "deepseek-reasoner",
            "name": "DeepSeek Reasoner",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 65536,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

### API Key
- 注册：https://platform.deepseek.com
- 新用户赠送 ¥10 额度

---

## 通义千问 (Qwen)

**推荐指数：⭐⭐⭐⭐**（阿里出品，中文强）

### 可用模型
| 模型 | 上下文 | 输入价格 | 输出价格 | 特点 |
|---|---|---|---|---|
| qwen-turbo | 128K | ¥0.3/M | ¥0.6/M | 快速便宜 |
| qwen-plus | 128K | ¥0.8/M | ¥2/M | 性能均衡 |
| qwen-max | 32K | ¥20/M | ¥60/M | 最强能力 |

### OpenClaw 配置
```json
{
  "models": {
    "providers": {
      "qwen": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen-turbo",
            "name": "Qwen Turbo",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "qwen-plus",
            "name": "Qwen Plus",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "qwen-max",
            "name": "Qwen Max",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 32768,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

### API Key
- 注册：https://dashscope.aliyun.com
- 免费试用额度

---

## 智谱 GLM

**推荐指数：⭐⭐⭐⭐**（有免费模型）

### 可用模型
| 模型 | 上下文 | 输入价格 | 输出价格 | 特点 |
|---|---|---|---|---|
| glm-4-flash | 128K | 免费 | 免费 | 免费！日常够用 |
| glm-4-plus | 128K | ¥50/M | ¥50/M | 高级能力 |
| glm-4-long | 1M | ¥1/M | ¥1/M | 超长上下文 |

### OpenClaw 配置
```json
{
  "models": {
    "providers": {
      "zhipu": {
        "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
        "apiKey": "xxx.xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "glm-4-flash",
            "name": "GLM-4 Flash",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 4096
          },
          {
            "id": "glm-4-plus",
            "name": "GLM-4 Plus",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

### API Key
- 注册：https://open.bigmodel.cn
- glm-4-flash 完全免费
- Key 格式：`{id}.{secret}`

---

## Moonshot (月之暗面 / Kimi)

**推荐指数：⭐⭐⭐**（长上下文）

### 可用模型
| 模型 | 上下文 | 输入价格 | 输出价格 |
|---|---|---|---|
| moonshot-v1-8k | 8K | ¥12/M | ¥12/M |
| moonshot-v1-32k | 32K | ¥24/M | ¥24/M |
| moonshot-v1-128k | 128K | ¥60/M | ¥60/M |

### OpenClaw 配置
```json
{
  "models": {
    "providers": {
      "moonshot": {
        "baseUrl": "https://api.moonshot.cn/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "moonshot-v1-32k",
            "name": "Moonshot v1 32K",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 32768,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

### API Key
- 注册：https://platform.moonshot.cn
- 新用户赠送 ¥15

---

## 百川 (Baichuan)

### OpenClaw 配置
```json
{
  "models": {
    "providers": {
      "baichuan": {
        "baseUrl": "https://api.baichuan-ai.com/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "Baichuan3-Turbo",
            "name": "Baichuan3 Turbo",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 32768,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

- 注册：https://platform.baichuan-ai.com

---

## 零一万物 (Yi)

### OpenClaw 配置
```json
{
  "models": {
    "providers": {
      "lingyiwanwu": {
        "baseUrl": "https://api.lingyiwanwu.com/v1",
        "apiKey": "xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "yi-medium",
            "name": "Yi Medium",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 16384,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

- 注册：https://platform.lingyiwanwu.com

---

## 推荐组合方案

### 🟢 零成本方案
日常对话用智谱 glm-4-flash（免费），适合体验和轻度使用。

### 🔵 性价比方案（推荐）
- 日常对话：DeepSeek deepseek-chat（¥1-2/M）
- 深度推理：DeepSeek deepseek-reasoner（¥2-16/M）
- 月成本约 ¥10-50

### 🟣 多模型方案
- 日常对话：DeepSeek deepseek-chat
- 中文写作：通义千问 qwen-plus
- 深度推理：DeepSeek deepseek-reasoner
- 超长文本：Moonshot moonshot-v1-128k

使用 `/model provider/model` 按需切换。

---

## 切换默认模型

通过 config.patch 修改默认模型：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat"
      }
    }
  }
}
```

或修改某个 agent 的模型（需要更新 agents.list 中对应条目）。

临时切换：在 OpenClaw 中使用 `/model deepseek/deepseek-chat`。
