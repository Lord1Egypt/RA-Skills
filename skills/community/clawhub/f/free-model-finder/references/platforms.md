# 平台详情 - Free Model Finder

## OpenRouter

**网址**: https://openrouter.ai
**免费模型**: 多个 provider 的 `:free` 后缀模型
**API Key**: 必需（免费获取）

### 可用免费模型（动态变化）
- `openrouter/free` - 智能路由，自动选择最佳可用模型
- `qwen/qwen-2.5-72b-instruct:free` - Qwen 2.5 72B
- `meta-llama/llama-3.1-8b-instruct:free` - Llama 3.1 8B
- `google/gemma-2-9b-it:free` - Gemma 2 9B
- `mistralai/mistral-7b-instruct:free` - Mistral 7B
- `01-ai/yi-large:free` - Yi Large

### Rate Limits
- 免费模型：约 20-100 requests/天（因模型而异）
- 自动轮换建议：启用 fallbacks

### 配置示例
```json
{
  "model": "openrouter/qwen/qwen-2.5-72b-instruct:free",
  "fallbacks": [
    "openrouter/free",
    "openrouter/meta-llama/llama-3.1-8b-instruct:free"
  ]
}
```

---

## Groq

**网址**: https://groq.com
**免费额度**: 当前完全免费（beta 期间）
**API Key**: 必需

### 可用模型
- `llama-3.1-70b-versatile` - Llama 3.1 70B（超快）
- `llama-3.1-8b-instant` - Llama 3.1 8B（极速）
- `mixtral-8x7b-32768` - Mixtral 8x7B
- `gemma2-9b-it` - Gemma 2 9B

### 优势
- 速度极快（LPU 加速）
- 免费额度充足
- 适合实时对话

### Rate Limits
- 当前 beta：约 30 requests/分钟
- 生产环境可能调整

---

## Google AI Studio (Gemini)

**网址**: https://aistudio.google.com
**免费额度**: 60 requests/分钟（Gemini 1.5 Flash）
**API Key**: 必需

### 可用模型
- `gemini-1.5-flash` - 快速、低成本
- `gemini-1.5-pro` - 高质量（有限免费）

### Rate Limits
- Flash: 60 RPM / 1M tokens/分钟
- Pro: 2 RPM / 240K tokens/分钟

---

## HuggingFace Inference API

**网址**: https://huggingface.co
**免费额度**: 有限免费额度
**API Key**: 必需

### 可用模型
- 数千个开源模型
- 质量参差不齐，需测试

### 注意事项
- 免费额度有限
- 冷启动延迟高
- 适合偶尔使用

---

## Ollama (本地)

**网址**: https://ollama.ai
**费用**: 完全免费（本地运行）
**API Key**: 不需要

### 安装
```bash
# Windows
winget install Ollama.Ollama

# 或使用安装包
# https://ollama.ai/download
```

### 常用模型
```bash
ollama pull llama3.1      # Llama 3.1 8B
ollama pull qwen2.5       # Qwen 2.5 7B/72B
ollama pull mistral       # Mistral 7B
ollama pull gemma2        # Gemma 2 9B
```

### 优势
- 完全免费
- 隐私保护
- 无网络依赖
- 无 rate limit

### 劣势
- 需要本地 GPU/内存
- 速度取决于硬件

---

## 平台对比

| 平台 | 免费程度 | 速度 | 质量 | 稳定性 | 推荐场景 |
|------|----------|------|------|--------|----------|
| OpenRouter | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 日常使用 |
| Groq | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 实时对话 |
| Google | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 高质量需求 |
| HF | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 实验用途 |
| Ollama | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 本地隐私 |

---

## 推荐配置策略

### 方案 A：纯免费（推荐新手）
```
主模型：openrouter/free
备用：groq/llama-3.1-8b-instant, ollama/llama3.1
```

### 方案 B：速度优先
```
主模型：groq/llama-3.1-8b-instant
备用：groq/llama-3.1-70b-versatile, openrouter/free
```

### 方案 C：质量优先
```
主模型：google/gemini-1.5-flash
备用：openrouter/qwen-2.5-72b-instruct:free, groq/llama-3.1-70b-versatile
```

### 方案 D：本地优先
```
主模型：ollama/llama3.1
备用：groq/llama-3.1-8b-instant, openrouter/free
```
