# DuoPlus Cloud Number API

Source index: <https://help.duoplus.net/docs/4D2HCXVy>

## Common request contract

- Global production base URL: `https://openapi.duoplus.net`
- Mainland China production base URL: `https://openapi.duoplus.cn` (set `DUOPLUS_API_BASE` for the bundled client)
- Method: `POST`
- Headers: `DuoPlus-API-Key: <key>`, `Content-Type: application/json`, optional `Lang: en`
- Success: HTTP 2xx, valid JSON, and top-level `code` equal to `200`
- Rate limit: 1 request per second per endpoint
- Pagination: `page` defaults to 1; `pagesize` defaults to 10 and must not exceed 100

## Endpoints

| Operation | Path | Request fields |
| --- | --- | --- |
| Number list | `/api/v1/cloudNumber/numberList` | Optional `id[]`, `phone_number`, `status[]` (1 active, 2 expired), `type_ids[]` (0 VOIP, 1 Non-VOIP), `region_ids[]`, `renewal_status[]`, `remark`, `sort_by`, `order`, `page`, `pagesize` |
| SMS list | `/api/v1/cloudNumber/smsList` | Required `number_id`; optional `page`, `pagesize` |
| Purchase packages | `/api/v1/cloudNumber/purchasePackage` | Empty object |
| Package durations | `/api/v1/cloudNumber/package` | Required ISO 3166-1 alpha-2 `region`; optional `type` (0 VOIP, 1 Non-VOIP, default 1) |
| Purchase | `/api/v1/cloudNumber/purchase` | Required `region`, integer `duration`; optional `type`, `quantity`, `coupon_code`, `renewal_status` |
| Renewal packages | `/api/v1/cloudNumber/renewalPackage` | Required non-empty `number_ids[]` |
| Renewal | `/api/v1/cloudNumber/renewal` | Required non-empty `list[]`; each item contains non-empty `number_ids[]` and integer `duration` |
| Auto-renewal | `/api/v1/proxy/autoRenewal` | Required non-empty `number_ids[]`, `type` (1 enable, 0 disable) |

The auto-renewal endpoint is documented under `/proxy/` even though it operates on cloud numbers. Use the documented path exactly.

## Relevant response fields

- Number list: `data.list[]` contains `id`, `phone_number`, `assigned`, `region_name`, `type_name`, `status_name`, `renewal_status`, `remark`, `created_at`, `expired_at`; pagination is in `data.page`, `pagesize`, `total`, `total_page`.
- SMS list: `data.list[]` contains `message`, `code`, `received_at`, plus pagination fields.
- Purchase packages: `data[]` contains `type`, `name`, and `country[]`; each country contains `region`, `name`, `durations[]`. Duration entries include `name`, `days`, `gif_days`, `random_gif_days`, `is_special_offer`, `price`, `card_price`, `total_price`.
- Package durations: `data.duration[]` contains supported durations.
- Renewal packages: `data.numbers[]` contains `id`, `phone_number`, `expired_at`, `duration[]`.
- Purchase and renewal: `data.order_id` and `data.product_ids[]`.

## Required sequencing

Purchase must be preceded by a fresh purchase-package lookup and confirmation of the selected region, type, duration, quantity, and price facts. Renewal must be preceded by a fresh renewal-package lookup for all selected IDs and confirmation of each duration. Do not retry mutation requests automatically.

Sources last checked 2026-09-30: Introduction, Cloud Number List, Cloud Number SMS, Cloud Number Purchase Package Details, Cloud Number Package Durations Details, Purchase Cloud Numbers, Cloud Number Renewal Package Details, Renew Cloud Numbers, and Enable/Disable Auto-Renewal.
