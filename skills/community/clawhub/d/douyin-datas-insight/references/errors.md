# 退出码与错误码 → Agent 应对

> **何时读**：遇到非常见错误、或要核对完整应对表时再读。日常以 `SKILL.md` 错误摘要为准。

| error_code | 退出码 | 含义 | Agent 必须做什么 |
| --- | --- | --- | --- |
| `AUTH_REQUIRED` / `AUTH_ERROR` | 3 | token 未配置 / 无效或过期 | **禁止重试**。引导到 [官网](https://www.guaikei.com) 开通并配置 `GUAIKEI_API_TOKEN` |
| `PLAN_LIMIT` | 1 | 套餐单次条数超限（常见于包月 Token） | **禁止同参重试**。转述 `message`；可建议降低 `--limit`（视频搜索/用户搜索/作品≤30，评论≤50）或到官网升级按量；**须用户同意后再跑** |
| `INSUFFICIENT_BALANCE` | 1 | 按量 Token 余额不足（含详情接口余额预检） | **禁止同参重试**。引导官网充值；不要改参数反复试 |
| `RATE_LIMITED` | 1 | 短时间提交任务过多 | **禁止立即重试**。告知稍后；经用户同意后再跑 |
| `DAILY_LIMIT` | 1 | 今日消费已达每日上限 | **禁止同参重试**。转述 `message`；明日再试或到官网调整每日限额 |
| `INVALID_KEYWORD` | 1 | 关键词不合法（长度/是链接/含特殊符号） | 转述 `message`，请用户换词；**禁止自动改词重试** |
| `INVALID_URL` | 1 | 无法识别链接或 ID，或链接类型传错 | 请用户提供：主页链接（post），或视频/图文链接（comment / detail） |
| `INVALID_ARGS` | 2 | 参数解析失败，或枚举/范围越界 | 按 `--help` 或 [options.md](options.md) 修正后重试**一次**；**禁止改成默认值后自动再跑** |
| `NO_MATCH`（status=empty） | 0 | 无结果，**不是失败** | 如实告知；可建议放宽（`--time 0`、换更常用词），**经用户同意后**再试 |
| `TIMEOUT` / `NETWORK_ERROR` | 1 | 超时或网络错误 | 可告知用户后重试，**最多 1 次**。视频搜索与用户搜索约 9 分钟、作品/详情/评论约 20 分钟内，服务端仍复用同一任务（同参是续等不是重做）。热榜不走这组复用。进程被提前结束后，不要马上再跑同一条命令 |
| `API_SCHEMA_CHANGED` | 1 | 成功响应的结果结构与约定不一致 | 按失败报告 `message`。不要把它说成没有结果 |
| `HTTP_5xx` / 其他 | 1 | 服务端或未知错误 | 如实报告 `message`，不编造原因，不反复重试 |

信封与 `results` 形态见 [contract.md](contract.md)。
