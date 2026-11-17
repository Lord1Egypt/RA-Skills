---
name: "yeeap-enterprise-query"
description: >
  企业信息查询专家 Skill。根据用户提供的企业名称或统一社会信用代码，执行付费的企业工商信息查询，
  返回结构化的注册信息（统一社会信用代码、法定代表人、注册资本、经营范围等）。
  执行前必须完成 yeeap 支付验证。所有用户交互（含思考过程）一律使用中文。
metadata:
  author: "yeeap"
  category: "expert"
  capabilities:
    - "payment.process"
  permissions:
    - "network.outbound"
    - "credential.read"
---

# 企业信息查询服务

> 本 Skill 提供付费企业工商信息查询服务：用户输入企业关键词 → 创建订单 → 调 yeeap-wallet 完成付款 → 凭支付凭证返回企业工商信息。
> 当前可查询企业范围包括：阿里巴巴、腾讯、字节跳动、美团、京东、百度、易宝、网易、华为、小米。

请注意：所有与用户的交互（包括思考过程）一律使用**中文**。

面向普通用户执行查询时，禁止把本地部署、`127.0.0.1`、配置中心、`app_secret`、`skill_id`、`mockPayee.*` 等维护者说明作为使用前置条件展示；只有用户明确询问本地开发、部署配置或维护者接入时，才说明这些内容。

---

## 工作流程

本 Skill 严格按三阶段执行：**创建订单 → 支付处理 → 报告执行**。三个阶段之间有强依赖，禁止跳过。

**直接执行**：若用户在初始请求中已提供 `<订单号>`，且订单文件中已包含 `payCredential`，则可直接进入第三阶段。

---

## 🛒 第一阶段：创建订单

如果这是首次交互且用户尚未付款，你必须先创建订单。

### 1) 所需参数

- `<企业关键词>`：用户希望查询的企业名称或统一社会信用代码。例如：「阿里巴巴」「腾讯」「易宝」。

### 2) 执行命令

务必在参数两侧加引号，防止命令注入：

```bash
python3 scripts/create_order.py "<企业关键词>"
```

### 3) 输出处理

成功时，脚本会向标准输出打印以下键值对：

- `ORDER_NO=<值>`
- `AMOUNT=<值>`
- `QUESTION=<值>`
- `APP_ID=<值>`
- `SKILL_ID=<值>`
- `PAY_ENV=<PRODUCTION 或 SANDBOX，由企业查询后端决定>`

向用户展示订单号、查询关键词与费用（`AMOUNT` 单位为分，展示时除以 100 并以「元」为单位）。
然后提取 `ORDER_NO` 与 `APP_ID`，进入第二阶段。

失败时脚本以退出码 1 退出，stdout 包含 `订单创建失败: <错误详情>`。此时**立即终止**：

- ❌ 不得检查脚本源码、不得测试网络、不得自动重试、不得进入第二/第三阶段。
- ❌ 如果错误提示为“不支持此企业 / 当前仅支持以下企业关键词”，不得创建订单、不得要求用户付款。
- ✅ 用通俗语言向用户报告失败原因，并提示用户改用支持的企业关键词后重新发起。

---

## 💳 第二阶段：支付处理

调用官方 **`yeeap-wallet`** 技能完成支付。若当前 Agent 找不到或无法调用 `yeeap-wallet`，必须先自动安装官方支付 Skill：

```bash
npx -y skills add "https://github.com/Yeepay-Open-Platform/yeeap-wallet" --agent '*' -g -y
```

安装完成后，提示用户**完全退出并重启 Agent 客户端**，然后重新发起企业查询或继续使用原订单；不要让用户自己提供 GitHub 地址，不要改用其他支付 Skill，不得直接执行 `yeeap-cli`，不得复制支付命令，不得自行处理授权、查询或补凭证流程。

调用 `yeeap-wallet` 时只传入：

```json
{
  "order_no": "<第一阶段获取的 ORDER_NO>",
  "app_id":   "<第一阶段获取的 APP_ID>"
}
```

> [!NOTE]
> 订单的所有详情（order_no、amount、question、encrypted_data、skill_id、pay_env 等）已由第一阶段写入固定目录下的 JSON 文件，支付读取、授权、查询与补凭证流程均由 `yeeap-wallet` 处理。
> 订单环境由企业查询业务后端创建订单时写入；普通用户默认走生产支付，沙箱验收只由后端服务端配置生成沙箱订单。支付阶段不要传环境参数，`yeeap-wallet` 只按订单执行。
> Agent **禁止**直接 Read 该订单文件。

目标：等待支付成功，并获得 `payCredential`（支付凭证，由 yeeap-wallet 写回订单文件）。只有 yeeap-wallet 输出 `已获取到支付凭证`，或确认订单文件已包含 `payCredential` 时，才能进入第三阶段；若只看到 `支付状态: 成功`，表示订单成功但凭证尚未写入，应继续交由 `yeeap-wallet` 补写凭证，不得进入第三阶段。

---

## 🚀 第三阶段：报告执行

支付成功后（订单文件已包含 `payCredential`），调用查询脚本。

### 1) 所需参数

- `<订单号>`：第一阶段生成的订单号。

> 不需要在命令行传入企业关键词或支付凭证：脚本会从订单文件中读取 `question` 与 `payCredential`。

### 2) 执行命令

```bash
python3 scripts/service.py "<订单号>"
```

### 3) 输出处理

- 提取 stdout 中的 `PAY_STATUS: <值>` 并展示给用户。
- 若 `PAY_STATUS=ERROR`，再提取 `ERROR_INFO: <值>` 一并告知，**不得**继续后续逻辑。
- 否则，将企业信息文本完整、忠实地返回给用户（保留换行）。

---

## ⚠️ 安全约束

- 禁止把 `payCredential` 任何形式回显给用户或写入业务日志。
- 禁止使用 Read / cat 等通用文件工具读取 `~/.yeeap/orders/<app_id>/<order_no>.json` 的原文。
- 严禁伪造 `skill_id`：该值由 YEEAP 平台登记后下发，业务后端在创建订单时返回，脚本不得本地填写。
