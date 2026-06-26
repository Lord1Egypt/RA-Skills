---
name: free-model-finder
description: 发现、对比和配置多平台免费/低价 AI 模型。支持 OpenRouter、HuggingFace、Groq、Google AI Studio、Ollama 等平台。Use when: (1) 用户想找免费或低价模型，(2) 当前模型太贵想切换，(3) 查询某平台可用模型，(4) 自动配置最优性价比模型，(5) 监控 rate limit 并轮换模型。
tags: ["free-models", "cost-optimization", "model-switching", "openrouter", "groq", "multi-platform"]
version: 0.1.0
---

# Free Model Finder - 多平台免费模型发现与配置

## 核心功能

### 1️⃣ 模型发现
扫描多个平台的免费/低价模型：
- **OpenRouter**：免费模型聚合（`:free` 后缀）
- **HuggingFace**：免费 Inference API 额度
- **Groq**：免费高速推理（Llama、Mixtral 等）
- **Google AI Studio**：Gemini 免费额度
- **Ollama**：本地运行（完全免费）
- **其他平台**：可扩展

### 2️⃣ 模型对比
按以下维度排序：
- 价格（免费/每百万 token 成本）
- 速度（平均响应时间）
- 质量（上下文长度、能力评级）
- 稳定性（rate limit 策略）

### 3️⃣ 自动配置
- 直接修改 OpenClaw 配置文件
- 设置主模型 + 备用模型列表
- 自动重启 Gateway 生效

### 4️⃣ 监控轮换
- 检测 rate limit 错误
- 自动切换到备用模型
- 记录切换历史

## 快速开始

```bash
# 查看所有平台免费模型清单
free-model-finder list

# 只看 OpenRouter 免费模型
free-model-finder list --platform openrouter

# 自动配置最优免费模型（推荐）
free-model-finder auto

# 切换到指定模型
free-model-finder switch groq/llama-3.1-70b-versatile

# 查看当前配置
free-model-finder status

# 监控 rate limit 并自动轮换
free-model-finder watch --daemon
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `list [--platform] [--limit]` | 列出可用模型 |
| `compare [--top N]` | 对比前 N 个模型的性价比 |
| `auto [--platforms]` | 自动配置最优模型 |
| `switch <model>` | 切换到指定模型 |
| `status` | 查看当前配置 |
| `watch [--daemon]` | 监控并自动轮换 |
| `refresh` | 刷新模型缓存 |

## 平台配置

### OpenRouter
需要 API Key：https://openrouter.ai/keys
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### Groq
需要 API Key：https://console.groq.com/keys
```bash
export GROQ_API_KEY="gsk_..."
```

### Google AI Studio
需要 API Key：https://aistudio.google.com/app/apikey
```bash
export GOOGLE_API_KEY="..."
```

### HuggingFace
需要 API Key：https://huggingface.co/settings/tokens
```bash
export HF_TOKEN="..."
```

### Ollama
本地运行，无需 API Key：
```bash
# 安装后直接可用
ollama pull llama3.1
```

## 配置文件位置

OpenClaw 配置：`~/.openclaw/openclaw.json`
- `agents.defaults.model.primary`：主模型
- `agents.defaults.model.fallbacks`：备用模型列表

## 扩展新平台

在 `references/platforms.md` 中添加新平台支持。

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 命令找不到 | `pip install -e .` 在技能目录运行 |
| API Key 错误 | 检查对应平台的环境变量 |
| 配置不生效 | 运行 `openclaw gateway restart` |
| 模型列表为空 | 运行 `free-model-finder refresh` 刷新缓存 |

## 相关资源

- [平台详情](references/platforms.md)
- [模型对比数据](references/model-comparison.md)
- [自动化脚本](scripts/)
