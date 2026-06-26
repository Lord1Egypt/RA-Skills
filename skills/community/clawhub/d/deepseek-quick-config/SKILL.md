# DeepSeek Quick Config for OpenClaw

5 分钟配置 DeepSeek V3 作为 OpenClaw 的 AI 模型。

## 为什么选 DeepSeek？

- **性价比最高**：¥0.27/百万 input tokens vs GPT-4o ¥35/百万
- **性能强劲**：接近 GPT-4 水平
- **中文优化**：国产模型，中文理解更好
- **无需 VPN**：国内直连，速度快

## 快速配置

### Step 1: 获取 API Key

1. 访问 https://platform.deepseek.com/
2. 注册/登录
3. 进入 API Keys 页面
4. 创建新 Key

### Step 2: 配置 OpenClaw

```bash
# 方法 1：命令行配置
openclaw configure --section models

# 选择 DeepSeek，粘贴 API Key
```

或编辑 `~/.openclaw/config.yaml`:

```yaml
models:
  default: deepseek-chat
  providers:
    deepseek:
      apiKey: sk-xxxxxxxx
      baseURL: https://api.deepseek.com/v1
```

### Step 3: 测试连接

```bash
openclaw chat "你好，介绍一下你自己"
```

## 成本对比

| 模型 | Input (¥/百万) | Output (¥/百万) | 相对成本 |
|------|---------------|-----------------|---------|
| DeepSeek V3 | ¥0.27 | ¥1.08 | 1x |
| GPT-4o mini | ¥1.05 | ¥4.20 | 4x |
| Claude Haiku | ¥0.63 | ¥3.15 | 3x |
| GPT-4o | ¥35.00 | ¥105.00 | 130x |
| Claude Sonnet | ¥21.00 | ¥105.00 | 97x |

## 常见问题

### Q: 提示 "API key invalid"
A: 检查 Key 是否正确复制，没有多余空格

### Q: 响应很慢
A: 深度思考模式 (deepseek-reasoner) 会慢一些，日常用 deepseek-chat

### Q: 想用 R1 深度思考？
A: 把模型名改成 `deepseek-reasoner`

## 高级配置

### 启用流式输出

```yaml
models:
  providers:
    deepseek:
      stream: true
```

### 自定义温度

```yaml
models:
  providers:
    deepseek:
      temperature: 0.7  # 0-2，默认 1
```

## 需要帮助？

- 微信：yanghu_ai
- Telegram: @yanghu_openclaw

---

Version: 1.0.0
Created: 2026-03-21
