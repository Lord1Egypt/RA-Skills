# API Contract

基础配置：

- Header: `X-API-Key`
- 可选 Header: `Idempotency-Key`
- 常见额度响应头：
  - `X-Flight-Scout-Plan-Code`
  - `X-Flight-Scout-Quota-Status`
  - `X-Flight-Scout-Quota-Used-Units`
  - `X-Flight-Scout-Quota-Remaining-Units`
  - `X-Flight-Scout-Quota-Window-End`
- 基础响应：

```json
{
  "request_id": "uuid",
  "data": {},
  "meta": {},
  "error": null
}
```

## POST /v1/flights/search

请求体：

```json
{
  "origin": "LHR",
  "destination": "PEK",
  "date": "2026-05-01",
  "return_date": null,
  "passengers": 1,
  "cabin_class": "economy",
  "max_polls": 3,
  "sort_by": "best",
  "locale": "zh-CN",
  "with_booking_summary": false,
  "booking_summary_limit": 0
}
```

- 响应里的 `data.offers` 会按 `sort_by` 排序，但不会只返回前几条
- `booking_summary_limit` 只限制附加订票摘要数量，不会截断主报价列表

## POST /v1/flights/calendar

请求体：

```json
{
  "origin": "PVG",
  "destination": "CDG",
  "date_start": "2026-07-03",
  "date_end": "2026-07-15",
  "passengers": 1,
  "cabin_class": "economy",
  "locale": "zh-HK",
  "currency": "CNY",
  "window_days": 30,
  "max_pages": 3,
  "timeout": 12
}
```

## POST /v1/flights/hidden-city/search

轻量同步查询。该端点会使用平台默认策略，并会强制限制：

- 服务端会返回当前扫描范围内的全部候选，不接受 `max_candidates`
- `max_destinations` 控制同步扫描要探索的延伸目的地数量，最大 `10`
- 不支持 `booking_summary`

常见判断方式：

- 如果响应里的 `data.hidden_city_count > 0`，代表快速查询已经发现隐藏城市候选
- 如果 `data.hidden_city_count == 0`，只代表“快速查询暂未发现”，不等于完整异步查询也一定没有结果
- 读取 `data.direct_reference.selection_mode`、`direct_available`、`one_stop_available`、`stops` 来判断参考价是否真的是直飞；如果 `selection_mode` 为 `one_stop_fallback`，就要明确告诉用户“目标航线没有直飞，只找到了 1 次中转参考价”

## POST /v1/flights/hidden-city/jobs

完整异步查询。返回：

```json
{
  "request_id": "uuid",
  "data": {
    "job_id": "uuid",
    "status": "queued",
    "status_url": "/v1/jobs/uuid"
  },
  "meta": {
    "queued": true
  },
  "error": null
}
```

## GET /v1/jobs/{job_id}

返回 `queued` / `running` / `succeeded` / `failed` / `expired` 之一。

- 当状态为 `succeeded` 时，结果通常位于 `data.result`

## GET /v1/airports/search

查询参数：

- `q`
- `locale`

## GET /v1/account/usage

支持查询参数：

- `period=all`
- `period=day`
- `period=month`

返回结果中的 `data.quota` 会给出当前额度周期摘要，常用字段包括：

- `used_units`
- `remaining_units`
- `window_started_at`
- `window_ends_at`
- `status`

`period` 只影响聚合统计窗口，不影响 `quota` 当前周期摘要。

## Common quota_exceeded error

当当前请求会超出 Free / Personal 套餐的包含额度时，接口会返回 `402 quota_exceeded`。

- `error.code = quota_exceeded`
- `meta.used_units` / `meta.included_units` / `meta.remaining_units` 用于表示当前周期额度状态
- `meta.request_units` / `meta.projected_units` 用于表示这次请求为什么会被拦截
- `meta.cycle_started_at` / `meta.cycle_ends_at` 用于表示本周期时间范围
- 同一批关键信息也会通过 `X-Flight-Scout-Quota-*` 响应头返回，方便脚本或网关直接读取
