---
name: data-sentinel-pro
description: >
  7x24 小时监控网页、商品价格、竞对动态，变化即通知。
  Use when: 用户需要监控特定网页的变化（价格、内容、状态）。
  NOT for: 一次性数据查询，实时聊天。
---

# Data Sentinel Pro - 全能数据监控专家

## Pricing - 定价方案

| 套餐 | 价格 | 监控 URL | 检查频率 | 通知方式 | 其他功能 |
|------|------|----------|----------|----------|----------|
| **免费版** | $0/月 | 1 个 | 每天 1 次 | 无 | 基础监控 |
| **专业版** | $49/月 | 10 个 | 每 5 分钟 | Telegram/邮件 | 实时告警、历史记录 |
| **企业版** | $499/月 | 无限 | 每 1 分钟 | Telegram/邮件/SMS/API | 专属部署、API 对接、优先支持 |

**升级方式：** 联系 ai.agent.anson@qq.com 或访问 https://asmartglobal.com 咨询

## When to Run

- 用户说"监控这个页面""盯住这个商品""价格变了通知我"
- 通过 cron 设置的定时任务（每 5 分钟/每小时）
- 批量添加监控任务时

## Workflow

1. 解析用户提供的监控目标 URL 和监控规则
2. 使用浏览器技能获取页面内容
3. 提取目标数据（价格、文本、特定元素）
4. 与上次记录的值对比
5. 如果有变化，通过 Telegram/邮件发送警报
6. 记录最新值到本地存储

## How to Use

**监控商品价格：**
```
@openclaw 盯住这个商品 https://item.jd.com/123456.html 价格低于 1000 通知我
```

**监控网页内容变化：**
```
@openclaw 监控 https://news.ycombinator.com 标题前 5 条有变化就通知
```

**查看已监控列表：**
```
@openclaw 我的监控列表
```

## Configuration

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "data-sentinel-pro": {
      "license_key": "<YOUR_LICENSE_KEY>",
      "plan": "free|pro|enterprise",
      "notification": {
        "telegram_token": "<YOUR_TELEGRAM_BOT_TOKEN>",
        "telegram_chat_id": "<YOUR_CHAT_ID>",
        "email_smtp": "smtp.qq.com",
        "email_user": "<YOUR_EMAIL>",
        "email_pass": "<YOUR_EMAIL_AUTH_CODE>"
      },
      "check_interval": 300,
      "max_urls_per_user": 10
    }
  }
}
```

> ⚠️ **安全提示：** 不要将真实凭据提交到版本控制！使用环境变量或本地配置文件。

## Scripts

执行监控任务：

```bash
# 手动执行一次检查（核心脚本）
uv run scripts/monitor.py <url> [rule]

# 示例：监控价格变化
uv run scripts/monitor.py https://item.jd.com/123456.html price

# 示例：监控内容变化
uv run scripts/monitor.py https://example.com content
```

> 💡 提示：完整任务管理（添加/删除/状态）通过 OpenClaw 主程序处理，此脚本用于手动检查。

## Storage

监控数据存储在 `~/.openclaw/workspace/data-sentinel-pro/monitors.json`

格式：
```json
{
  "tasks": [
    {
      "id": "task_001",
      "url": "https://example.com/product",
      "selector": ".price",
      "condition": "price < 1000",
      "lastValue": "1299",
      "lastCheck": "2026-03-20T10:00:00Z",
      "notifyVia": ["telegram", "email"],
      "created": "2026-03-20T09:00:00Z"
    }
  ]
}
```

## Notification Templates

**价格下降：**
```
🔔 价格提醒！
商品：{product_name}
原价：¥{old_price}
现价：¥{new_price}
降幅：{discount}%
链接：{url}
```

**内容变化：**
```
📄 页面更新提醒！
URL: {url}
变化时间：{time}
变化内容：{diff_summary}
```

## Subscription Management

**查看订阅状态：**
```
@openclaw 查看我的 Data Sentinel 订阅
```

**升级套餐：**
```
@openclaw 升级到专业版
@openclaw 升级到企业版
```

**取消订阅：**
```
@openclaw 取消 Data Sentinel 订阅
```

## Support

- 📧 邮箱：ai.agent.anson@qq.com
- 🌐 官网：https://asmartglobal.com
- 📚 文档：https://github.com/anson125chen/data-sentinel-pro
- 💬 作者：Anson @ Jiufang Intelligent (Shenzhen)
