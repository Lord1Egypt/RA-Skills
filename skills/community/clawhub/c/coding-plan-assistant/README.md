# coding-plan-assistant

> 管理各种编程助手（Coding Plan）的注册、购买和凭据配置流程

## 快速开始

### 1. 查看支持的平台

```bash
node index.js list
```

### 2. 检查配置状态

```bash
node scripts/check-status.js
```

### 3. 对比定价

```bash
node scripts/compare-pricing.js
```

### 4. 获取注册指南

```bash
node index.js register claude-code
```

### 5. 配置 API Key

对 智能体 说：
```
配置 GitHub Copilot
```

然后提供你的 API Key，技能会安全存储到 `.openclaw/.env`。

## 功能特性

- ✅ **7 个主流平台支持**: GitHub Copilot、Claude Code、Gemini CLI、Codex、Qwen Code、百度飞桨、OpenRouter
- ✅ **安全凭据管理**: 存储在 `.openclaw/.env`，自动脱敏显示
- ✅ **注册引导**: 提供详细的注册步骤和官方链接
- ✅ **成本对比**: 清晰的定价对比和推荐方案
- ✅ **状态检测**: 自动检测已配置的凭据
- ✅ **凭据轮换**: 支持安全轮换 API Key

## 自然语言使用

对 智能体 说：

| 需求 | 说法 |
|------|------|
| 查看平台 | "支持哪些编程助手？" |
| 检查配置 | "我的 API Key 配置好了吗？" |
| 注册指导 | "帮我注册 Claude Code" |
| 价格对比 | "哪个平台最便宜？" |
| 配置 Key | "配置 GitHub Copilot" |
| 轮换 Key | "轮换 OpenAI API Key" |

## 安全提示

- 🔒 所有 API Key 存储在 `.openclaw/.env`
- 🔒 该文件已加入 `.gitignore`，不会提交到 Git
- 🔒 不在日志中明文显示完整 Key
- ⚠️ 不要将 `.env` 文件分享给他人
- ⚠️ 定期轮换敏感凭据（建议 90 天）

## 目录结构

```
coding-plan-assistant/
├── SKILL.md           # 技能说明
├── index.js           # 主程序入口
├── config.json        # 平台配置
├── package.json       # NPM 配置
├── README.md          # 本文件
├── .gitignore         # Git 忽略配置
├── scripts/           # 辅助脚本
│   ├── check-status.js
│   ├── rotate-key.js
│   └── compare-pricing.js
└── references/        # 官方文档链接
    ├── github-copilot.md
    ├── claude-code.md
    ├── gemini-cli.md
    ├── codex-openai.md
    ├── qwen-code.md
    ├── baidu-paddle.md
    └── openrouter.md
```

## 版本

- **1.0.0** (2026-03-27): 初始版本

## 许可证

MIT
