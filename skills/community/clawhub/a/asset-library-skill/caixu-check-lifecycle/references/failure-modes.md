# Failure Modes

## Unknown goal

- 直接结构化失败
- 不要静默回退到默认场景

## Invalid lifecycle payload

以下任一情况都必须失败或 partial：

- schema 不完整
- `asset_id` 不存在
- 日期不是绝对 `YYYY-MM-DD`
- `readiness` 与 blocking/warning items 冲突

## Persistence boundary

- 失败结果只写 audit
- 不把冲突 payload 写成正式 lifecycle run
