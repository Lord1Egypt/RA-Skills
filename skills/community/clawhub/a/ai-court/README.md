# AI 朝廷 · 多 Agent 协作系统

> **一行命令起王朝，三省六部皆 AI。**
> 
> 以中国古代三省六部制为蓝本的多 Agent 协作框架。

## 🏛️ 简介

**AI 朝廷**是一个基于 OpenClaw 的多 Agent 协作系统，将中国古代三省六部制映射到现代 AI 协作场景：

- **明朝内阁制** - 司礼监调度，内阁优化，六部执行
- **唐朝三省制** - 中书起草，门下审核，尚书执行
- **现代企业制** - CEO 决策，Board 审议，CxO 各司其职

**一台服务器 + OpenClaw = 一支 7×24 在线的 AI 协作团队。**

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **三种制度** | 明朝/唐朝/现代企业可选 |
| **灵活配置** | 1-11 Bot 按需选择 |
| **多平台** | 飞书/Discord 支持 |
| **完整文档** | 配置/部署/故障排除 |

## 📦 安装

```bash
# 通过 clawdhub 安装
clawdhub install ai-court

# 或手动克隆
git clone https://github.com/wanikua/ai-court-skill.git
```

## 🚀 快速开始

### 1. 选择制度 + 配置模板

```bash
# 明朝 3 Bot（推荐）
cp configs/feishu-ming/openclaw-3bot.json ~/.openclaw/openclaw.json

# 唐朝 3 Bot
cp configs/feishu-tang/openclaw-3bot.json ~/.openclaw/openclaw.json

# 现代 3 Bot
cp configs/feishu-modern/openclaw-3bot.json ~/.openclaw/openclaw.json
```

### 2. 配置 Bot 凭证

编辑 `~/.openclaw/openclaw.json`，填入你的飞书应用凭证。

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

## 📋 配置模板

| 制度 | 1 Bot | 3 Bot | 完整版 |
|------|-------|-------|--------|
| **明朝** | ✅ | ✅ | 9 Bot |
| **唐朝** | ✅ | ✅ | 11 Bot |
| **现代** | ✅ | ✅ | 9 Bot |

## 📖 文档

- [飞书配置指南](./docs/feishu-setup-simple.md) - 5 分钟快速配置
- [灵活配置指南](./docs/feishu-flexible-setup.md) - 按需选择 Bot 数量

## 🔗 相关项目

| 项目 | 说明 |
|------|------|
| **danghuangshang** | 生产部署实例 - https://github.com/wanikua/danghuangshang |
| **OpenClaw** | 底层框架 - https://github.com/openclaw/openclaw |

## 📝 License

MIT License
