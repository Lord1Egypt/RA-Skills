# OpenClaw 全自动安装技能

🦞 一站式 OpenClaw 安装、配置和维护工具

## 功能

- ✅ **全自动安装 OpenClaw** - 一键安装最新版本
- ✅ **Claude API 中转站配置** - 接入 AI 中转站
- ✅ **飞书插件集成** - 安装并配置飞书消息通道
- ✅ **Bug 自动修复** - 检测并修复常见问题

## 快速开始

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/install-openclaw

# 1. 安装 OpenClaw
./scripts/install.sh

# 2. 配置 Claude API
./scripts/configure-claude.sh

# 3. 安装飞书插件
./scripts/install-feishu.sh

# 4. 修复 Bug
./scripts/fix-bugs.sh
```

## 脚本说明

### install.sh
- 检查 Node.js、pnpm、Python 依赖
- 安装 OpenClaw
- 初始化配置目录

### configure-claude.sh
- 配置 AI 中转站 URL 和 API Key
- 创建模型配置文件
- 测试 API 连接

### install-feishu.sh
- 获取飞书应用凭证
- 安装飞书插件
- 配置飞书通道

### fix-bugs.sh
- 检查网关状态
- 清理日志文件
- 修复权限问题
- 检查插件依赖
- 测试 API 连接
- 重启网关

## 配置信息

### AI 中转站
- URL: `https://ai.jiexi6.cn`
- 需要 API Key

### 飞书配置
- 需要飞书开放平台应用凭证
- App ID、App Secret、Verification Token

## 故障排查

查看日志：
```bash
openclaw logs --follow
```

查看状态：
```bash
openclaw status
```

重置配置：
```bash
openclaw config reset
```

## 参考文档

- [OpenClaw 官方文档](https://docs.openclaw.ai/)
- [飞书开放平台](https://open.feishu.cn/)

## 作者

自动创建 by OpenClaw Agent
