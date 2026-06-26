# API 配置指南

## 支持的 API 提供商

Claude Code 支持多种 API 提供商：

| 提供商 | BASE_URL | 说明 |
|--------|----------|------|
| Anthropic | https://api.anthropic.com | 官方 API |
| 腾讯 Coding | https://api.lkeap.cloud.tencent.com/coding/anthropic | Coding Plan |
| DeepSeek | https://api.deepseek.com | DeepSeek API |
| 百度千帆 | https://aip.baidubce.com/rpc/2.0/ai_custom/v1 | 百度 API |
| 阿里百炼 | https://dashscope.aliyuncs.com/compatible-mode/v1 | 阿里 API |

## 配置方法

### 方法 1: 环境变量

```bash
# 基本配置
export ANTHROPIC_API_KEY="your-api-key"

# 使用代理服务
export ANTHROPIC_API_KEY="your-api-key"
export ANTHROPIC_BASE_URL="https://api.example.com/v1"
export ANTHROPIC_MODEL="model-name"  # 可选

# 启动 Claude Code
claude
```

### 方法 2: .env 文件

在项目目录创建 `.env`:

```env
ANTHROPIC_API_KEY=your-api-key
ANTHROPIC_BASE_URL=https://api.example.com/v1
ANTHROPIC_MODEL=model-name
```

### 方法 3: acpx 配置

在 `~/.acpx/config.json` 中配置每个代理的环境变量。

## 模型名称

| 提供商 | 模型名称示例 |
|--------|-------------|
| Anthropic | claude-sonnet-4-20250514 |
| 腾讯 Coding | glm-5, glm-4 |
| DeepSeek | deepseek-chat, deepseek-coder |

## 安全建议

1. **不要硬编码 API Key** - 使用环境变量或配置文件
2. **添加到 .gitignore** - 防止意外提交
3. **使用 .env.local** - 本地开发时使用不跟踪的文件
4. **定期轮换 Key** - 安全最佳实践

## Docker 环境持久化

```bash
# 在持久化目录存储配置
mkdir -p ~/workspace/.claude
mkdir -p ~/workspace/.env

# 创建符号链接
ln -sf ~/workspace/.claude ~/.claude

# 环境变量可在启动脚本中设置
# 或使用 .env 文件
```

## 常见问题

### Q: LiteLLM 代理不兼容工具调用?

某些代理服务 (如 LiteLLM) 在流式响应时不兼容某些模型的工具调用。

**解决方案**: 直接连接 API，不使用代理。

```bash
# 直接连接，绕过 LiteLLM
export ANTHROPIC_BASE_URL="https://api.example.com/anthropic"
claude
```

### Q: 权限错误?

root 用户不能使用 `--dangerously-skip-permissions`。

**解决方案**: 配置 `settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(**)",
      "Write(**)",
      "Bash(**)"
    ]
  }
}
```
