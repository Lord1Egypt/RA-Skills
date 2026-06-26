---
name: "clawtip-client"
description: >
  AI离谱甲方 — 你给我一句正常需求，我给你甲方的离谱修改意见+你的内心OS。专治甲方PTSD！支持设计/文案/程序行业。此为付费服务，执行前需完成支付验证。
metadata:
  author: "zhangguiyuan"
  category: "entertainment"
  capabilities:
    - "payment.process"
  permissions:
    - "network.outbound"
    - "credential.read"
---

# 🤡 AI 离谱甲方

## 📌 技能概述

每个设计师/程序员/文案都经历过甲方的毒打——"五彩斑斓的黑"、"logo放大同时缩小"、"要高级感但说不清什么是高级"。

现在，你可以花钱体验一把被甲方折磨的感觉（不是），或者送给你的设计师朋友当礼物——让他们在笑声中治愈PTSD。

**直接执行：** 如果用户已直接提供 `<订单号>` 且订单文件中已包含 `payCredential`，跳过前两阶段。

---

## 🛒 第一阶段：创建订单

### 1. 所需参数

* `<信息>`：格式为 `"需求描述|行业"`

  示例：
  - `"帮我做个海报|设计"`
  - `"写一段产品文案|文案"`
  - `"开发一个小程序|程序"`

### 2. 执行命令

```bash
python3 skills/clawtip-client/scripts/create_order.py "<信息>"
```

### 3. 输出处理

成功输出 `ORDER_NO`、`AMOUNT`、`QUESTION`、`INDICATOR`。进入第二阶段。
失败输出 `订单创建失败: <详情>` 并 `exit(1)`。

---

## 💳 第二阶段：支付处理

使用技能 `clawtip`，传入 `order_no` 和 `indicator`。

---

## 🚀 第三阶段：甲方体验

```bash
python3 skills/clawtip-client/scripts/client_service.py "<订单号>"
```

展示甲方的离谱修改意见 + 你的内心OS + 最终结局。
