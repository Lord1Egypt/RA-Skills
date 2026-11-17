---
name: "ai-content-creator-assistant"
version: "1.1.0"
description: >
  Multi-platform content creation: generates 3-5 platform-adapted versions for Xiaohongshu, Douyin, Kuaishou, WeChat, and more. AI-delivered service via clawtip payment verification. No cookies, no auto-posting, no scraping of private data. Reference link analysis limited to publicly visible content.
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

# ai-content-creator-assistant

请使用中文与用户交互。

## 技能概述

本技能根据用户提供的主题或参考素材，**一次生成多套完整方案**（至少 3 个不同角度的版本），再让用户从中挑选最终方案。支持多平台调性适配，AI 内置各平台的写作规则。

### 服务交付方式

本技能是 **AI 对话交付型** 服务：
- `create_order.py` — 创建本地订单文件（仅用于 clawtip 支付验证）
- 支付由 **clawtip** 官方钱包处理
- `service.py` — 验证支付凭证后，指示 AI 在对话中交付创作方案

### 核心能力

| 能力 | 说明 |
|------|------|
| 多方案交付 | 一次请求产出至少 3 个完整方案（标题+正文+标签），切入角度不同 |
| 平台调性适配 | AI 内置各平台写作规则（小红书、抖音、快手、视频号、公众号、知乎、Twitter） |
| 参考素材分析 | 支持链接分析，仅检索视频标题、描述等**公开可见文本** |
| 批量生成 | 单主题支持同时生成多平台版本 |

### 合规边界（不可执行行为）

| ❌ 禁止 | ✅ 允许 |
|---------|---------|
| 模拟登录、Cookie 采集 | 分析用户提供的文本/链接 |
| 爬取非公开内容（播放量、点赞数、用户信息） | 检索公开可见的视频标题和描述 |
| 自动发布到任何平台 | AI 生成文案，用户自行复制粘贴 |
| 存储平台账号凭据 | 仅存储本地订单文件（clawtip 支付所需） |

### 定价

- 单次生成：190 UT（¥1.90/次）

> 💡 **高频用户推荐：** 另有 **ai-content-creator-pro** 买断版（¥9.90），\
> 一次付费永久使用，不限次数。\
> 安装：`openclaw skills install @jinyu12166/ai-content-creator-pro`

### 用户交互示例

| 用户输入 | 输出 |
|----------|------|
| "帮我写一篇小红书文案，主题是XX产品" | 3 个不同角度的小红书笔记方案 |
| "参考这个链接的风格，帮我生成抖音脚本" | 分析链接公开信息 + 适配的脚本 |

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

## 🛒 第一阶段：创建订单

```bash
python3 scripts/create_order.py "<question>"
```

> 本地订单文件：`~/.openclaw/skills/orders/{indicator}/{order_no}.json` |
> 包含 orderNo、amount、question 等支付验证字段。不存储任何创作内容或平台凭据。

**成功：** `ORDER_NO=... AMOUNT=... QUESTION=... INDICATOR=...`
**失败：** `Order creation failed: <详情>` → 终止。

---

## 💳 第二阶段：支付处理

### 沙箱测试

```bash
npx --yes @clawtip/clawtip-sandbox-cli@1.0.0 pay -o <ORDER_NO> -i <INDICATOR> -v 1.0.12
```

### 生产环境

调用 **clawtip** 钱包：`{"orderNo": "<ORDER_NO>", "indicator": "<INDICATOR>"}`

---

## 🚀 第三阶段：内容创作

```bash
python3 scripts/service.py "<order_no>"
```

成功后 AI 将在对话中交付多套创作方案。

---

## 数据处理说明

### 本地存储
| 文件 | 路径 | 内容 |
|------|------|------|
| 订单文件 | `~/.openclaw/skills/orders/{indicator}/{order_no}.json` | orderNo、amount、question 等支付验证字段 |

### 远程传输
本技能自身不发起任何远程 HTTP 请求。支付验证由 clawtip 官方钱包处理。

### 绝不收集或传输
平台账号 Cookie、Token、API Key、用户原始素材内容、生成的文案内容。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.1.0 | 2026-07-28 | Rebuild per BUILD_STANDARD: inline SM4/file_utils; compliance boundary defined; AI-delivered service model |
| 1.0.0 | 2026-07-27 | Initial release |
