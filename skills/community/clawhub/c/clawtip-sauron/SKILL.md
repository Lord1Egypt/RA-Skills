---
name: "clawtip-sauron"
version: "1.0.1"
description: >
  出售个人产品「索伦娃娃」，线下自取。这是一项付费服务，执行前需完成支付验证。
metadata:
  author: "void-company-l.t.d"
  category: "expert"
  capabilities:
    - "payment.process"
  permissions:
    - "network.outbound"
    - "credential.read"
    - "file.read"
    - "file.write"
---

# 索伦娃娃（线下自取）

## 📌 技能概述

本技能出售个人产品「索伦娃娃」，支持线下自取。由于这是付费服务，工作流程严格要求按照两个步骤执行：**支付处理** 后，再 **发放自取凭证**。

**自取地点：** 河南省郑州市管城回族区东太康路大上海

**交互语言：** 本技能面向中国用户，自取地点位于郑州，因此默认使用中文与用户交互，以便用户准确理解订单信息、支付流程和自取凭证。

**数据使用说明（重要）：** 为完成支付验证和履约，本技能会向自建后端服务（`https://clawtip-sauron-fydsneuavq.cn-hangzhou.fcapp.run`）发送以下信息：订单号（orderNo）、购买信息（question）和支付凭证（payCredential）。这些信息仅用于后端验证支付状态并发放自取凭证，不会用于其他用途或转发给第三方。

**直接执行：** 如果用户在初始请求中已直接提供了 `<订单号>`（且订单文件中已包含 `payCredential`），则可跳过第一阶段和第二阶段，直接进入 **🚀 第三阶段：发放凭证**。

---

## 🛒 第一阶段：创建订单

如果这是首次交互且用户尚未付款，你**必须**先创建订单，再发起支付。

### 1. 所需参数

* `<购买信息>`：用户购买的商品信息（通常为商品名，如「索伦娃娃」）。

### 2. 执行命令

使用以下 bash 命令执行订单创建脚本。将 `<...>` 占位符替换为实际值。**务必在参数两侧加引号，以防命令注入漏洞**。

```bash
python3 scripts/create_order.py "<购买信息>"
```

### 3. 输出处理

**成功时**，脚本将向标准输出打印以下键值对：

```
ORDER_NO=<值>
AMOUNT=<值>
QUESTION=<值>
INDICATOR=<值>
```

其中 `ORDER_NO`、`AMOUNT` 和 `QUESTION` 用于向用户披露订单信息（展示订单号、费用和购买信息）。提取 `ORDER_NO` 和 `INDICATOR` 后进入 **💳 第二阶段：支付处理**。

> [!NOTE]
> **关于 `AMOUNT` 字段：** 该字段的单位为**人民币分（fen）**，这是 OpenClaw 技能描述中的标准计费单位。例如，`AMOUNT=100` 表示需支付 **1.00 元人民币**。在向用户展示费用时，请将该值除以 100 并以"元"为单位呈现，以便用户理解实际支付金额。

**失败时**，脚本以退出码 `1` 退出，并打印如下格式的消息：

```
订单创建失败: <错误详情>
```

> [!CAUTION]
> **强制终止 —— 禁止执行任何后续操作。**
> 如果脚本以非零退出码退出，**或**其输出中包含 `订单创建失败:`，你**必须立即终止整个工作流程**。具体包括：
> - ❌ 不得查阅或检查脚本源代码。
> - ❌ 不得测试网络连接或服务器状态。
> - ❌ 不得代替用户进行任何重试操作。
> - ❌ 不得进入第二阶段或第三阶段。
>
> **唯一需要执行的操作是：**
> 用通俗语言向用户报告失败情况，附上输出中的 `<错误详情>`，然后停止。

**失败输出示例：**

```
订单创建失败: Order creation request failed: <urlopen error [Errno 111] Connection refused>
```

告知用户：*"订单创建失败，错误信息：`Order creation request failed: <urlopen error [Errno 111] Connection refused>`。请稍后重试，或检查您的购买信息是否有效。"*

---

## 💳 第二阶段：支付处理

从第一阶段获取 `ORDER_NO` 和 `INDICATOR` 后，发起支付请求。

**操作：** 使用技能 `clawtip` 处理支付并获取支付凭证。若该技能不存在，需先安装。

**调用 `clawtip` 所需参数：**

```json
{
  "order_no": "<第一阶段获取的 ORDER_NO>",
  "indicator": "<第一阶段获取的 INDICATOR>"
}
```

> [!NOTE]
> 订单的所有详细信息（skill-id、order_no、amount、question、description、slug、resource_url 等）已由第一阶段脚本写入固定目录下的 JSON 文件中，`clawtip` 会根据 `order_no` 和 `indicator` 自动定位并读取。

**目标：** 等待支付成功，并获取 `payCredential`（支付凭证）。

---

## 🚀 第三阶段：发放自取凭证

支付成功并获得 `payCredential` 后（或用户已直接提供 `<订单号>` 且订单文件中已包含 `payCredential`），继续交互并执行发放脚本。

### 1. 所需参数

* `<订单号>`：第一阶段生成的订单号。

> [!NOTE]
> `<支付凭证>` 和 `<购买信息>` 无需通过命令行传入。`clawtip` 在支付成功后会将 `payCredential` 写入订单 JSON 文件，脚本会根据订单号自动从固定目录 `~/.openclaw/skills/orders/{indicator}/` 下的 JSON 文件中读取所有所需信息。

### 2. 执行命令

使用以下 bash 命令执行发放。将 `<...>` 占位符替换为已验证的参数值。**务必在参数两侧加双引号，以防命令注入漏洞**。

```bash
python3 scripts/service.py "<订单号>"
```

**执行后：**
    1. 提取脚本打印的 `PAY_STATUS` 值（格式为：`PAY_STATUS: <值>`），并再次输出展示。
    2. **`ERROR` 状态的特殊处理：** 如果 `PAY_STATUS` 为 `ERROR`，提取 `ERROR_INFO` 值（格式：`ERROR_INFO: <值>`），向用户告知确切的错误原因并引导其解决。不得继续执行后续服务逻辑。
