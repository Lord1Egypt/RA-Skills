# 支持的 LLM 模型列表

财经新闻分析器支持多种大语言模型，包括国际主流模型和国产大模型。

---

## 🌐 国际模型

### OpenAI GPT 系列

| 模型 | 模型名称 | 适用场景 | 价格 |
|------|---------|---------|------|
| GPT-4o | `gpt-4o` | 高精度分析，复杂推理 | $$$$ |
| GPT-4o Mini | `gpt-4o-mini` | **推荐** 日常分析，性价比高 | $$ |
| GPT-4 Turbo | `gpt-4-turbo` | 高质量分析 | $$$ |
| GPT-3.5 Turbo | `gpt-3.5-turbo` | 快速分析，低成本 | $ |

**配置方式：**
```bash
export OPENAI_API_KEY=sk-xxx
```

**使用示例：**
```bash
python scripts/main.py --model gpt-4o-mini
python scripts/analyze_sentiment.py --model gpt-4o --input news.json
```

**获取 API Key：** https://platform.openai.com/api-keys

---

### Anthropic Claude 系列

| 模型 | 模型名称 | 适用场景 | 价格 |
|------|---------|---------|------|
| Claude 3.5 Sonnet | `claude-3-5-sonnet-20241022` | **推荐** 平衡性能与成本 | $$$ |
| Claude 3 Opus | `claude-3-opus-20240229` | 最高质量分析 | $$$$ |
| Claude 3 Haiku | `claude-3-haiku-20240307` | 快速分析 | $$ |

**配置方式：**
```bash
export ANTHROPIC_API_KEY=sk-ant-xxx
```

**使用示例：**
```bash
python scripts/main.py --model claude-3-5-sonnet-20241022
```

**获取 API Key：** https://console.anthropic.com/settings/keys

---

## 🇨🇳 国产大模型

### 阿里通义千问 (DashScope)

| 模型 | 模型名称 | 适用场景 | 价格 |
|------|---------|---------|------|
| Qwen-Max | `qwen-max` | 复杂任务，高质量 | $$$ |
| Qwen-Plus | `qwen-plus` | **推荐** 平衡性能 | $$ |
| Qwen-Turbo | `qwen-turbo` | 快速响应 | $ |
| Qwen-Long | `qwen-long` | 长文本分析 | $$ |

**配置方式：**
```bash
export DASHSCOPE_API_KEY=sk-xxx
```

**使用示例：**
```bash
python scripts/main.py --model qwen-plus
python scripts/analyze_sentiment.py --model qwen-max --input news.json
```

**获取 API Key：** https://dashscope.console.aliyun.com/apiKey

**价格参考：** https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-llm-price

---

### 百度文心一言 (Qianfan)

| 模型 | 模型名称 | 适用场景 | 价格 |
|------|---------|---------|------|
| ERNIE-Bot 4.0 | `ernie-bot-4.0` | 高质量分析 | $$$ |
| ERNIE-Bot | `ernie-bot` | **推荐** 通用场景 | $$ |
| ERNIE-Bot Turbo | `ernie-bot-turbo` | 快速响应 | $ |
| ERNIE-Speed | `ernie-speed` | 低成本 | $ |

**配置方式：**
```bash
export QIANFAN_AK=xxx        # API Key
export QIANFAN_SK=xxx        # Secret Key
```

**使用示例：**
```bash
python scripts/main.py --model ernie-bot
python scripts/analyze_sentiment.py --model ernie-bot-4.0 --input news.json
```

**获取 API Key：** https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application

**价格参考：** https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlrk4akp7

---

### 智谱 AI (GLM 系列)

| 模型 | 模型名称 | 适用场景 | 价格 |
|------|---------|---------|------|
| GLM-4 | `glm-4` | 高质量分析 | $$$ |
| GLM-4-Flash | `glm-4-flash` | **推荐** 快速响应 | $ |
| GLM-3-Turbo | `glm-3-turbo` | 低成本 | $ |

**配置方式：**
```bash
export ZHIPUAI_API_KEY=xxx.xxx
```

**使用示例：**
```bash
python scripts/main.py --model glm-4
python scripts/analyze_sentiment.py --model glm-4-flash --input news.json
```

**获取 API Key：** https://open.bigmodel.cn/usercenter/apikeys

**价格参考：** https://open.bigmodel.cn/dev/api/thirdparty-frame/introduction

---

## 💻 本地模型

### Ollama

支持运行本地 LLM 模型，完全免费，数据隐私性好。

**支持的模型：**
- Llama 3 / Llama 3.1 / Llama 3.2
- Mistral / Mixtral
- Qwen (通义千问开源版)
- Yi (零一万物)
- 以及任何 Ollama 支持的模型

**安装 Ollama：**

Windows/macOS/Linux:
```bash
# 下载安装
curl -fsSL https://ollama.com/install.sh | sh

# 或使用 Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

**下载模型：**
```bash
# Llama 3.1 (8B)
ollama pull llama3.1

# Llama 3.1 (70B)
ollama pull llama3.1:70b

# Qwen2.5 (7B)
ollama pull qwen2.5

# Mistral (7B)
ollama pull mistral
```

**配置方式：**
```bash
# 可选：自定义 Ollama 地址
export OLLAMA_BASE_URL=http://localhost:11434/v1
```

**使用示例：**
```bash
# 使用 Llama 3.1
python scripts/main.py --model ollama/llama3.1

# 使用 Qwen2.5
python scripts/main.py --model ollama/qwen2.5

# 指定自定义地址
python scripts/main.py --model ollama/llama3.1 --ollama-url http://192.168.1.100:11434/v1
```

**Ollama 官网：** https://ollama.com

---

## 📊 模型对比

### 准确性排名

```
GPT-4o ≈ Claude 3.5 Sonnet > GLM-4 > Qwen-Max > ERNIE-Bot 4.0 > GPT-3.5 > 本地模型
```

### 速度排名

```
本地模型 (GPU) > GPT-4o Mini > Qwen-Turbo > ERNIE-Speed > GLM-4-Flash > Claude Haiku
```

### 性价比排名

```
本地模型 (免费) > GPT-4o Mini > Qwen-Plus > GLM-4-Flash > ERNIE-Bot > GPT-4o
```

### 中文理解能力

```
Qwen 系列 > ERNIE 系列 > GLM 系列 > GPT-4o > Claude > 本地模型
```

---

## 🎯 推荐配置

### 最佳质量（不差钱）
```bash
export OPENAI_API_KEY=sk-xxx
python scripts/main.py --model gpt-4o
```

### 最佳性价比（推荐）
```bash
export OPENAI_API_KEY=sk-xxx
python scripts/main.py --model gpt-4o-mini
```

### 国产最佳
```bash
export DASHSCOPE_API_KEY=sk-xxx
python scripts/main.py --model qwen-plus
```

### 完全免费（本地）
```bash
# 需要 NVIDIA GPU (8GB+ VRAM 推荐)
ollama pull llama3.1
python scripts/main.py --model ollama/llama3.1
```

### 企业级（高并发）
```bash
# 多个 API Key 轮换
export OPENAI_API_KEY=sk-xxx,sk-yyy,sk-zzz
python scripts/main.py --model gpt-4o-mini --max-concurrent 20
```

---

## ⚙️ 高级配置

### 多模型轮换

在 EXTEND.md 中配置：

```yaml
llm_api:
  # 主模型
  primary_model: gpt-4o-mini
  
  # 备选模型（主模型失败时自动切换）
  fallback_models:
    - gpt-3.5-turbo
    - qwen-plus
    - glm-4-flash
  
  # 模型路由规则
  routing:
    # 短文本使用便宜模型
    short_text_model: gpt-4o-mini
    # 长文本使用高质量模型
    long_text_model: gpt-4o
    # 中文内容使用国产模型
    chinese_content_model: qwen-plus
```

### 成本优化

```yaml
# 设置每日预算上限
cost_control:
  daily_budget: 10.0  # 美元
  alert_threshold: 8.0  # 达到 80% 时提醒
  
  # 自动切换到便宜模型
  auto_switch:
    enabled: true
    threshold_percent: 90  # 预算使用 90% 时切换
    fallback_model: gpt-3.5-turbo
```

---

## 🔧 故障排查

### 问题 1: API Key 无效

**错误信息：** `401 Unauthorized` 或 `Invalid API Key`

**解决方案：**
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置
export OPENAI_API_KEY=sk-xxx

# 验证 API Key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 问题 2: 模型不支持

**错误信息：** `Model not found` 或 `404 Not Found`

**解决方案：**
```bash
# 检查模型名称是否正确
python scripts/main.py --model gpt-4o-mini  # 正确
python scripts/main.py --model gpt4         # 错误

# 查看支持的模型列表
python -c "from openai import OpenAI; print(OpenAI().models.list())"
```

### 问题 3: 速率限制

**错误信息：** `429 Too Many Requests` 或 `Rate limit exceeded`

**解决方案：**
```bash
# 降低并发数
python scripts/main.py --max-concurrent 3

# 使用多个 API Key
export OPENAI_API_KEY=sk-xxx,sk-yyy,sk-zzz

# 添加重试延迟
python scripts/main.py --retry-delay 5
```

### 问题 4: 本地模型 Ollama 连接失败

**错误信息：** `Connection refused` 或 `Cannot connect to Ollama`

**解决方案：**
```bash
# 检查 Ollama 是否运行
ollama list

# 启动 Ollama
ollama serve

# 检查端口
netstat -an | grep 11434

# 使用正确的地址
export OLLAMA_BASE_URL=http://localhost:11434/v1
```

---

## 📚 参考资料

- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [阿里 DashScope 定价](https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-llm-price)
- [百度千帆定价](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlrk4akp7)
- [智谱 AI 定价](https://open.bigmodel.cn/dev/api/thirdparty-frame/introduction)
- [Ollama Models](https://ollama.com/library)

---

## 🆙 更新记录

- 2026-03-10: 新增多模型支持（通义千问、文心一言、智谱 AI、Ollama）
- 后续将持续添加更多模型支持
