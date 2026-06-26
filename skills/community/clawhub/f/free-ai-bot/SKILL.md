---
name: free-ai-bot
description: 🤖 Free AI Bot - 免费 AI 聚合器。整合 Ollama 本地模型 + Cloudflare Workers AI + Groq 等免费资源，智能路由+故障转移，让 AI 零成本运行。
metadata:
  {
    "openclaw": {
      "emoji": "🤖",
      "requires": { "bins": ["curl"] },
      "primaryEnv": "OLLAMA_HOST"
    }
  }
---

# Free AI Bot 🤖

免费 AI 聚合器 - 让 AI 零成本运行

## 核心理念

**免费 ≠ 廉价**
- 本地模型 + 免费 API = 零成本运行
- 智能路由 = 始终选择最优方案
- 故障转移 = 一个不行换一个

## 支持的资源

### 🏠 本地模型 (完全免费)

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| llama3.2 | 轻量快速 | 日常对话 |
| qwen2.5 | 中文优化 | 中文任务 |
| phi3.5 | 微软出品 | 推理任务 |

### ☁️ 免费云端 API

| 服务 | 免费额度 | 特点 |
|------|----------|------|
| **Cloudflare Workers AI** | 100,000 次/天 | 快速稳定 |
| **Groq** | 60次/分钟 | 推理极快 |
| **Kimi** | 暂时有限 | 中文友好 |

## 环境配置

```bash
# 本地模型（推荐）
export OLLAMA_HOST=http://localhost:11434

# Cloudflare Workers AI（可选）
export CF_ACCOUNT_ID=your_account_id
export CF_API_TOKEN=your_token

# Groq（可选）
export GROQ_API_KEY=your_key
```

## 使用方式

### 命令行调用

```bash
# 自动选择最佳免费方案
python3 {baseDir}/scripts/ask_free_ai.py "你好"

# 指定使用本地模型
python3 {baseDir}/scripts/ask_free_ai.py "你好" --provider ollama

# 指定使用云端
python3 {baseDir}/scripts/ask_free_ai.py "你好" --provider cloudflare
```

### 智能路由逻辑

```
1. 优先本地模型（最快/免费）
   ↓ 失败
2. Cloudflare Workers AI（稳定）
   ↓ 失败
3. Groq（推理快）
   ↓ 失败
4. 返回错误
```

## 故障排除

- **Ollama 未启动**: `ollama serve`
- **API 额度用完**: 检查对应服务后台
- **网络问题**: 确认能访问对应 API

## 贡献

欢迎提交 PR！一起打造最好的免费 AI 方案。

## License

MIT License - 免费开源
