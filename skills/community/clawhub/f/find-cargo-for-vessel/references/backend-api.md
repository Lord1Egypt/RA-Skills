# ShippingClaw 后台需求接口

后台接口尚未提供。当前实现通过环境变量隔离接口差异，搜索功能可独立运行，需求不会丢失。

## 环境变量

- `API_BASE_URL`：ShippingClaw 后台根地址。
- `CARGO_DEMAND_API_PATH`：需求写入路径，例如 `/admin/cargo-demands`。未设置时写入本地 outbox。
- `ADMIN_API_KEY`：优先使用，作为 `X-Api-Key`。
- `ADMIN_TOKEN`：没有 API Key 时作为 Bearer Token。
- `CARGO_MATCHER_CACHE_DIR`：可选缓存目录。

## 暂定请求

`POST {API_BASE_URL}{CARGO_DEMAND_API_PATH}`

```json
{
  "user_id": "当前登录船东用户ID",
  "current_port": "舟山港",
  "destination_port": "防城港",
  "capacity_tons": 10000,
  "trade_type": "domestic",
  "queried_at": "2026-07-25T10:00:00+08:00"
}
```

成功条件：HTTP 2xx。推荐货盘编号不写入需求记录。

后台接口提供后，只需在 `scripts/demand_sync.py` 的 `build_payload` 和 `send_payload` 中按真实字段及响应约定调整，并补充契约测试。
