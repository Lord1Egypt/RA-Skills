# Vision API Configuration

## 必填项

本技能支持**所有 OpenAI 兼容的视觉 API**，你需要自行配置以下三项：

| 字段 | 说明 | 示例 |
|------|------|------|
| `baseUrl` | API 地址 | `https://api.siliconflow.cn/v1` |
| `apiKey` | API 密钥 | `sk-xxx...` |
| `model` | 视觉模型名称 | `Qwen/Qwen3-VL-32B` |

`provider` 字段为可选标识，仅用于日志记录。

## 配置方式

### 方式一：config.json（推荐）

复制 `config.example.json` 为 `config.json`，填入你的 API 信息：

```json
{
  "vision": {
    "provider": "siliconflow",
    "baseUrl": "https://api.siliconflow.cn/v1",
    "apiKey": "sk-your-api-key",
    "model": "Qwen/Qwen3-VL-32B"
  }
}
```

### 方式二：环境变量

```bash
export SV_VISION_API_KEY=sk-your-api-key
export SV_VISION_BASE_URL=https://api.siliconflow.cn/v1
export SV_VISION_MODEL=Qwen/Qwen3-VL-32B
export SV_VISION_PROVIDER=siliconflow   # 可选
```

---

## 推荐视觉模型

以下是经过测试的视觉模型，按性价比排序：

| 模型 | 厂商/平台 | 视觉能力 | 价格 | 推荐场景 |
|------|-----------|---------|------|---------|
| Qwen3-VL-32B | 硅基流动 / 阿里百炼 | ⭐⭐⭐⭐ | 低 | 日常桌面操控（推荐） |
| GLM-4V-Plus | 智谱 BigModel | ⭐⭐⭐⭐ | 低 | 备选方案 |
| GPT-5.4-Mini | OpenAI / V-API 等中转 | ⭐⭐⭐⭐⭐ | 中 | 高精度任务 |
| GPT-5.4 CUA | OpenAI | ⭐⭐⭐⭐⭐ | 高 | 专业 Computer Use |
| Qwen3-VL-8B | 硅基流动（免费额度） | ⭐⭐⭐ | 极低 | 预算有限 |
| Llama 3.2 Vision | Ollama 本地 | ⭐⭐ | 免费 | 有 GPU、隐私优先 |

> **提示**：选择模型时，视觉理解能力比通用对话能力更重要。模型需要能准确识别屏幕上的按钮、输入框、文字等 UI 元素并给出精确坐标。

## 各平台配置示例

### 硅基流动（SiliconFlow）

国内访问快，价格低，推荐首选。

```json
{
  "vision": {
    "provider": "siliconflow",
    "baseUrl": "https://api.siliconflow.cn/v1",
    "apiKey": "sk-your-siliconflow-key",
    "model": "Qwen/Qwen3-VL-32B"
  }
}
```

注册地址：https://siliconflow.cn

### 阿里百炼

阿里云旗下，模型质量高。

```json
{
  "vision": {
    "provider": "dashscope",
    "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "apiKey": "sk-your-dashscope-key",
    "model": "qwen-vl-max"
  }
}
```

注册地址：https://dashscope.console.aliyun.com

### 智谱 BigModel

```json
{
  "vision": {
    "provider": "zhipu",
    "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
    "apiKey": "your-zhipu-key",
    "model": "glm-4v-plus"
  }
}
```

注册地址：https://open.bigmodel.cn

### OpenAI / V-API 等中转

支持所有 OpenAI 兼容的中转站。

```json
{
  "vision": {
    "provider": "openai",
    "baseUrl": "https://api.openai.com/v1",
    "apiKey": "sk-your-key",
    "model": "gpt-5.4-mini"  // 替换为你使用的模型
  }
}
```

### Ollama 本地模型（免费）

需要有 GPU 的机器。

```json
{
  "vision": {
    "provider": "ollama",
    "baseUrl": "http://localhost:11434/v1",
    "apiKey": "ollama",
    "model": "llama3.2-vision"
  }
}
```

---

## API 调用格式

所有 provider 统一使用 OpenAI Chat Completions 格式：

```json
{
  "model": "<your-model>",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "<analysis_prompt>"},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,<screenshot>"}}
    ]
  }],
  "max_tokens": 1500
}
```

如果你的 API 不兼容此格式，可能无法正常使用。

## 常见问题

**Q: 配置后提示 "Vision API not configured"**
A: 检查 `baseUrl`、`apiKey`、`model` 三项是否都已填写。环境变量优先于 config.json。

**Q: API 返回 401/403 错误**
A: API Key 不正确或已过期，请到对应平台重新生成。

**Q: 分析结果不准确，坐标偏移**
A: 尝试更换视觉能力更强的模型（如 GPT-5.4-Mini），或调整 `display.resolution` 确保与实际屏幕分辨率一致。
