# Claude Code 安装指南

## 系统要求

- Node.js 18+ 
- Linux/macOS/Windows
- 最小 2GB 内存

## 安装步骤

### 1. 安装 Node.js (如果没有)

```bash
# Debian/Ubuntu
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# 验证
node --version  # 应显示 v20.x.x
npm --version
```

### 2. 安装 Claude Code

```bash
# 全局安装
npm install -g @anthropic-ai/claude-code

# 验证
claude --version
```

### 3. 配置 API

Claude Code 支持多种 API 提供商：

#### 直接使用 Anthropic API

```bash
export ANTHROPIC_API_KEY="your-api-key"
claude
```

#### 使用代理服务 (如腾讯 Coding Plan)

```bash
export ANTHROPIC_API_KEY="your-api-key"
export ANTHROPIC_BASE_URL="https://api.example.com/v1"
export ANTHROPIC_MODEL="model-name"
claude
```

### 4. 权限配置

创建 `~/.claude/settings.local.json`:

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

**注意**: `--dangerously-skip-permissions` 不能在 root 用户下使用。

### 5. 持久化配置 (Docker 环境)

在 Docker 容器中，需要将配置目录映射到持久化存储：

```bash
# 创建持久化目录
mkdir -p ~/workspace/claude-code/.claude

# 创建符号链接
ln -sf ~/workspace/claude-code/.claude ~/.claude
```

这样容器重启后配置不会丢失。

## 配置文件说明

| 文件 | 用途 |
|------|------|
| `~/.claude/settings.json` | 全局设置 |
| `~/.claude/settings.local.json` | 本地权限配置 |
| `CLAUDE.md` | 项目级指令文件 |

## 常用命令

```bash
claude              # 启动交互式会话
claude "task"       # 直接执行任务
claude --print      # 输出到 stdout
claude --help       # 查看帮助
```
