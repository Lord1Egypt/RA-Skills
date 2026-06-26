# 安装指南

## 适用场景

- 在 Claude Code 中安装和配置 Claude-Flow
- 通过 MCP 将 Claude-Flow 集成到 Claude Code 工作流
- 配置 Anthropic API 密钥

---

## 方式一：一键安装脚本（推荐）

> **AI 可自动执行**

```bash
# 完整安装（MCP + 诊断工具）
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash -s -- --full

# 或仅基础安装
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash
```

---

## 方式二：npx 安装

```bash
# 交互式向导安装
npx ruflo@latest init --wizard

# 或直接初始化（接受默认配置）
npx ruflo@latest init
```

---

## 方式三：全局 npm 安装

```bash
npm install -g claude-flow
# 或
npm install -g ruflo

# 验证
claude-flow --version
ruflo --version
```

---

## 配置 Anthropic API 密钥

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# 或写入 .env 文件
echo 'ANTHROPIC_API_KEY=sk-ant-...' >> .env
```

---

## 在 Claude Code 中配置 MCP

### 自动配置（推荐）

```bash
# 在 Claude Code 会话中执行
claude mcp add claude-flow --scope user npx ruflo@latest mcp start
```

### 手动配置

在 `~/.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "claude-flow": {
      "command": "npx",
      "args": ["ruflo@latest", "mcp", "start"],
      "env": {
        "ANTHROPIC_API_KEY": "your-key"
      }
    }
  }
}
```

**安装后必须重启 Claude Code** 使 MCP 生效。

---

## 验证安装

```bash
# 检查版本
npx ruflo@latest --version

# 检查 Claude Code MCP 集成
claude mcp list  # 应显示 claude-flow

# 查看可用智能体
npx ruflo@latest agent list

# 系统诊断
npx ruflo@latest hooks intelligence --status
```

---

## 完成确认检查清单

- [ ] 安装命令执行成功
- [ ] `ANTHROPIC_API_KEY` 环境变量已配置
- [ ] Claude Code 重启后 MCP 工具可用
- [ ] `npx ruflo@latest agent list` 显示可用智能体列表

---

## 下一步

- [快速开始](02-quickstart.md) — 启动智能体、蜂群模式、在 Claude Code 中使用
