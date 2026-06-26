---
name: install-openclaw
description: OpenClaw 全自动安装、配置和修复工具。包括：OpenClaw 安装、Claude API 中转站配置、飞书插件集成、bug 自动修复。当用户需要安装、配置或修复 OpenClaw 时使用此技能。
---

# OpenClaw 全自动安装与配置

## 概述

本技能提供 OpenClaw 的一站式安装、配置和维护服务：

1. **全自动安装 OpenClaw** - 一键安装最新版本的 OpenClaw
2. **Claude API 中转站配置** - 接入用户的 AI 中转站
3. **飞书插件集成** - 安装并配置飞书消息通道
4. **Bug 自动修复** - 检测并修复 OpenClaw 的常见问题

## 依赖

确保已安装：
- Node.js 18+ 
- pnpm
- Python 3.8+

## 工作流程

### 阶段一：学习 OpenClaw 文档

首先阅读 OpenClaw 官方文档，成为 OpenClaw 专家：

```bash
# 阅读本地文档
ls ~/Library/pnpm/global/*/node_modules/openclaw/docs/

# 查看安装文档
cat ~/Library/pnpm/global/*/node_modules/openclaw/docs/install/*.md

# 查看网关配置文档
cat ~/Library/pnpm/global/*/node_modules/openclaw/docs/gateway/*.md
```

**关键知识点：**
- OpenClaw 是一个自托管网关，连接聊天应用（WhatsApp、Telegram、Discord、iMessage 等）到 AI 助手
- 核心组件：Gateway（网关）、Control UI（控制界面）、Plugins（插件）
- 配置文件位置：`~/.openclaw/`
- 日志文件位置：`~/.openclaw/logs/`

### 阶段二：检查 OpenClaw 安装状态

```bash
# 检查是否已安装
which openclaw
openclaw --version

# 检查网关状态
openclaw gateway status

# 查看日志
openclaw logs --tail 100
```

### 阶段三：全自动安装 OpenClaw

如果未安装或需要重新安装：

```bash
# 使用官方安装脚本
curl -fsSL https://openclaw.ai/install.sh | bash

# 或使用 pnpm 安装
pnpm add -g openclaw

# 验证安装
openclaw --version
```

### 阶段四：配置 Claude API 中转站

根据用户提供的中转站配置文档进行配置：

**配置信息：**
- AI 中转站 URL：`https://ai.jiexi6.cn`
- API Key：用户自行提供

**配置步骤：**

1. 编辑 OpenClaw 配置文件：
```bash
# 编辑模型配置
nano ~/.openclaw/config/models.json
```

2. 添加中转站配置：
```json
{
  "models": {
    "claude": {
      "provider": "openai-compatible",
      "baseUrl": "https://ai.jiexi6.cn/v1",
      "apiKey": "用户_API_Key",
      "models": ["claude-sonnet-4-5-20250929", "claude-opus-4-5-20250929"]
    }
  }
}
```

3. 验证配置：
```bash
openclaw models list
openclaw models test claude
```

### 阶段五：安装飞书插件

**步骤：**

1. 获取飞书应用凭证：
   - 访问 [飞书开放平台](https://open.feishu.cn/app)
   - 创建自建应用
   - 获取 App ID 和 App Secret
   - 配置 Bot 权限

2. 安装飞书插件：
```bash
# 安装飞书通道插件
openclaw plugins install feishu

# 或手动安装
cd ~/.openclaw/plugins
git clone https://github.com/openclaw/feishu-plugin.git
```

3. 配置飞书插件：
```bash
# 编辑飞书配置
nano ~/.openclaw/config/feishu.json
```

配置内容：
```json
{
  "appId": "cli_xxxxxxxxxxxxx",
  "appSecret": "xxxxxxxxxxxxxxxxxxxxx",
  "verificationToken": "xxxxxxxxxxxxxxxxxxxxx",
  "encryptKey": "xxxxxxxxxxxxxxxxxxxxx"
}
```

4. 启动飞书通道：
```bash
openclaw channels enable feishu
openclaw channels status feishu
```

### 阶段六：Bug 自动检测与修复

**常见问题及修复：**

1. **网关无法启动：**
```bash
# 检查端口占用
lsof -i :8080

# 清理并重启
openclaw gateway stop
openclaw gateway clean
openclaw gateway start
```

2. **模型连接失败：**
```bash
# 测试 API 连接
curl -X POST https://ai.jiexi6.cn/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# 更新模型配置
openclaw models refresh
```

3. **插件加载失败：**
```bash
# 重新安装插件
openclaw plugins reinstall feishu

# 检查插件依赖
cd ~/.openclaw/plugins/feishu
pnpm install
```

4. **日志文件过大：**
```bash
# 清理旧日志
openclaw logs clean --days 7

# 配置日志轮转
nano ~/.openclaw/config/logging.json
```

### 阶段七：验证和测试

```bash
# 检查整体状态
openclaw status

# 测试消息发送
openclaw message send --channel feishu --to "测试用户" --message "测试消息"

# 查看运行状态
openclaw gateway logs --tail 50
```

## 自动化脚本

运行全自动安装脚本：

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/install-openclaw

# 运行安装脚本
./scripts/install.sh

# 运行配置脚本
./scripts/configure-claude.sh

# 运行飞书安装脚本
./scripts/install-feishu.sh

# 运行修复脚本
./scripts/fix-bugs.sh
```

## 故障排查

### 查看日志

```bash
# 查看网关日志
tail -f ~/.openclaw/logs/gateway.log

# 查看插件日志
tail -f ~/.openclaw/logs/plugins/feishu.log

# 使用 openclaw 命令查看
openclaw logs --follow
```

### 常见问题

1. **权限问题：**
```bash
chmod -R 755 ~/.openclaw
```

2. **依赖问题：**
```bash
cd ~/.openclaw
pnpm install
```

3. **配置问题：**
```bash
# 重置配置
openclaw config reset

# 重新配置
openclaw onboard
```

## 记忆要点

将以下信息写入 MEMORY.md：

1. **OpenClaw 安装路径：** `~/Library/pnpm/global/*/node_modules/openclaw/`
2. **配置目录：** `~/.openclaw/`
3. **日志目录：** `~/.openclaw/logs/`
4. **AI 中转站 URL：** `https://ai.jiexi6.cn`
5. **飞书文档：** https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/docx-overview

## 下一步

安装完成后：
1. 运行 `openclaw onboard` 完成向导设置
2. 访问 Control UI：http://localhost:8080
3. 配对移动设备
4. 测试消息收发

---

**参考文档：**
- OpenClaw 官方文档：https://docs.openclaw.ai/
- 飞书开放平台：https://open.feishu.cn/
- AI 中转站配置文档：用户提供的飞书文档
