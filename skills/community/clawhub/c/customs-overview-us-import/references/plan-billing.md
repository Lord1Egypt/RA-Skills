# 套餐计费与余额降级

跨境魔方开放平台的 `/agent/search/**`、`/agent/customs/**`、`/agent/map/**` 接口支持套餐计费。
本技能的脚本已按本规范处理计费：支持套餐的接口默认走套餐，不支持套餐的接口固定按余额计费。调用方（AI）必须遵守下面的确认流程。

## 1. planMode 取值

| planMode | 含义 | 扣费来源 |
|---|---|---|
| 不传 | 历史行为，后端默认按余额计费 | API 余额 |
| `1` | 显式使用 API 余额 | API 余额 |
| `2` | 显式使用套餐 | 套餐额度 |

**支持套餐的接口默认传 `planMode=2`（套餐优先）**；不支持套餐的接口（如 `/agent/validation/**`、`/agent/mail/**`、`/agent/sms/**`）不会传该参数，传了也会被忽略。

## 2. 解析优先级

脚本按以下顺序决定本次 planMode：

1. 环境变量 `UPKUAJING_PLAN_MODE`（`1` / `2` / `0|off|none` 表示不传）
2. 请求参数中的 `planMode`
3. 接口默认值（支持套餐的接口为 `2`）

环境变量优先级最高：分页任务用 `--task_id` 续跑时会复用历史参数，必须保证用户「改用余额」的选择不被历史 `planMode=2` 覆盖。

## 3. 套餐不可用的信号（退出码 3）

套餐不可用时（无有效套餐 / 额度用完），脚本**在业务执行前**停止，不产生任何扣费，并输出：

- 退出码：`3`
- stdout 追加一行：`PLAN_UNAVAILABLE {JSON}`（单行 JSON，便于在进度输出之后定位）

### JSON 字段

| 字段 | 说明 |
|---|---|
| status | 固定 `plan_unavailable` |
| reason | `no_plan`（无有效套餐）或 `quota_exhausted`（额度用完） |
| reasonText | 中文原因，可直接转述 |
| httpStatus / code | 原始状态码，仅用于排查，**不要直接展示给用户** |
| endpoint | 本次调用的接口 |
| requestId | 请求追踪 ID |
| retryAfterSeconds | 预计恢复秒数（429 时取自响应体 `retryAfter`，缺失时取 `Retry-After` 响应头） |
| resumeAt | 预计恢复时间（本地时间） |
| exhaustedWindows | 额度不足的窗口：`window` / `capability` / `quotaType` / `limit` / `used` / `remaining` / `resetsAt` |
| serverHint | 服务端提示（可能为空） |
| paramsSummary | 本次请求参数摘要（已截断） |
| nextActions | 固定 `["use_balance", "retry_later", "upgrade_plan"]` |
| retryWith | 改用余额的重试方式 |
| askUser | 可直接转述给用户的询问文案 |
| billingMode | 固定 `PLAN` |

### 示例

```text
PLAN_UNAVAILABLE {"status":"plan_unavailable","reason":"quota_exhausted","reasonText":"套餐额度已用完","httpStatus":429,"code":1005,"endpoint":"/agent/search/company/list","requestId":"8f4a1c2e9b7d4f5a8c3e1d2b6a9f7c0e","retryAfterSeconds":1800,"resumeAt":"2026-11-25 21:30:00","exhaustedWindows":[{"window":"req5h","capability":"SEARCH","quotaType":"REQUEST","limit":300,"used":300,"remaining":0,"resetsAt":1798761600}],"serverHint":"","paramsSummary":"{\"keywords\": [\"valve\"]}","nextActions":["use_balance","retry_later","upgrade_plan"],"retryWith":"UPKUAJING_PLAN_MODE=1 <同一条命令>","askUser":"套餐额度已用完，预计约 30 分钟后恢复，恢复时间约 2026-11-25 21:30:00。是否改用API余额继续本次调用？改用余额将按接口定价扣费，可用 auth.py --price_info 查询单价。","billingMode":"PLAN"}
```

## 4. 调用方处理流程（必须遵守）

1. 识别 stdout 中的 `PLAN_UNAVAILABLE` 行与退出码 `3`。
2. 用自然语言说明：触发原因 + 预计恢复时间（有的话）+ 哪个能力窗口额度不足。
3. 说明改用余额的计费口径：本次将按接口定价从 API 余额扣费（单价用 `python scripts/auth.py --price_info` 查询），并给出接口名与参数摘要。
4. **停下来等用户明确回复**，不要在同一条消息里直接重试。
5. 用户同意 → 用同一条命令加环境变量 `UPKUAJING_PLAN_MODE=1` 重跑：

   ```bash
   UPKUAJING_PLAN_MODE=1 python scripts/xxx.py --params '...'
   ```

   PowerShell：

   ```powershell
   $env:UPKUAJING_PLAN_MODE='1'; python scripts/xxx.py --params '...'
   ```

6. 余额调用成功后展示 `fee`（`apiCost` / `balance`，单位：分钱）；若返回余额不足（95），提示充值（`python scripts/auth.py --new_rec_order`），不再重试。
7. 用户拒绝 → 本次不执行、不扣费；给出三个出口：稍后重试 / 升级套餐（`--plan_config`）/ 使用余额。**不要反复弹窗**。

### 会话内记忆

如果用户明确表示「本会话都用余额」，后续同类调用可直接带 `UPKUAJING_PLAN_MODE=1`；金额较大或批量调用前，仍建议再次确认。

### 幂等

网络超时后的重试，建议两次调用使用同一个 `UPKUAJING_IDEMPOTENCY_KEY`（脚本会作为 `Idempotency-Key` 请求头发送），避免重复计费。429 / 1004 发生在业务执行之前，改传 `planMode=1` 重试不会重复扣费。

## 5. 错误码对照

| code / HTTP | 含义 | 处理 |
|---|---|---|
| 95 | 余额不足 | 提示充值，不重试 |
| 98 | 参数错误（含 planMode 非法） | 检查参数，不重试 |
| 1003 | 该接口不支持套餐 | 移除 planMode，不重试 |
| 1004 | 无有效套餐 | 退出码 3，询问用户是否用余额 |
| 1005 / HTTP 429 | 套餐额度已用完 | 退出码 3，询问用户是否用余额 |
| HTTP 429（非套餐原因） | 普通限流 | 按原 HTTP 错误处理 |

**不要向用户暴露错误码原文**，统一转成可读文案。

## 6. 额度查询（建议批量调用前预检）

| 命令 | 接口 | 说明 |
|---|---|---|
| `python scripts/auth.py --plan_quota` | `POST /agent/plan/quota` | 当前套餐可用性与各窗口 `limit` / `used` / `remaining` / `resetsAt` |
| `python scripts/auth.py --plan_config` | `POST /agent/plan/config` | 各档位额度上限（免鉴权），用于说明升级后能获得多少额度 |
| `python scripts/auth.py --account_info` | `POST /agent/auth/info` | 余额与套餐字段 |

- `available=0` 或目标窗口 `remaining=0` 时，直接进入「是否使用余额」的询问，避免必然失败的调用。
- `/agent/auth/plan/fallback` 配置对 Agent 不生效（仅 API 渠道），不要依赖它做降级。
