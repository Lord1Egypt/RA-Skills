# KFC/McD clawauto-shop Skill（2.0.0）

Automates KFC and McDonald's order-link flows after backend returns a `cdkey` URL.

**仅需查询**：若只需 **查询商品信息** 与 **查询个人信息**，请使用 **1.0.0** 目录：`../1.0.0/`。

## Upload Readiness (ClawHub)
- Self-contained under this folder (`openclaw_skill.py`, `kfc_place_order_test_old.py`, `kfc_custom_product_flow.py`, `kfc_vip_choose_spec_flow.py`, `mcd_place_order_test.py`, `mcd_custom_product_flow.py`, `requirements.txt`).
- No hardcoded local paths.
- Outputs are written to `skill/outputs/` (or current dir).
- Can run with user-configured phone + api key.

## Required Runtime Config
Use either CLI args or environment variables. For OpenClaw usage, **.env is recommended**:

### Env-based config (dev / prod)

Create `.env` manually in this folder, then paste and modify:

```env
KFC_PLATFORM_ENV=dev
KFC_PLATFORM_PHONE=13800138000
KFC_PLATFORM_API_KEY=your_api_key_here
KFC_PLATFORM_BASE_URL_DEV=http://localhost:8888/api/openclaw
KFC_PLATFORM_BASE_URL_PROD=https://www.clawauto.shop/api/openclaw
KFC_PLATFORM_BASE_URL=http://localhost:8888/api/openclaw
# Optional:
# KFC_PLATFORM_USERNAME=your_username
```

Then configure:

- Environment:
  - `KFC_PLATFORM_ENV`: `dev` / `prod` (default `dev`)
- Backend base URL:
  - `KFC_PLATFORM_BASE_URL_DEV`: dev backend, default `http://localhost:8888/api/openclaw`
  - `KFC_PLATFORM_BASE_URL_PROD`: prod backend, default `https://www.clawauto.shop/api/openclaw`
  - `KFC_PLATFORM_BASE_URL`: common base URL fallback
- Identity & API key:
  - `KFC_PLATFORM_PHONE`: user phone
  - `KFC_PLATFORM_API_KEY`: API key
  - optional `KFC_PLATFORM_USERNAME`

When running inside OpenClaw, `.env` will be loaded automatically, so you don't need to type these each time.

### CLI vs env

- Identity:
  - `--phone` or `KFC_PLATFORM_PHONE`
  - (fallback) `--username` or `KFC_PLATFORM_USERNAME`
- API key:
  - `--api-key` or `KFC_PLATFORM_API_KEY`
- Backend URL:
  - `--base-url` or `KFC_PLATFORM_BASE_URL`
  - default: `http://localhost:8888/api/openclaw`

## Runtime Chain
1. Optional: `GET /health` 探活（无鉴权，独立限流）。
2. Query platform products (`POST /products`).
3. Optional: `POST /orders` 拉取当前用户订单列表（与网页端「我的订单」同源）。
4. User selects `product_id` (or `supplier_goods_id` for supplier-only SKUs).
5. Skill calls platform order (`POST /order`)，请求体可带 `idempotency_key`，或使用 HTTP 头 `Idempotency-Key`。
6. After order: use `POST /order/status` with `order_id` to poll supplier status / refreshed meal URL (`openclaw_skill.py --fetch-order-status <id>`).
7. Skill auto-runs browser order flow based on returned `flow` or URL host.
8. Stops before final submit by default unless explicitly allowed.

OpenClaw JSON 错误体含 `message` + `code`（如 `OPENCLAW_UNAUTHORIZED`、`OPENCLAW_RATE_LIMITED`）；成功响应带 `X-OpenClaw-RateLimit-Remaining` / `X-OpenClaw-RateLimit-Limit`，限流时另有 `Retry-After`。

## Flow 识别规则（OpenClaw 调用时据此选择脚本）

| 优先级 | URL 特征 | flow_code | 脚本 |
|--------|----------|-----------|------|
| 1 | 后端 order 返回 `flow.code` 且存在于注册表 | 后端指定 | 见 FLOW_REGISTRY |
| 2 | `vip.woaicoffee.com` 且含 `outId=` 且非 choose_specifications | `kfc_vip_choose_spec` | `kfc_vip_choose_spec_flow.py` |
| 3 | `kfc.woaicoffee.cn` 且含 `cdkey=` 且非 customProduct 路径 | `kfc_custom_product` | `kfc_custom_product_flow.py` |
| 4 | `kfc.woaicoffee.cn`（其他） | `kfc_city_store_booking` | `kfc_place_order_test_old.py` |
| 5 | `mdl.woaicoffee.cn` 且含 `cdkey=` 且非 customProduct 路径 | `mcd_custom_product` | `mcd_custom_product_flow.py` |
| 6 | `mdl.woaicoffee.cn`（其他） | `mcd_store_eattype` | `mcd_place_order_test.py` |
| 7 | 其他 | （空） | 仅打开浏览器 |

主程序会输出一行 `flow_detected: <flow_code> -> <script>` 便于日志与校验。

## Required Per-Run Inputs (purchase flow)
- `--product-id`
- `--store-keyword`
- KFC flow only: `--city`

Optional:
- `--store-name`
- `--pickup-type` (default `Dine-in` for McD / `外带` for KFC)
- `--pickup-time` (empty => immediate pickup)
- `--eat-type` (McD only, default `Dine-in`)
- `--kfc-store-code` (肯德基门店编号如 SHA391，VIP/customProduct 不填则用 city+store-keyword 调 API)
- `--booking-time` (肯德基 customProduct 预定时间编码，0=立即取餐)
- `--mcd-store-number` (麦当劳 customProduct 直接填门店编号，不填则用 store-keyword 调 API)
- `--wait-pickup-seconds` (麦当劳/肯德基 VIP 等待取餐码最大秒数，默认 60)
- `--list-products` (query only, no purchase)
- `--skip-flow` (return link only)
- `--allow-final-submit` (explicitly allow clicking final confirm)
- `--no-final-submit` (force stop; safety mode already stops)

## Install
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Backend Requirement
Backend endpoint must be reachable:
- `KFC_PLATFORM_BASE_URL` or default `http://localhost:8888/api/openclaw`
- `POST /api/openclaw/products`: accepts username/phone + api_key
- `POST /api/openclaw/order`: validates balance (yuan), deducts cost, returns order link + `cost_yuan` / `balance_yuan`  
- 肯德基 VIP 链接：`GET /api/openclaw/kfc/store?city=xxx&keyword=xxx` 返回 `{"store_code": "SHA391"}`（或 `storeCode`/`store`）
- 麦当劳 customProduct：`GET /api/openclaw/mcd/store?keyword=xxx` 返回 `{"store": "1450468"}`

## Quick Start (recommended with env)
```bash
set KFC_PLATFORM_PHONE=13800138000
set KFC_PLATFORM_API_KEY=your_api_key

python openclaw_skill.py --list-products
```

Then purchase and auto-order:
```bash
python openclaw_skill.py --product-id 1 --city 上海 --store-keyword 金地新华道
```

## 肯德基 customProduct 链接（kfc.woaicoffee.cn/?cdkey=...）

当订单链接为 **肯德基 customProduct** 格式（`https://kfc.woaicoffee.cn/?cdkey=...`，且不是已带 `customProduct` 的完整链接）时，Skill 会：

1. **转换链接**：用 `--city` + `--store-keyword` 调用后端 `GET /kfc/store?city=xxx&keyword=xxx` 获取门店编号，或直接使用 `--kfc-store-code`；`--booking-time` 为预定时间编码（默认 `0`=立即取餐）。生成：
   `https://kfc.woaicoffee.cn/index/index/customProduct?cdkey=...&store=...&booking_time=...`
2. **浏览器流程**：打开转换后的链接 → 点击页面最下方红色「确认提交」→ 弹窗点「确认」完成下单 → 等待订单成功页、识别取餐码并截图，输出简要信息。
3. **输出**：取餐码、订单号、截图路径等通过 `print_chat_report` 输出给用户。

**必填**：`--city` 与 `--store-keyword`（用于查门店）或 `--kfc-store-code`。  
**可选**：`--booking-time`（默认 0，立即取餐）、`--wait-pickup-seconds`（默认 60）。

## 肯德基 VIP 兑换链接（vip.woaicoffee.com）

当订单链接为 **肯德基 VIP** 格式（`https://vip.woaicoffee.com/?outId=xxx`）时，Skill 会：

1. **浏览器步骤**：打开链接 → 点击「下一步」→ 若有定位权限弹窗则点击「访问该网站时允许」→ 从当前访问链接解析 `productId`。
2. **转换链接**：用 `--city` + `--store-keyword` 调用后端 `GET /kfc/store?city=xxx&keyword=xxx` 获取门店编号 `storeCode`，或直接使用 `--kfc-store-code`；生成：
   `https://vip.woaicoffee.com/kfc/choose_specifications?outId=xxx&productId=393&storeCode=SHA391&sendPhoneMsg=false`
3. **下单**：打开上述链接 → 点击「下单」→ 二次确认弹窗点击「确认」→ 等待页面刷新出现取餐码（最多 `--wait-pickup-seconds` 秒）→ 将取餐信息返回用户。

**必填**：`--city` 与 `--store-keyword`（用于查门店）或 `--kfc-store-code`（直接填门店编号如 SHA391）。  
**可选**：`--wait-pickup-seconds`（默认 60）。

## 麦当劳 customProduct 链接（门店自提）

当订单链接为 **麦当劳 customProduct** 格式（`https://mdl.woaicoffee.cn/?cdkey=...`，且不是已带 `customProduct` 的完整链接）时，Skill 会：

1. **转换链接**：用 `--store-keyword` 调用后端 `GET /mcd/store?keyword=xxx` 获取门店编号，或直接使用 `--mcd-store-number`；`eat_type` 固定为 **门店自提**，生成：
   `https://mdl.woaicoffee.cn/index/index/customProduct?cdkey=...&store=...&eat_type=门店自提`
2. **浏览器流程**：打开转换后的链接 → 点击页面底部红色「下单」→ 弹窗「请再次确认门店信息是否正确」中点击蓝色「就是这个餐厅」（不点「返回重选」）→ 等待下单成功页，最多 **1 分钟** 内获取取餐码/订单号。
3. **输出**：取餐信息、订单号、截图路径等通过 `print_chat_report` 输出给用户。

**必填**：`--store-keyword`（用于查门店）或 `--mcd-store-number`（直接填门店编号）。  
**可选**：`--wait-pickup-seconds`（默认 60，等待取餐码最大秒数）。

## 断连与恢复（大模型异常时在聊天框展示结果）

当 OpenClaw 大模型断连或订单执行停滞时：

1. **订餐链接已返回时**：Skill 在获得订餐链接后会**立即**输出可解析行，便于客户端/大模型从**已有输出**中提取并展示给用户：
   - 标准输出中会有一行以 `OPENCLAW_FINAL_LINK:` 开头的订餐链接。
   - 另有一行 `OPENCLAW_ORDER_STATE:` 开头的 JSON，含 `url`、`order_id`、`stage` 等。
   - **建议**：大模型或调用方在断连、超时、异常时扫描本次调用的 stdout，若匹配到 `OPENCLAW_FINAL_LINK:`，则**直接在用户聊天框展示该链接**，并提示「订单已生成订餐链接，请点击使用」。

2. **订单状态保存在用户本地**：每次下单/流程推进都会把当前阶段写入**本地目录**（默认 `skill/2.0.0/openclaw_order_state/`，可通过环境变量 `OPENCLAW_ORDER_STATE_DIR` 覆盖）。保存内容包括：`order_id`、`url`、`stage`（order_received / flow_running / flow_done / flow_failed）、取餐码等。该目录含订餐链接等敏感信息，已加入 `.gitignore`，请勿提交到版本库。

3. **恢复后查询进度**：大模型恢复或用户询问「订单到哪了」时，可再次调用 Skill 的**查询模式**，从本地读取并返回当前阶段与订餐链接：
   - 按幂等键查询：`--query-order <idempotency_key>`（与下单时使用的 `--idempotency-key` 一致）。
   - 按订单 ID 查询：`--query-order-by-id <order_id>`。
   - **列出本机最近订单**：`--list-local-orders` 输出最近约 20 条本地订单的 order_id、阶段、更新时间与链接摘要，用户说「我最近的订单」时先调此接口，再按 order_id 用 `--query-order-by-id` 查详情。
   - 查询会输出阶段说明、订餐链接（若有）以及取餐码/订单号（若流程已跑完），并再次输出 `OPENCLAW_FINAL_LINK:` 行便于展示。

**解析订餐链接（供调用方/大模型实现）**：从 Skill 的 **stdout** 中取**第一行**包含 `OPENCLAW_FINAL_LINK:` 的整行，**冒号后到行尾**的字符串 trim 后即为订餐链接 URL；可直接展示给用户或写入聊天框。

**建议**：调用方在下单时传入固定的 `--idempotency-key`（例如由会话 ID 或用户 ID 生成），断连后即可用 `--query-order <该 key>` 查询同一笔订单，无需用户提供 order_id。

**示例**（查询本地进度）：
```bash
python openclaw_skill.py --list-local-orders
python openclaw_skill.py --query-order abc123def456
python openclaw_skill.py --query-order-by-id 10086
```

## 报错与处理建议

流程脚本会在结果 JSON 中写入 `error`（详情）和 `error_code`（标准码）。主程序失败时会根据 `error_code` 输出处理建议。

| error_code | 含义 | 处理建议 |
|------------|------|----------|
| `ELEMENT_NOT_FOUND` | 未找到页面上的预期按钮/文案 | 检查页面是否完全加载、网络是否稳定、门店是否营业、链接是否过期 |
| `TIMEOUT` | 页面加载或操作超时 | 检查网络或稍后重试；可适当增加 `--wait-pickup-seconds` |
| `NETWORK` | 网络请求失败 | 检查本机网络与后端/目标站点是否可达 |
| `API_ERROR` | 门店或订单接口返回异常 | 确认后端 `/kfc/store` 或 `/mcd/store` 已实现且返回正确格式；或直接传 `--kfc-store-code` / `--mcd-store-number` |
| `INVALID_URL` | 链接缺少必要参数(cdkey/outId等) | 确认订单接口返回的 url 格式正确 |
| `SUBMIT_ABORTED` | 已按配置在最终确认前停止 | 若需真实下单请使用 `--allow-final-submit` |
| `SCRIPT_NOT_FOUND` | 流程脚本文件不存在 | 确认 skill 目录完整，包含对应 .py 脚本 |
| `RESULT_READ_ERROR` | 无法解析流程结果 | 查看 outputs 目录下最新 JSON 与截图排查 |
