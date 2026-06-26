---
name: flight-scout
description: 调用远程 Flight Scout 商用 API 的 skill。用于用户提供 API base URL 和 API key 后，执行航班搜索、价格日历、同步甩尾查询、异步甩尾任务查询，并返回结构化 JSON 结果。
homepage: https://github.com/EBOLABOY/flight-scout
metadata:
  openclaw:
    homepage: https://github.com/EBOLABOY/flight-scout
    primaryEnv: FLIGHT_SCOUT_API_KEY
    requires:
      bins:
        - python3
      env:
        - FLIGHT_SCOUT_API_BASE_URL
        - FLIGHT_SCOUT_API_KEY
---

# flight-scout

该 skill 目录通常会附带一个 `.env.example` 模板文件。

推荐做法：

- 使用官方安装脚本完成安装或更新；脚本会保留现有 `.env`，只同步受管理文件
- 如果手动安装，请根据 `.env.example` 创建本地 `.env`
- 本地 `.env` 用于保存真实接口密钥，不应提交到版本库

本地 `.env` 里通常包含：

- `FLIGHT_SCOUT_API_BASE_URL`
- `FLIGHT_SCOUT_API_KEY`
- `FLIGHT_SCOUT_API_TIMEOUT_SECONDS`

脚本行为：

- `scripts/call_api.py` 会优先自动读取 skill 根目录下的 `.env`
- 如果当前 shell 已经显式设置了同名环境变量，则以显式环境变量为准

读取以下环境变量：

- `FLIGHT_SCOUT_API_BASE_URL`
- `FLIGHT_SCOUT_API_KEY`
- `FLIGHT_SCOUT_API_TIMEOUT_SECONDS`，默认 `30`

调用前必须确认：

1. 出发机场三字码
2. 到达机场三字码
3. 日期
4. 舱位与乘客数（如未给出，默认 `economy` 和 `1`）

优先使用脚本：

- [scripts/call_api.py](scripts/call_api.py)

示例命令：

```bash
python3 {baseDir}/scripts/call_api.py search --origin HKG --destination NRT --date 2026-05-01
python3 {baseDir}/scripts/call_api.py calendar --origin PVG --destination CDG --date-start 2026-07-03 --date-end 2026-07-15
```

接口选择规则：

- 普通航班搜索：调用 `search`
- 机场联想补全：调用 `airport-search`
- 日期区间最低价：调用 `calendar`
- 甩尾票接口选择：
  - 如果需要同步直接返回结果，调用 `hidden-city-sync`
  - 如果接受异步任务和轮询，调用 `hidden-city-job-create`
  - 不需要先调用 `hidden-city-sync` 再决定是否发起 `hidden-city-job-create`
  - 选择依据主要是“是否需要即时结果”和“调用额度消耗”，不是先做命中判断
- 用量汇总：调用 `usage`
- 当用户询问“已用多少额度 / 剩余多少额度 / 什么时候重置”时，优先调用 `usage`
- 如果业务接口返回 `quota_exceeded`，继续读取 `meta.remaining_units`、`meta.cycle_ends_at`、`meta.upgrade_required`

结果处理要求：

- 直接返回接口 JSON，不要重写字段名
- 如果接口返回错误，保留 `request_id`、`error.code`、`error.message`
- 额度相关字段优先读取 `data.quota.*`；如果是额度拦截错误，则读取 `meta.remaining_units`、`meta.included_units`、`meta.cycle_ends_at`
- 如果使用异步 job，明确告诉用户当前 `job_id` 和状态
- 如果使用同步查询，就按同步结果直接说明；如果使用异步 job，就按任务状态与最终结果说明

详细接口字段见 [references/api-contract.md](references/api-contract.md)
