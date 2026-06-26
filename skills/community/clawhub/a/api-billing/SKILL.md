---
name: api-billing
description: API账户余额与历史账单查询工具。支持火山引擎、阿里云、DeepSeek、MiniMax、OpenRouter等平台的余额查询和历史账单功能。用于查询各平台账户余额、订阅用量、历史消费记录。
---

# API 账户账单查询工具

## 概述

此技能提供多个平台的余额查询和历史账单功能，帮助追踪API使用费用。

## 功能

- **火山引擎**: 余额查询 + 历史账单（近6个月）
- **阿里云**: 余额查询 + 历史账单
- **DeepSeek**: 余额查询
- **MiniMax**: Coding Plan 用量查询
- **OpenRouter**: 余额查询

## 凭证配置

所有凭证文件存放在 `~/.openclaw/workspace/` 目录：

| 文件 | 用途 |
|------|------|
| `.volc_ak_sk.env` | 火山引擎 AccessKey/SecretKey |
| `.aliyun_ak_sk.env` | 阿里云 AccessKey/SecretKey |
| `.minimax_cp_key.env` | MiniMax Coding Plan API Key |
| `.deepseek_key.env` | DeepSeek API Key |
| `.openrouter_key.env` | OpenRouter API Key |

## 使用方法

```bash
# 火山引擎（余额 + 历史账单）
python3 skills/api-billing/scripts/query_volc_billing.py
python3 skills/api-billing/scripts/query_volc_billing.py --history

# 阿里云
python3 skills/api-billing/scripts/query_aliyun_balance.py

# DeepSeek
python3 skills/api-billing/scripts/query_deepseek_balance.py

# MiniMax
python3 skills/api-billing/scripts/query_minimax_plan.py

# OpenRouter
python3 skills/api-billing/scripts/query_openrouter_balance.py
```

## 敏感信息保护

- 凭证文件使用 Base64 编码存储
- 文件权限设为 600（仅自己可读写）
- 已加入 .gitignore，不会提交到 GitHub
