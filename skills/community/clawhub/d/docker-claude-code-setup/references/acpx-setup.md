# acpx 多代理工具配置

## 什么是 acpx

acpx 是 Anthropic 提供的 ACP (Agent Communication Protocol) 工具，可以在多个 AI 编码代理之间切换：

- Claude Code
- OpenAI Codex
- Gemini CLI
- Cursor
- 更多...

## 安装

```bash
# 需要 Node.js 18+
npm install -g @anthropic-ai/acpx

# 验证
acpx --version
```

## 配置文件

创建 `~/.acpx/config.json`:

```json
{
  "defaultAgent": "claude-code",
  "agents": {
    "claude-code": {
      "command": "claude",
      "args": [],
      "env": {
        "ANTHROPIC_API_KEY": "your-key-here"
      }
    },
    "codex": {
      "command": "codex",
      "args": [],
      "env": {
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  }
}
```

## 使用方法

```bash
# 使用默认代理
acpx "fix the bug in app.ts"

# 指定代理
acpx claude-code "add error handling"
acpx codex "refactor this module"

# 查看帮助
acpx --help
```

## 持久化配置 (Docker)

```bash
# 创建持久化目录
mkdir -p ~/workspace/.acpx

# 创建符号链接
ln -sf ~/workspace/.acpx ~/.acpx
```

## 环境变量

可以在配置文件中或通过环境变量设置：

```bash
# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI (for Codex)
export OPENAI_API_KEY="sk-..."

# 自定义 API 端点
export ANTHROPIC_BASE_URL="https://api.example.com/v1"
```
