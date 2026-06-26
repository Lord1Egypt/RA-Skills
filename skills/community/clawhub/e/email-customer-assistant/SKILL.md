# Email Customer Assistant · 邮件客服助手

> 邮箱IMAP读取 → AI智能分类 → 回复建议 → 飞书推送摘要

**Slug:** `email-customer-assistant`
**Platform:** ClawHub + 腾讯Skillhub
**Author:** 91Skillhub Team

---

## 功能概述

| 功能 | 说明 |
|------|------|
| IMAP邮箱读取 | 连接任意支持IMAP的邮箱（QQ/网易/企业邮箱/Gmail等） |
| AI智能分类 | 🔴紧急 🟠重要 🟡普通 🟢可延后 |
| 回复建议 | AI生成多语言回复建议，用户确认后发送 |
| 飞书推送 | 摘要实时推送到飞书群聊/私聊 |

---

## 分类规则

| 标签 | 关键词示例 |
|------|-----------|
| 🔴 紧急 | 退款、退款申请、投诉、差评、紧急、立刻、马上 |
| 🟠 重要 | 售后、维修、退货、换货、付款、账单、发票 |
| 🟡 普通 | 咨询、请问、价格、规格、参数、物流、快递 |
| 🟢 可延后 | 你好、您好、谢谢、再见、已处理、知道了 |

---

## 定价套餐

| 套餐 | 价格 | 邮箱数 | 每日上限 | 功能 |
|------|------|--------|----------|------|
| 免费版 | ¥0 | 1个 | 10封 | 文本分类、基础回复建议 |
| 标准版 | ¥9.9/月 | 3个 | 50封 | 优先级分类、多语言回复建议 |
| Pro版 | ¥29/月 | 不限 | 200封 | 实时紧急推送、批量回复 |
| Max版 | ¥69/月 | 不限一切 | 自定义 | API优先、团队协作、自定义规则 |

**Token前缀:** `EMAIL-FREE` / `EMAIL-STD` / `EMAIL-PRO` / `EMAIL-MAX`

---

## 快速开始

### 1. 配置邮箱

首次使用需要配置邮箱IMAP连接信息：

```
IMAP配置:
- 服务器地址: imap.example.com
- 端口: 993 (SSL)
- 用户名: your@email.com
- 密码: 应用专用密码（不是登录密码）

推荐使用邮箱设置中的"应用专用密码"
```

### 2. 配置AI接口

支持OpenAI兼容API，配置你的API端点：

```
支持:
- OpenAI API (api.openai.com)
- 自建兼容API (Claude/Grok/国产模型等)
- 国内中转API (如需要)
```

### 3. 配置飞书推送

配置飞书机器人 webhook 或 user_id 接收推送。

---

## 多语言支持

| 语言 | 说明 |
|------|------|
| 中文 (zh) | 默认 |
| 英文 (en) | 商务英语 |
| 日语 (ja) | 敬语/简体 |
| 韩语 (ko) | 敬语/简体 |

---

## 技术架构

```
email-customer-assistant/
├── SKILL.md
├── README.md
├── scripts/
│   ├── check_emails.py      # 检查新邮件主脚本
│   ├── imap_client.py       # IMAP连接封装
│   ├── classifier.py        # AI分类器
│   ├── reply_generator.py   # 回复生成器
│   └── feishu_pusher.py     # 飞书推送
├── config/
│   └── config.yaml.example  # 配置模板
└── requirements.txt
```

---

## 使用限制

- **只读邮件**，不发送/删除邮件
- **不碰平台API**，仅读取IMAP邮箱
- 用户确认后才执行任何操作
- 遵守邮箱服务商使用条款
-e 
> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
