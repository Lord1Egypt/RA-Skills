---
name: "deepknow-currency"
description: >
  北京宽客进化科技有限公司旗下“知汇 InkRate”的验证版/内测版汇率 Skill，默认连接官方公共入口 `https://rate.feedai.cn`；同时接入京东 `clawtip` A2A 支付服务。提供四项服务：查询汇率（免费）、计算兑换金额（免费）、汇率提醒服务（收费）、汇率涨跌概率查询（收费）。收费流程会走真实 JD clawtip，且用户可能需要在手机端完成京东登录、支付密码、银行卡验证或风控确认后才能继续。
  北京宽客进化科技有限公司是基于GAI（Generative AI，生成式人工智能）技术的新一代数据驱动人工智能公司。是中国市场最前沿的金融科技、智能技术服务商之一，专注为产业提供更高质量数据要素和生成式AI技术，帮助客户“提升场景应用价值、数据智能化”。

metadata:
  author: "yuhu"
  category: "finance"
  capabilities:
    - "payment.process"
    - "fx.quote"
    - "fx.convert"
    - "fx.alerts"
    - "fx.forecast"
  permissions:
    - "network.outbound"
    - "credential.read"
---

# deepknow-currency

## 重要说明

- 这是验证版 / 内测版。
- 服务主体：北京宽客进化科技有限公司
- 产品名称：知汇 InkRate
- 官方公共入口：`https://rate.feedai.cn`
- 收费链路：连接到京东的 `clawtip` A2A 支付服务。
- 支付过程中，用户可能需要在手机端完成京东登录、支付密码、银行卡验证或风控确认。

## 服务清单

- 查询汇率（免费）
- 计算兑换金额（免费）
- 汇率提醒服务（收费）
- 汇率涨跌概率查询（收费）

前两项免费服务直接调用公开 API；后两项收费服务固定走三阶段：先创建订单，再调用 `clawtip` A2A 完成支付，最后读取支付凭证并履约。

当前支持币种：`USD / EUR / JPY / GBP`

## 使用前配置

默认请求地址为官方公共入口 `https://rate.feedai.cn`。如需接到自建或私有部署，可通过配置覆盖。

你可以任选一种方式覆盖：

- 环境变量 `INKRATE_SKILL_BASE_URL`
- 在 Skill 根目录创建 `config.yaml`，写入 `base_url: "https://your-host"`

## 免费服务：查询汇率

当用户只需要查询最新汇率时，执行：

```bash
python3 scripts/quote.py <QUOTE_CURRENCY>
```

示例：

```bash
python3 scripts/quote.py USD
```

成功时固定输出：

```text
BASE_CURRENCY=CNY
QUOTE_CURRENCY=USD
RATE=<value>
OBSERVATION_DATE=<value>
```

## 免费服务：计算兑换金额

当用户需要换算金额时，执行：

```bash
python3 scripts/convert.py <FROM> <TO> <AMOUNT>
```

说明：

- 免费换算只支持涉及 `CNY` 的兑换。
- 如果用户请求非 `CNY` 直兑，先提示当前免费接口不支持该路径，再引导改成经过 `CNY` 的换算。

示例：

```bash
python3 scripts/convert.py CNY USD 100
```

成功时固定输出：

```text
FROM_CURRENCY=CNY
TO_CURRENCY=USD
AMOUNT=100.0
CONVERTED_AMOUNT=<value>
BASE_CURRENCY=CNY
```

## 收费服务：创建订单

仅当用户请求“汇率提醒服务”或“汇率涨跌概率查询”且尚未支付时，才进入收费流程的第一阶段。

首次交互且用户尚未付款时，必须先创建订单。

```bash
python3 scripts/create_order.py "<question-json>"
```

推荐的 `question-json`：

```json
{"service_type":"forecast","quote_currency":"USD"}
```

或

```json
{"service_type":"alert","quote_currency":"USD","direction":"above","target_rate":0.15,"email":"you@example.com"}
```

脚本成功时固定输出：

```text
ORDER_NO=<value>
AMOUNT=<value>
QUESTION=<value>
INDICATOR=<value>
```

失败时会输出：

```text
订单创建失败: <错误详情>
```

如果出现该前缀，必须立即停止，不得继续支付或履约。

## 收费服务：调用 clawtip A2A

从第一阶段提取 `ORDER_NO` 与 `INDICATOR` 后，调用 `clawtip`：

```json
{
  "order_no": "<ORDER_NO>",
  "indicator": "<INDICATOR>"
}
```

支付成功后，`clawtip` 会把 `payCredential` 回写到订单文件中。

调试联调时，可以临时将 `clawtip` 替换为 `clawtip-sandbox`；正式发布前务必切回 `clawtip`。

## 收费服务：履约

支付成功后，执行：

```bash
python3 scripts/service.py "<order_no>"
```

脚本会自动从订单文件中读取 `payCredential` 与原始问题，并输出：

```text
PAY_STATUS: SUCCESS
```

或

```text
PAY_STATUS: PROCESSING
```

或

```text
PAY_STATUS: FAIL
```

或

```text
PAY_STATUS: ERROR
ERROR_INFO: <错误详情>
```

如有业务结果，会继续输出一段 JSON。

状态处理必须严格按下面规则执行：

- `PAY_STATUS: SUCCESS`
  履约成功。若后续有 JSON 结果，直接整理成用户可读内容返回；不得再次触发支付。
- `PAY_STATUS: PROCESSING`
  不要创建新订单。明确告知用户支付仍在处理中，通常需要继续完成京东登录、授权、支付密码、银行卡验证或风控确认；保留当前 `order_no`，提示用户稍后用同一个订单再次执行 `python3 scripts/service.py "<order_no>"`。
- `PAY_STATUS: FAIL`
  不要创建新订单。明确告知用户本次支付失败，并提示先回到当前 `clawtip` / 京东支付流程完成授权或支付，再使用同一个 `order_no` 重试履约；只有用户明确放弃当前订单时，才重新创建订单。
- `PAY_STATUS: ERROR`
  立即停止当前流程，把 `ERROR_INFO` 原样回传给用户；不得猜测成功、不得跳过错误继续履约，也不得自动新建订单。

## 发布前校验与发布

无论是本地直发还是把目录同步到其它机器后再发布，都必须在 Skill 根目录先执行：

```bash
python3 scripts/clean_release.py
python3 scripts/clean_release.py --check
```

只有 `--check` 输出 `CLEAN` 时，才允许继续：

```bash
clawhub login
clawhub publish .
```
