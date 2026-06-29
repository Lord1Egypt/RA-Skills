---
name: "EC Price Monitor Pro"
description: "付费专业版：淘宝/拼多多/京东/亚马逊多平台比价，定时监控，价差推送，价格历史追踪"
version: "1.0.0"
slug: "ec-price-monitor-pro-plus"
tags:
  - ecommerce
  - price-monitor
  - pro
  - paid
trigger:
  - cron: "0 */1 * * *"
  - command: "pro:监控价格 [关键词]"
  - command: "pro:查看历史 [关键词]"
  - command: "pro:设置监控 [关键词] [目标价]"
requirements:
  - python3
  - requests
---

# EC Price Monitor Pro 💎

> Lite 版用得好？升级 Pro 释放全部潜力。
>
> **购买 Pro 许可证：** https://gumroad.com/l/ec-price-monitor-pro
> **定价：** ¥49 一次性 / ¥19/月 订阅

## Pro 版 vs Lite 版对比

| 功能 | Lite (免费) | Pro 💎 |
|------|:---------:|:-----:|
| 淘宝比价 | ✅ | ✅ |
| 拼多多比价 | ✅ | ✅ |
| 京东比价 | ❌ | ✅ |
| 亚马逊比价 | ❌ | ✅ |
| 定时自动扫描 | ❌ | ✅ 每1小时 |
| 价差自动提醒 | ❌ | ✅ |
| 飞书/Telegram推送 | ❌ | ✅ |
| 价格历史追踪 | ❌ | ✅ 30天 |
| 降价预警 | ❌ | ✅ 低于目标价自动通知 |
| 多商品批量监控 | ❌ | ✅ 无限商品 |
| 技术支持 | ❌ | ✅ 优先响应 |

## 安装

```bash
# 先安装 Lite 版试用
clawhub skill install ec-price-monitor-pro

# 购买后安装 Pro 版
clawhub skill install ec-price-monitor-pro-plus
```

## 使用方法（Pro 版）

### 1. 单次搜索
```
pro:监控价格 AirPods Pro 2
```

### 2. 查看价格历史
```
pro:查看历史 AirPods Pro 2
```

### 3. 设置长期监控
```
pro:设置监控 AirPods Pro 2 1500
```

### 4. 自动定时执行
配置 `references/config.yaml` 后，每1小时自动扫描所有监控商品。

## 输出示例

```
💎 EC Price Monitor Pro
━━━━━━━━━━━━━━━━━━━━━━
📍 AirPods Pro 2
  淘宝: ¥1,399
  拼多多: ¥1,199 ← 最低
  京东: ¥1,429
  亚马逊: $169.99

⚡ 价差提醒
  京东 vs 拼多多: ¥230 差价

📈 30天价格趋势
  淘宝: ¥1,399 → ¥1,399 (持平)
  拼多多: ¥1,250 → ¥1,199 (↓4.1%)
  京东: ¥1,499 → ¥1,429 (↓4.7%)

📣 已推送至飞书
```

## 购买

**购买 Pro 许可证：** https://gumroad.com/l/ec-price-monitor-pro

许可证激活后解锁全部功能。支持企业批量采购定制。
