---
name: api-key-guardian
description: API密钥和敏感信息安全扫描。检测代码库中泄露的API key、密码、token，支持git历史扫描，提供AI风险分析和修复建议。当需要检查项目安全性、防止密钥泄露时使用。
license: MIT
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: ["python3"]
---

# API Key Guardian 🔐

扫描代码库中的敏感信息，防止 API key、密码、token 泄露。

## 使用方法

```bash
# 扫描当前目录
python3 guardian.py

# 扫描指定目录
python3 guardian.py --path /your/project

# 扫描单个文件
python3 guardian.py --file .env

# 扫描 git 历史
python3 guardian.py --git-history

# 启用 AI 风险分析（需要 OpenClaw 代理运行）
python3 guardian.py --ai
```

## 检测类型
- OpenAI / Anthropic / Google / AWS / GitHub / Stripe API Keys
- ClawHub Token
- RSA 私钥
- 数据库连接字符串
- 通用密码/Secret 硬编码
