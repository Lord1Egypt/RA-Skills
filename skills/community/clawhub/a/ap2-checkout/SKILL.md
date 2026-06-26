---
name: ap2-checkout
description: AP2 Agent-to-Agent mock checkout (SuperShoe). HP/HNP with card or x402 via mcporter and local mock MCP. No real payments.
version: 1.0.1
user-invocable: true
metadata: {"openclaw":{"emoji":"🛒","requires":{"bins":["mcporter","curl","uv","python3"]},"envVars":[{"name":"AP2_HOME","required":true,"description":"Absolute path to AP2 repository root (directory containing code/)."},{"name":"MCPORTER_CONFIG","required":false,"description":"Path to this skill mcporter.json after ClawHub install."}],"install":[{"id":"mcporter","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter CLI"}]}}
---

# AP2 Checkout (mock)

Drive the **AP2 unified demo** purchase flow via **mcporter** against **local mock** MCP servers (merchant, buyer, credentials provider, MPP). All settlement is simulated.

## One-command install (recommended for demo)

From your AP2 clone (installs skill, patches OpenClaw, **starts mock backend**):

```bash
cd "$AP2_HOME"
npx -y file:code/samples/python/scenarios/a2a/unified/clawhub/npm/ap2-agent-checkout install
```

Then restart the OpenClaw gateway. Manual steps below are only needed if you skip the installer.

## First-time setup (manual)

1. **Clone AP2** and set `AP2_HOME` to the repository root (the folder that contains `code/`):

```bash
export AP2_HOME="/path/to/AP2"
```

2. **Start the mock backend** (triggers 8091–8094, MCP HTTP 8100–8103):

```bash
cd "$AP2_HOME/code/samples/python/scenarios/a2a/unified"
chmod +x openclaw/start_ap2_backend.sh openclaw/stop_ap2_backend.sh
./openclaw/start_ap2_backend.sh
```

3. **Point mcporter** at this skill's `mcporter.json` (after ClawHub install, use the skill directory):

```bash
# After clawhub install (adjust if your skills dir differs):
export MCPORTER_CONFIG="$HOME/.openclaw/workspace/skills/ap2-checkout/mcporter.json"
```

4. **Enable skills** in `~/.openclaw/openclaw.json`: `mcporter` and `ap2-checkout` → `enabled: true`. Restart the gateway.

5. **Verify** (optional): run `scripts/check-backend.sh` from this skill folder with `AP2_HOME` set.

See `references/setup.md` for ports and troubleshooting.

## Session identity

Use a stable **`session_id`** per chat (Feishu channel + peer id, or any unique string). Pass it to every **`ap2-buyer.*`** tool.

```bash
mcporter list ap2-buyer --schema
mcporter list ap2-merchant --schema
```

## Mode selection (always first)

| User intent | presence_mode | payment_method |
|-------------|---------------|----------------|
| Drop / monitor / buy when price drops | `hnp` | `card` or `x402` if user says crypto |
| Buy now / in stock today | `hp` | `card` or `x402` if user says so |

```bash
mcporter call ap2-buyer.set_ap2_session_config_tool \
  session_id=CHAT_ID presence_mode=hnp payment_method=card merchant=shoe
mcporter call ap2-buyer.get_ap2_session_config_tool session_id=CHAT_ID
```

Follow **`merchant_instruction`** from `get_ap2_session_config`.

## Trusted Surface (user approval)

Before signing mandates, show a clear summary (item, price cap, payment rail). Wait for explicit **yes / approve / 确认**.

```bash
mcporter call ap2-buyer.register_trusted_surface_approval \
  session_id=CHAT_ID price_cap=200 payment_method=card \
  item_id=supershoe_limited_edition_gold_sneaker_womens_9_0
```

Plain-text budget or "pay by card" alone is **not** approval.

## HNP flow (delegated drop)

1. Set config → `hnp` + `card` or `x402`.
2. Build `item_id` as `<slug>_0` (lowercase, non-alphanumeric → `_`). **Do not** call `search_inventory` for shoes.
3. `mcporter call ap2-merchant.check_product item_id=... constraint_price_cap=200`
4. Mandate summary → user approval → `register_trusted_surface_approval`.
5. Sign mandates — `mandate_request` must be a **JSON string** inside `--args`:

```bash
mcporter call ap2-buyer.assemble_and_sign_mandates --args '{
  "session_id": "CHAT_ID",
  "mandate_request": "{\"item_id\":\"...\",\"price_cap\":200,\"qty\":1}"
}'
```

6. Poll: `mcporter call ap2-buyer.check_constraints session_id=CHAT_ID price=299 available=false`
7. If stock 0, user runs (replace ITEM_ID and PRICE from tool results):

```bash
curl -X POST "http://127.0.0.1:8091/trigger-price-drop?item_id=ITEM_ID&price=199&stock=10"
```

8. When `meets_constraints` is true: `assemble_cart` → `create_checkout` → payment/checkout presentations → `issue_payment_credential` (`presence_mode=hnp`) → `complete_checkout` → `verify_checkout_receipt_tool`. Emit **`purchase_complete`** JSON and stop.

## HP flow (buy now)

1. Set config → `hp` + `card` or `x402`.
2. `search_inventory` or `check_product` → `assemble_cart`.
3. **Once:** `create_hp_open_mandates` (no `checkout_jwt` yet).
4. `create_checkout` with `open_checkout_mandate_id` and `payment_method`.
5. Checkout summary → user **确认** → `register_trusted_surface_approval`.
6. `assemble_and_sign_immediate_mandates` with `checkout_jwt`, `checkout_jwt_hash`, `amount_cents`, etc.
7. `issue_payment_credential` (`presence_mode=hp`) → `complete_checkout` → **`purchase_complete`**.

**Never** call `create_hp_open_mandates` twice per purchase. **Never** re-run `assemble_cart` / `create_checkout` after user confirmed.

## Payment rail switch

`set_ap2_session_config_tool` with new `payment_method` → `clear_open_mandate_session_tool` → re-approve → sign again.

## Stop backend

```bash
cd "$AP2_HOME/code/samples/python/scenarios/a2a/unified" && ./openclaw/stop_ap2_backend.sh
```
