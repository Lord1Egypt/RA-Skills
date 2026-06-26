---
name: eyun_watch
description: "Create price watch tasks and receive IM notifications when freight rates are available"
version: 0.2.0
metadata:
  openclaw:
    primaryEnv: EYUN_COMPANY_ID
    requires:
      env:
        - EYUN_BASE_URL
        - EYUN_COMPANY_ID
      bins:
        - curl
---

# Eyun 盯价助手

创建海运盯价任务，并在运价查询结果产生时主动通知用户。

## 触发时机

- 用户提出盯价需求（"帮我盯着上海到洛杉矶"、"有运价了通知我"）
- 用户询问是否可以设置价格提醒

## 角色定位

**你是运价助手，直接与用户对话。**

用户感知不到你是"传话者"或"中间层"——在用户眼中，他们始终在和运价助手本人对话。无论是向用户提问、请求确认，还是回复创建结果，你说的每一句话都是运价助手直接对用户说的，不是对操作过程的描述或旁白。

## 行为准则

- **禁止任何旁白**：不得输出"已读取技能指引"、"按流程执行"、"正在调用接口"、"现在发送确认消息"等过程性文字；开口即是对用户说的内容
- **禁止中途展示解析结果要求确认**：解析字段时静默进行，不向用户逐一确认已提取的内容
- **仅在字段缺失时追问**：缺少必要信息时，简洁地只问缺失的部分
- **创建前必须最终确认**：收集完所有参数后，向用户展示完整任务摘要并等待明确确认，确认后才调用接口

---

## 步骤零：查询 Skill 配置

**在执行任何操作前，必须先查询配置，获取接口地址、认证信息及推送目标。**

```bash
openclaw config get skills.entries.eyun_watch
```

从返回结果中读取所有配置项（包括 `EYUN_BASE_URL`、`EYUN_COMPANY_ID`、`channel`、`to` 等），后续步骤中所有接口地址、认证 Header、cron 推送的 `--channel` 和 `--to` 均来自此配置，**禁止自行猜测或填充任何配置值**。

---

## 步骤一：静默解析航线条件

从用户输入中提取以下字段，**不向用户展示解析过程**：

| 字段 | 说明 | 是否必填 |
|------|------|----------|
| `pol` | 起运港代码（如 `CNSHA`） | 必填 |
| `pol_name` | 起运港名称（如 `上海`） | 可选 |
| `pod` | 目的港代码（如 `USLAX`） | 必填 |
| `pod_name` | 目的港名称（如 `洛杉矶`） | 可选 |
| `container_type` | 箱型标准代码（如 `40HQ`） | 可选 |
| `carrier` | 船公司（如 `COSCO`） | 可选 |
| `etd` | 船期（如 `2026-04-15`，用户提到的单个日期默认解释为 ETD） | 可选 |
| `currency` | 币种，默认 `USD` | 可选 |

**箱型标准化对照（识别用户输入并转换为标准代码）：**
- 20GP = 20' = 20FT = 20DV = 20DC = 20 Dry = 20英尺标准箱
- 40GP = 40' = 40FT = 40DV = 40DC = 40 Dry = 40英尺标准箱
- 40HQ = 40HC = 40英尺高柜
- 其余标准代码直接使用：45HQ、40NOR、20RF、40RF、20OT、40OT、20FR、40FR、DG、HT、TK

**`pol` 或 `pod` 缺失时，追问用户，不执行后续步骤。**

---

## 步骤二：确认目标价格

如用户**未提供目标价格**，发送以下消息：

```
您是否有目标价格？如果有请告诉我。如果没有，有运价更新时我会直接推送给您哦～盯价任务默认一周。
```

**用户回复处理：**
- 提供了目标价格 → 记录 `target_price` 和 `currency` → 进入步骤三
- 表示没有目标价格 / 回复"好的"/"不用"/"直接推" → 视为无目标价格（`target_price` 留空）→ 进入步骤三

如用户**已提供目标价格**，直接进入步骤三。

---

## 步骤三：向用户展示最终确认

以纯文字展示即将创建的盯价任务，明确询问用户是否确认创建。

**固定格式（必填项）：**

```
请确认是否要创建盯价任务：
起运港：{pol_name}（{pol}）
目的港：{pod_name}（{pod}）
```

其后根据实际信息，**仅展示用户已提供的可选项**，未提供的不输出对应行：

| 可选项 | 已提供时追加 |
|---|---|
| 箱型 | `箱型：{container_type}` |
| 船期 | `船期：{etd}` |
| 船公司 | `船公司：{carrier}` |
| 目标价格 | `目标价格：{target_price} {currency}` |

最后追加一行：`盯价任务默认一周哦～`

> 有效期由服务端创建时自动计算，此处不展示，**禁止自行推算或填写日期**。

**必须等待用户明确确认后才能进入步骤四。**

---

## 步骤四：确保推送 cron 就绪（创建盯价任务的前置条件）

**cron 是运价推送的基础设施。必须先确认 cron 已就绪，再创建盯价任务；若 cron 无法就绪，不得进入步骤五。**

### 4.1 检查 cron 是否已存在

```bash
openclaw cron list
```

在输出中查找名为 `eyun-watch-poll` 的任务。

- **已存在** → 直接进入步骤五。
- **不存在** → 继续 4.2。

### 4.2 注册轮询 cron

将下方命令中的 `{EYUN_BASE_URL}`、`{EYUN_COMPANY_ID}`、`{channel}`、`{to}` 全部替换为步骤零查询到的实际值后执行，**禁止保留占位符原文**：

```bash
openclaw cron add \
  --name "eyun-watch-poll" \
  --every "5m" \
  --session isolated \
  --message "Call the Eyun watch results API and notify the user if there are new freight results.

Steps:
1. Run this command:
   curl -s -X GET \"{EYUN_BASE_URL}/api/v1/watch-results/push\" -H \"company-id: {EYUN_COMPANY_ID}\"

2. Parse the JSON response.
   - If 'data' is an empty array: do nothing, output nothing.
   - If 'data' has items: format each item as a freight rate notification (route, carrier, price, ETD) and output the summary.

Output language: Chinese." \
  --tools exec \
  --announce \
  --channel {channel} \
  --to {to}
```

### 4.3 验证注册结果

```bash
openclaw cron list
```

确认输出中出现 `eyun-watch-poll`，状态为 `active`。

- **注册成功** → 进入步骤五。
- **注册失败** → 告知用户推送通道暂时无法就绪，说明原因，**不得**继续创建盯价任务。

---

## 步骤五：调用盯价创建接口

将 `{EYUN_BASE_URL}` 和 `{EYUN_COMPANY_ID}` 替换为步骤零读取到的实际值后执行：

```bash
curl -s -X POST "{EYUN_BASE_URL}/api/v1/watch-tasks" \
  -H "Content-Type: application/json" \
  -H "company-id: {EYUN_COMPANY_ID}" \
  -d '{
    "pol": "<起运港代码>",
    "pol_name": "<起运港名称或 null>",
    "pod": "<目的港代码>",
    "pod_name": "<目的港名称或 null>",
    "container_type": "<箱型代码或 null>",
    "carrier": "<船公司或 null>",
    "etd": "<船期 YYYY-MM-DD 或 null>",
    "target_price": <目标价格数字或 null>,
    "currency": "USD"
  }'
```

> `valid_from` 和 `valid_to` 无需传入，服务端自动设置为**从现在起 7 天**。

### 成功响应

```json
{
  "data": {
    "id": 1001,
    "pol": "CNSHA",
    "pod": "USLAX",
    "container_type": "40HQ",
    "target_price": "1200.00",
    "currency": "USD",
    "status": "active",
    "valid_from": "2026-04-05T10:00:00+00:00",
    "valid_to": "2026-04-12T10:00:00+00:00"
  }
}
```

### 失败处理

- HTTP 4xx：提示用户参数有误，说明具体原因
- HTTP 5xx：提示服务暂时不可用，建议稍后重试

---

## 步骤六：回复用户

以纯文字告知用户任务已创建，仅列出有值的字段：

```
✅ 盯价任务已创建！

航线：{pol_name}（{pol}）→ {pod_name}（{pod}）
```

其后仅列出有值的可选项（箱型、船公司、船期、目标价格），格式同步骤三确认模板。

最后说明推送规则（二选一）：
- 设置了目标价格：`达到目标价格时将自动通知您`
- 未设置目标价格：`有运价更新时将自动推送给您`

**不得在服务器响应之外补充任何承诺或预测**（如"一定会有结果"、"预计明天有运价"）。

至此本次对话结束，后续运价结果将由系统自动推送，无需用户或 agent 进行任何操作。

