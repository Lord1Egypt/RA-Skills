# Dify 模型提供商配置

## 支持的模型提供商

### 主流提供商

| 提供商 | 模型类型 | 备注 |
|-------|---------|------|
| OpenAI | LLM, Embedding, TTS, ASR | GPT-4, GPT-3.5, Whisper |
| Anthropic | LLM | Claude系列 |
| Azure OpenAI | LLM, Embedding | 企业Azure部署 |
| Google | LLM | Gemini系列 |
| AWS Bedrock | LLM | 多模型托管 |
| Cohere | LLM, Embedding, Rerank | |
| Mistral | LLM | |
| Replicate | LLM | 开源模型托管 |

### 国内提供商

| 提供商 | 模型 |
|-------|------|
| 智谱AI | GLM-4, GLM-3-turbo |
| 百度文心 | ERNIE系列 |
| 阿里通义 | Qwen系列 |
| 字节豆包 | Doubao系列 |
| Moonshot | Kimi系列 |
| DeepSeek | DeepSeek系列 |
| MiniMax | abab系列 |
| 讯飞星火 | Spark系列 |

### 本地/开源模型

| 方案 | 说明 |
|-----|------|
| Ollama | 本地运行开源模型 |
| LocalAI | 兼容OpenAI API的本地方案 |
| Xinference | 多模型推理服务 |
| vLLM | 高性能LLM推理 |

---

## 模型配置

### 添加模型

1. Settings → Model Providers
2. 选择提供商
3. 配置API Key或自定义端点
4. 选择要使用的模型

### 模型参数

```yaml
Temperature: 0-2          # 创造性程度
Top P: 0-1                # 核采样
Max Tokens: 1-32000       # 最大输出
Frequency Penalty: -2-2   # 频率惩罚
Presence Penalty: -2-2    # 存在惩罚
```

### 模型能力

| 能力 | 说明 |
|-----|------|
| Chat | 对话生成 |
| Completion | 文本补全 |
| Vision | 图像理解 |
| Function Call | 工具调用 |
| Reasoning | 推理能力 |

---

## 自定义模型

### OpenAI兼容接口

配置自定义端点使用兼容接口:

```yaml
Base URL: http://your-server:8000/v1
API Key: your-key
Model Name: your-model
```

### 本地模型 (Ollama)

```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 运行模型
ollama run llama2

# Ollama默认端口
# http://localhost:11434
```

在Dify中配置:
- Provider: Ollama
- Base URL: http://host.docker.internal:11434

---

## 模型负载均衡

### 配置多个同类型模型

1. 添加多个模型实例
2. 在应用中选择模型
3. 系统自动负载均衡

### 故障转移

模型不可用时自动切换到备用模型。

---

## 成本优化

### 模型选择策略

| 场景 | 推荐模型 |
|-----|---------|
| 简单对话 | GPT-3.5, Qwen-Turbo |
| 复杂推理 | GPT-4, Claude-3 |
| 中文场景 | GLM-4, Qwen, DeepSeek |
| 代码生成 | DeepSeek-Coder, GPT-4 |
| 本地部署 | Ollama + 开源模型 |

### Token优化

- 使用 shorter prompts
- 缓存常用回复
- 合理设置 max_tokens
- 使用 Embedding 模型进行检索而非全文
