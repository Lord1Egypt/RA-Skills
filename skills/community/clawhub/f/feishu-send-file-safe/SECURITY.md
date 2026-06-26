# 安全指南

## 概述

本 skill 处理敏感的飞书 API 凭证。请遵循以下安全最佳实践。

## 安全特性

### 1. 配置分离

- `config.json` 包含敏感凭证，已被添加到 `.gitignore`
- 提供 `config.json.example` 作为配置模板
- 用户需自行创建 `config.json`

### 2. 环境变量支持

所有脚本优先从环境变量读取配置：

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_RECEIVE_ID="ou_xxx"
```

### 3. 无硬编码凭证

- 所有脚本均从外部配置读取凭证
- 无硬编码的 API key、token 或用户 ID

## 使用建议

### 不要提交 config.json

```bash
# 确认 config.json 被忽略
git status
# 不应看到 config.json
```

### 使用环境变量（推荐）

适合 CI/CD 或临时使用，不留下持久化凭证。

### 保护你的凭证

- 不要分享 `app_secret`
- 定期轮换凭证
- 使用最小权限原则配置飞书应用

## 报告安全问题

如发现安全漏洞，请通过 GitHub Issues 私下报告。

---

**安全状态**: ✅ 已审计，适合开源发布
