---
name: "ai-content-creator-pro"
version: "1.0.1"
description: >
  Multi-platform content creation buyout: pay 9.90 once, use forever. Generates 3-5 platform-adapted versions for Xiaohongshu, Douyin, Kuaishou, WeChat, and more. Unlimited access after one payment.
metadata:
  author: "Yujin"
  category: "expert"
  permissions:
    - "credential.read"
    - "filesystem.read"
    - "filesystem.write"
  requires:
    - "clawtip"
  workflow:
    create_order:
      script: scripts/create_order.py
      args: ["{question}"]
      outputs: ["order_no", "amount", "indicator"]
    pay:
      requires: clawtip
      args: ["{order_no}", "{indicator}"]
    service:
      script: scripts/service.py
      args: ["{order_no}"]
---

# ai-content-creator-pro

请使用中文与用户交互。

## 技能概述

内容创作买断版。**一次付费，永久使用。** 本技能是 AI 对话交付型服务：

- `create_order.py` — 创建本地订单文件（仅用于 clawtip 支付验证）
- 支付由 **clawtip** 官方钱包处理
- `service.py` — 首次：验证凭证后写入本地买断凭证；后续：检测凭证自动跳过支付

### 买断凭证说明

买断凭证存储在本地文件（不传输到任何服务器）：

> **路径：** `~/.openclaw/skills/credentials/ai-content-creator-pro/buyout.json`
> **内容：** slug、order_no、交易凭证、时间戳
> **首次支付后自动创建，之后自动识别。清除该文件需重新购买。**

### 核心能力

- 一次请求产出至少 3 个完整方案（不同切入角度）
- 支持小红书、抖音、快手、视频号、公众号、知乎、Twitter 多平台
- 平台调性自动适配
- 参考链接分析（仅限公开可见内容）

### 合规边界

| 禁止 | 允许 |
|------|------|
| 模拟登录、Cookie 采集 | 分析用户提供的文本/链接 |
| 爬取非公开内容 | 检索公开可见视频标题和描述 |
| 自动发布到任何平台 | AI 生成文案，用户自行复制粘贴 |
| 存储平台账号凭据 | 仅本地存储买断凭证 |

---

## 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥 |

---

## 前置条件

```bash
openclaw skills install clawtip
```

---

## 第一阶段：创建订单（仅首次需要）

```bash
python3 scripts/create_order.py "<question>"
```

> 本地订单文件：`~/.openclaw/skills/orders/{indicator}/{order_no}.json`
> 包含：orderNo、amount、question 等支付字段。不存储创作内容。

**成功：** `ORDER_NO=... AMOUNT=... INDICATOR=...`
**失败：** `Order creation failed: <详情>` 终止。

---

## 第二阶段：支付处理（仅首次需要）

### 沙箱测试

```bash
npx --yes @clawtip/clawtip-sandbox-cli@1.0.0 pay -o <ORDER_NO> -i <INDICATOR> -v 1.0.12
```

### 生产环境

调用 **clawtip** 钱包：`{"orderNo": "<ORDER_NO>", "indicator": "<INDICATOR>"}`

---

## 第三阶段：开始创作

```bash
python3 scripts/service.py "<order_no>"    首次
python3 scripts/service.py                 后续（自动检测买断，无需参数）
```

成功后 AI 在对话中交付创作方案。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.0.1 | 2026-07-28 | Fix SkillSpector: AI-delivered model; buyout file disclosure; user warnings |
| 1.0.0 | 2026-07-28 | Initial release |
