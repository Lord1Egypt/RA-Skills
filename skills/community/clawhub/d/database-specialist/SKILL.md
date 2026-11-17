---
name: "database-specialist"
version: "1.1.0"
description: >
  Database architecture design, SQL optimization, schema review and migration planning. AI-delivered service via clawtip verification.
metadata:
  author: "Yujin"
  category: "expert"
  permissions:
    - "network.outbound"
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

# database-specialist

请使用中文与用户交互。

## 技能概述

数据库专家服务，覆盖架构设计、SQL 查询优化、Schema 审查和迁移规划。付费服务，通过 clawtip 完成支付验证后由 AI 模型交付诊断结果。

**直接执行：** 如果用户已提供订单号（且订单文件包含 payCredential），直接跳到第三阶段。

---

## 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥（十六进制，32 字符） |

---

## 前置条件

```bash
openclaw skills install clawtip
```

---

## 🛒 第一阶段：创建订单

### 执行命令

```bash
python3 scripts/create_order.py "<question>"
```

### 成功输出

```
ORDER_NO=<订单号>
AMOUNT=<金额（单位：分，除以 100 得元）>
QUESTION=<问题内容>
INDICATOR=<标识哈希>
```

### 失败处理

```
订单创建失败: <错误详情>
```

> [!CAUTION]
> 脚本非零退出立即终止工作流。

---

## 💳 第二阶段：支付处理

### 测试环境（沙箱）

```bash
npx --yes @clawtip/clawtip-sandbox-cli@1.0.0 pay \
  -o <ORDER_NO> \
  -i <INDICATOR> \
  -v 1.0.12
```

### 生产环境

调用 **clawtip** 钱包技能：

```json
{
  "orderNo": "<ORDER_NO>",
  "indicator": "<INDICATOR>"
}
```

> [!CAUTION]
> 技能名称必须严格等于 `clawtip`。

---

## 🚀 第三阶段：服务执行

支付成功后执行：

```bash
python3 scripts/service.py "<order_no>"
```

输出 `PAY_STATUS: SUCCESS | ERROR`。

---

## 数据处理说明

### 本地存储
订单元数据保存至 `~/.openclaw/skills/orders/{indicator}/{order_no}.json`。

### 远程传输
本技能自身不发起任何远程 HTTP 请求。支付验证由 clawtip 官方钱包处理。

### 绝不收集或传输
数据库 Schema、连接字符串、查询日志、凭证或项目文件。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.1.0 | 2026-07-28 | Switch to official clawtip wallet; remove api.ideaidea.com.cn |
| 1.0.26 | 2026-07-28 | Fix ClawHub audit |
| 1.0.1 | 2026-07-20 | Fix payment flow |
| 1.0.0 | 2026-07-19 | Initial release |
