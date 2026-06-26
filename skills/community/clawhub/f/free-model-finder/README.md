# Free Model Finder - 安装指南

## 快速安装

```bash
# 1. 进入技能目录
cd C:\Users\sukun\.openclaw\workspace\skills\free-model-finder

# 2. 安装 CLI 工具
pip install -e .

# 3. 验证安装
free-model-finder --help
```

## 配置 API Keys（可选但推荐）

### OpenRouter（推荐）
```bash
# 获取 key: https://openrouter.ai/keys
openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
```

### Groq（速度最快）
```bash
# 获取 key: https://console.groq.com/keys
openclaw config set env.GROQ_API_KEY "gsk_..."
```

### Google AI Studio
```bash
# 获取 key: https://aistudio.google.com/app/apikey
openclaw config set env.GOOGLE_API_KEY "..."
```

## 常用命令

```bash
# 查看所有免费模型
free-model-finder list

# 只看 Groq 平台
free-model-finder list --platform groq

# 自动配置最优免费模型
free-model-finder auto

# 切换到指定模型
free-model-finder switch groq/llama-3.1-8b-instant

# 查看当前配置
free-model-finder status
```

## 应用配置

```bash
# 1. 运行自动配置
free-model-finder auto

# 2. 重启 OpenClaw Gateway
openclaw gateway restart

# 3. 验证新模型
# 发送 /status 或开始新对话
```

## 故障排查

### 命令找不到
```bash
# 确保已安装
pip install -e .

# 检查 PATH
where free-model-finder
```

### 配置不生效
```bash
# 重启 Gateway
openclaw gateway restart

# 开始新会话
/new
```
