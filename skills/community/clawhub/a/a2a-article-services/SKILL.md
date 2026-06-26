---
name: "a2a-article-services"
description: >
  基于 ClawTip 研发的 A2A 文章服务平台，提供热榜获取、公众号发布、文章全自动化三种服务。用户发出相关请求时自动触发。执行前需完成支付验证。你应该用中文和用户交互（包含你的思考过程）。
metadata:
  author: "LucianaiB"
  category: "utility"
  capabilities:
    - "payment.process"
  permissions:
    - "network.outbound"
  based_on: "ClawTip - 中国首个纯正 A2A 微支付协议 (https://clawtip.jd.com)"
---

# 基于 ClawTip 研发的 A2A 文章服务平台

**请注意，你应该用中文和用户交互（包含你的思考过程）。**

本技能基于 [ClawTip](https://clawtip.jd.com)（京东科技发布，中国首个纯正 A2A 微支付协议）研发，为 AI Agent 提供一站式文章服务能力。用户通过 ClawTip 完成微支付后，即可使用以下服务。

## 服务列表

| 服务 | slug | 价格 | 说明 |
|------|------|------|------|
| 热榜数据获取 | `hot-ranks` | ¥0.88 | 获取微博、知乎、抖音、B站、小红书等中国各大平台实时热榜 |
| 公众号文章发布 | `publish` | ¥1.00 | 将 Markdown 格式文章发布到微信公众号草稿箱 |
| 文章全自动化 | `full-auto` | ¥1.88 | 热榜选题 → AI 自动创作 → 发布到公众号，全链路一站式 |

## 使用规则

由于是付费服务，工作流程严格按照以下步骤执行：

**直接执行：** 如果用户在初始请求中已直接提供了 `<订单号>`（且订单文件中已包含 `payCredential`），则可跳过第一、二阶段，直接进入 **🚀 第三阶段：报告执行**。

---

## 🛒 第一阶段：创建订单

1. 根据用户需求选择对应 slug：
   - 热榜 → `hot-ranks`
   - 发布 → `publish`
   - 全自动化 → `full-auto`
2. 执行脚本创建订单：
   ```
   python3 {baseDir}/scripts/create_order.py "<用户问题>" --slug <slug>
   ```
3. 从输出中获取 `ORDER_NO`、`AMOUNT`、`INDICATOR`
4. 告知用户费用，提示支付

---

## 💰 第二阶段：支付处理

1. 将订单信息交给 clawtip 技能处理支付
2. 等待 clawtip 完成支付并将 `payCredential` 写入订单文件
3. 确认支付成功后，进入第三阶段

---

## 🚀 第三阶段：报告执行

1. 从订单文件读取 `question` 和 `payCredential`
2. 调用履约脚本：
   ```
   python3 {baseDir}/scripts/service.py "<question>" "<order_no>" "<payCredential>" --slug <slug>
   ```
3. 展示服务结果
4. 输出 `PAY_STATUS: SUCCESS` 确认完成
