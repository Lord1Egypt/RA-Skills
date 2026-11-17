---
name: drivethru-sanmar
description: Deterministic SanMar API toolkit covering the four order-lifecycle pillars — purchase orders, inventory, tracking, and invoicing — behind typed CLI tools over SanMar's SOAP web services, PromoStandards services, and SFTP data feeds. Submit and pre-validate POs; check real-time per-warehouse inventory (PromoStandards v2) or bulk FTP feeds; get package-level tracking (Order Shipment Notification) and parse the FTP Daily Shipment Status file; retrieve invoices (InvoicePort — by PO, invoice number, order date, date range, or unpaid) and parse the FTP Daily Invoice / EDI-810 files, all normalized to a common payables shape. Also search products, pull myPrice pricing, parse PO PDFs, resolve marketing colors to mainframe codes, and file portal returns. Use whenever the user needs to read from or write to SanMar for apparel sourcing, pricing, ordering, tracking, or accounts-payable.
version: 0.3.1
emoji: 👕
homepage: https://www.sanmar.com
metadata:
  openclaw:
    requires:
      bins: [python3]
    envVars:
      SANMAR_CUSTOMER_NUMBER:
        required: false
        description: >
          SanMar customer number for SOAP web services. Optional — credentials
          may instead be passed inline in a tool's stdin JSON. Treat as a secret.
      SANMAR_USERNAME:
        required: false
        description: SanMar web-services username (typically an email). Optional env cache.
      SANMAR_PASSWORD:
        required: false
        description: SanMar web-services password. Optional env cache; treat as a secret.
      SANMAR_ENV:
        required: false
        description: >
          `production` (default) or `development`. `development` flips the PO
          submit endpoint to SanMar's test-ws host.
      SANMAR_FTP_USERNAME:
        required: false
        description: >
          SanMar SFTP username (the customer number). Defaults to
          SANMAR_CUSTOMER_NUMBER. Needed only for mainframe-color resolution.
      SANMAR_FTP_PASSWORD:
        required: false
        description: >
          SanMar SFTP password — distinct from the web-services password. Needed
          only for mainframe-color resolution. Treat as a secret.
      SANMAR_FTP_HOST:
        required: false
        description: Override for the SFTP host. Defaults to `ftp.sanmar.com`.
      SANMAR_FTP_PORT:
        required: false
        description: Override for the SFTP port. Defaults to `2200`.
      SANMAR_FTP_CACHE_DIR:
        required: false
        description: Override for the local SDL CSV cache directory. Defaults to `/tmp/sme-sanmar-cache`.
      SANMAR_FTP_OUTBOUND_DIR:
        required: false
        description: >
          SFTP directory holding the by-request outbound files (Daily
          Invoice, Daily Shipment Status). Account-specific; defaults to the
          FTP root `/`. Can be overridden per-call with `remote_path`.
      SANMAR_PORTAL_USERNAME:
        required: false
        description: >
          sanmar.com customer-portal username — used by the browser-driven
          `process-return` action only. SEPARATE from SANMAR_USERNAME (the
          web-services login). Optional env cache; treat as a secret.
      SANMAR_PORTAL_PASSWORD:
        required: false
        description: >
          sanmar.com customer-portal password for `process-return`. Separate
          from the web-services password. Optional env cache; treat as a secret.
      SANMAR_PORTAL_BASE_URL:
        required: false
        description: Override for the portal base URL. Defaults to `https://www.sanmar.com`.
    install:
      uv:
        - requests>=2.28
        # Optional: required only for parse-po-pdf (PDF intake).
        - pypdf>=4.0
        # Optional: required for all SFTP-backed tools — mainframe-color
        # resolution and fetching the FTP feeds behind get-inventory-feed,
        # get-shipment-status, and parse-invoice-file (server reads only).
        - paramiko>=3.0
        # Optional: required only for the browser-driven process-return action.
        # Also needs a browser binary: `python -m playwright install chromium`.
        - playwright>=1.40
---

# SanMar API toolkit

This skill is a deterministic, JSON-in / JSON-out wrapper over SanMar's **SOAP
web services** and the **PromoStandards** order-shipment-notification service.
Every tool is reached through one CLI entrypoint:

```bash
echo '<json-args>' | python3 scripts/sanmar.py <action>
```

The action is the **first CLI argument**; arguments are a JSON object on
**stdin**. Each call prints a single JSON object on stdout, or
`{"error": {"type": ..., "message": ...}}` with a non-zero exit code on failure.

The skill is self-contained: no Odoo, no ORM, no `lxml`. It needs Python 3.11+
and `requests`; all XML/SOAP work uses the stdlib `xml.etree.ElementTree`, and
the FTP files are parsed with the stdlib (fixed-width, tab, and pipe layouts —
no `openpyxl`). Three optional installs unlock the file/browser tools:

- `pypdf>=4.0` — required for `parse-po-pdf` (PDF text extraction).
- `paramiko>=3.0` — required for every SFTP-backed tool:
  `lookup-mainframe-color`, the marketing-color auto-resolve fallback in
  `check-inventory` / `get-pricing`, and fetching the FTP feeds behind
  `get-inventory-feed`, `get-shipment-status`, and `parse-invoice-file`
  (only when reading straight off the server rather than a local path/text).
- `playwright>=1.40` — required only for the browser-driven `process-return`
  action (returns are not exposed by any SanMar web service). Also needs a
  browser binary: `python -m playwright install chromium`.

All three are imported lazily, so the skill still loads without them; the
affected tools raise a clear error pointing at the missing `pip install`.

## When to use this skill

Reach for a `scripts/sanmar.py` action when the request involves any of:

- Looking up SanMar product styles, colors, sizes, or images.
- Checking inventory at SanMar warehouses — real-time per-warehouse levels
  (`get-inventory-levels`), a single SKU (`check-inventory`), or a bulk feed
  (`get-inventory-feed`).
- Pulling customer-specific (`myPrice`) pricing for a SKU.
- Validating a draft cart of style/color/size lines before ordering.
- Submitting a SanMar purchase order, or polling its status / tracking.
- Getting tracking numbers and shipment detail for a PO — live
  (`get-tracking`) or from the FTP Daily Shipment Status file
  (`get-shipment-status`).
- Retrieving **invoices** for accounts-payable — by PO, invoice number, order
  date, date range, or all unpaid (`get-invoices`), or parsing the FTP Daily
  Invoice / EDI-810 file (`parse-invoice-file`). Both emit a normalized
  `common` shape that plugs straight into `drivethru-payable-matching`.
- Processing a return for a shipped order (browser-driven portal action).
- Parsing an uploaded PDF purchase order into a structured draft for review.
- Translating a marketing color name (e.g. "Athletic Heather") into SanMar's
  mainframe color code (e.g. "ATHHTHR") when inventory/pricing rejects the
  consumer-facing color.

Do **not** use it for other apparel vendors (S&S, Alpha, etc.), and never
invent SanMar request shapes from prose — call the deterministic actions.

## Actions

Grouped by the four order-lifecycle pillars (plus product/color helpers and
returns). Every action reads credentials from the environment or inline JSON
(see **Credentials**), so those fields are omitted from the table.

**Products & pricing**

| Action | Risk | stdin JSON (key fields) |
| --- | --- | --- |
| `search-products` | read-only | `{style, color?, size?}` |
| `get-pricing` | read-only | `{lines: [{style, color, size}, ...], auto_resolve_color?}` |
| `lookup-mainframe-color` | read-only (SFTP) | `{style, color, size?, force_refresh?}` |

**Inventory**

| Action | Risk | stdin JSON (key fields) |
| --- | --- | --- |
| `check-inventory` | read-only | `{style, color, size, auto_resolve_color?}` — legacy single-SKU port |
| `get-inventory-levels` | read-only | `{style, part_ids?}` — PromoStandards v2, named per-warehouse |
| `get-inventory-feed` | read-only (SFTP/file) | `{style?, path? \| text? \| remote_path?}` — bulk `sanmar_dip.txt` |

**Purchase orders**

| Action | Risk | stdin JSON (key fields) |
| --- | --- | --- |
| `validate-cart` | read-only | `{purchase_order: {...}}` (pre-submit `getPreSubmitInfo`, no commit) |
| `create-purchase-order` | **high — external write** | `{purchase_order: {...}, confirm}` |
| `parse-po-pdf` | read-only (local file) | `{pdf_path}` |
| `cancel-order` | stub | `{po_number, reason?, confirm?}` — SanMar exposes no public cancel endpoint |

**Tracking**

| Action | Risk | stdin JSON (key fields) |
| --- | --- | --- |
| `check-order-status` | read-only | `{po_number}` |
| `get-tracking` | read-only | `{po_number \| sales_order_number \| shipment_date}` — package-level OSN detail |
| `get-shipment-status` | read-only (SFTP/file) | `{path? \| text? \| remote_path?, po_number?}` — FTP ASN file |

**Invoicing**

| Action | Risk | stdin JSON (key fields) |
| --- | --- | --- |
| `get-invoices` | read-only | `{po_number \| invoice_number \| order_date \| (start_date+end_date) \| unpaid, headers_only?}` |
| `parse-invoice-file` | read-only (SFTP/file) | `{path? \| text? \| remote_path?, edi?}` — Daily Invoice / EDI-810 |

**Returns**

| Action | Risk | stdin JSON (key fields) |
| --- | --- | --- |
| `process-return` | **high — portal write (browser)** | `{order_number \| po_number, lines: [{style, color, size, reason, quantity?, details?, replacement?, image_path?}], confirm?}` |

Run `python3 scripts/sanmar.py` with no action to print the full action list.
See [`references/examples.md`](references/examples.md) for realistic prompts and
end-to-end flows. Offline correctness tests for the invoice/tracking/inventory/
feed parsers live in [`scripts/_selftest.py`](scripts/_selftest.py)
(`python3 scripts/_selftest.py`).

## Credentials

SanMar SOAP requests carry three fields: `sanMarCustomerNumber`,
`sanMarUserName`, `sanMarUserPassword`. PromoStandards (order shipment) reuses
the same username/password in its SOAP header.

The skill never hardcodes credentials. Supply them in **either** of two ways:

1. **Environment variables** (preferred for a deployed agent):

   ```bash
   SANMAR_CUSTOMER_NUMBER=...
   SANMAR_USERNAME=...
   SANMAR_PASSWORD=...
   SANMAR_ENV=production        # or "development" — flips PO submit to test-ws
   # SFTP (only for mainframe-color resolution; separate password):
   SANMAR_FTP_USERNAME=<customer_number>   # defaults to SANMAR_CUSTOMER_NUMBER
   SANMAR_FTP_PASSWORD=...
   ```

2. **Inline in the stdin JSON** — pass `customer_number`, `username`,
   `password`, `environment`, and (for SFTP tools) `ftp_password` alongside the
   tool's own arguments. Inline values take precedence over the environment.

If neither is present, the tool exits with
`{"error": {"type": "config_error", ...}}` (exit code 2). In a normal
user-facing turn, treat that as a signal to ask the user for the missing
fields. **On a delegated agent-to-agent turn it means something different — see
[Agent-to-Agent (A2A) mode](#agent-to-agent-a2a-mode) below; do not ask, and do
not go looking for the credentials yourself.** Either way, do not guess
defaults, reuse credentials across tenants, or paste secrets the user did not
provide.

## Agent-to-Agent (A2A) mode

Deploy this skill on a dedicated SanMar agent and let another agent in the org
(e.g. an Accounts Payable or purchasing agent) reach it through a **delegation
connection** in the Knoxville platform. On that kind of turn the SanMar
credentials are **not yours** — they belong to the calling agent, which shares
them with this connection.

**How the credentials reach the skill.** When you handle a delegated call, the
runtime pulls the shared `SANMAR_*` credentials for this conversation and places
them into the skill's **execution environment for this turn only**, before your
`exec` runs. `scripts/sanmar.py` then reads them from the environment exactly as
it would standalone. You do **not** see these values in your context, and that
is by design — they are deliberately kept out of the model prompt.

**So on a delegated turn, just run the tool.** Your first action for a SanMar
request is the `exec` call itself, e.g.:

```bash
echo '{"lines":[{"style":"ST405","color":"...","size":"..."}]}' | python3 scripts/sanmar.py get-pricing
```

Do **not**, before running it:

- call `get_my_bundle`, `get_delegated_credentials`, or any tool to look for or
  "verify" the credentials — they are intentionally invisible to you, so you
  will always find nothing and wrongly conclude you have no access;
- spawn a sub-agent (`sessions_spawn`) or try to delegate this skill's job to
  another session — you are the agent that runs this skill;
- tell the caller you lack credentials or access **before** you have actually
  run the script and read its output.

**If the script itself returns `config_error` / an auth error**, then the
calling connection did not share the credential (or sharing is misconfigured) —
surface that error message to the caller verbatim. Do not ask the user for a key
(on a delegated turn there is no user to ask), and never print a credential
value into the reply.

> **FTP credentials are separate.** Per SanMar's FTP Integration Guide v23.1,
> the SDL feed lives on `ftp.sanmar.com:2200` over **SFTP (SSH)**, and the FTP
> password is issued separately from the web-services password — your
> `sanmar.com` web username will not work on the FTP server.

## Write safety

`create-purchase-order`, `cancel-order`, and `process-return` are the
side-effecting actions.

- `create-purchase-order` requires `"confirm": true` to transmit. Without it,
  it returns a **dry-run** preview of the SOAP envelope and makes no submit
  call. Normal flow: `get-pricing` (to enrich each line with `inventory_key`
  and `size_index`) → `validate-cart` (proceed only if `ok`) →
  `create-purchase-order` with `confirm: true`. Confirm with the user first.
- `cancel-order` is a reserved stub: SanMar's published SOAP and PromoStandards
  bindings expose no cancel operation, so it always returns a structured
  `not_implemented` response. Cancellations go through SanMar customer service.
- `process-return` requires `"confirm": true` to file. Without it, it logs into
  the portal, fills + validates the return form, and returns a `dry_run`
  preview (matched lines + estimated credit/restock) **without submitting**.
  See the next section.

All other actions are pure reads.

## Invoicing

`get-invoices` wraps SanMar's **Standard Invoicing service** (`InvoicePort`).
Pick exactly one query:

- `po_number` — every invoice for a customer PO (the payables match key).
- `invoice_number` — one invoice by its SanMar number.
- `order_date` — invoices for an order date (`yyyy-mm-dd`).
- `start_date` + `end_date` — an invoice-date range (≤ 3 months apart).
- `unpaid: true` — all currently open invoices.

Add `headers_only: true` to skip line items where the query type supports it.

> **Auth note.** InvoicePort authenticates with `CustomerNo` / `UserName` /
> `Password` element names — distinct from the `sanMar*` names the other
> standard ports use. The skill handles this; you pass the same credentials.

> **Timing.** SanMar invoices once per day after 9 p.m. Pacific, and only after
> an order ships. Pull invoice data the day *after* the order date. A PO that
> isn't invoiced yet returns an **empty** result (not an error).

Each returned invoice carries the SanMar-native header + `lines`, **and** a
`common` block — the cross-vendor invoice shape (`source`, `po_number`,
`invoice_number`, `invoice_date`, `due_date`, `is_credit`, `has_lines`, `total`,
`charges` {`merchandise`, `freight`, `freight_allowance`, `sales_tax`},
`lines[]`) — so `drivethru-payable-matching` reconciles a SanMar invoice against
its PO with no SanMar-specific handling. A negative `total` sets
`is_credit: true` (a credit memo — route it to a human / vendor credit, never
bill it).

`parse-invoice-file` produces the **identical** shape from SanMar's FTP invoice
files instead of the API: the fixed-width Daily Invoice `.txt` (default) or the
EDI-810 file (`edi: true`). Supply the file as inline `text`, a local `path`, or
a `remote_path` (SFTP; a directory or omission fetches the newest
`*Invoice_Details*` file from the outbound folder). SanMar states the Daily
Invoice file "shares the same data as the invoicing calls", so it's the batch
alternative to `get-invoices`. See
[`references/invoicing.md`](references/invoicing.md).

## Inventory — three surfaces

- `get-inventory-levels` (**preferred**) — PromoStandards `getInventoryLevels`
  v2.0.0. Returns each part's total plus a **named** per-warehouse breakdown
  (`warehouse_id`, `warehouse_name`, `quantity`). Query a whole style, or pass
  `part_ids` (SanMar unique keys) to limit it.
- `check-inventory` — the legacy `getInventoryQtyForStyleColorSize` port for one
  style/color/size. Returns per-warehouse quantities (unnamed) and a
  `total_available` = the largest single warehouse (SanMar ships complete from
  one warehouse by default). Keeps the marketing→mainframe color auto-resolve.
- `get-inventory-feed` — the bulk `sanmar_dip.txt` SFTP feed (refreshed hourly),
  parsed to per-warehouse rows. Pass `style` to filter — the full feed is large.

## Tracking — live + file

- `get-tracking` — PromoStandards Order Shipment Notification. Query by
  `po_number` (default), `sales_order_number` (SanMar `SO-…`), or
  `shipment_date` (UTC, 7-day window). Returns one package per shipment with
  `tracking_number`, normalized `carrier`, `shipment_method`, `ship_date`, the
  `sales_order_number`, ship-from/to city+state, and the `items` in the box.
- `get-shipment-status` — parses the FTP Daily Shipment Status (Advance Ship
  Notification) file: the same tracking numbers plus per-line **costs**
  (subtotal, freight, handling, invoice total) and box/LPN detail. Supply
  `text` / `path` / `remote_path`; filter to one `po_number`. See
  [`references/shipment_status.md`](references/shipment_status.md).
- `check-order-status` — a lightweight roll-up (SanMar sales-order number +
  shipped/submitted status) for a PO.

## Processing returns (portal / browser)

SanMar exposes **no web service for returns**, so `process-return` drives the
sanmar.com customer portal with Playwright. It needs the optional `playwright`
install plus a browser binary (`python -m playwright install chromium`) and a
**separate portal login** (`SANMAR_PORTAL_USERNAME` / `SANMAR_PORTAL_PASSWORD`,
or inline `portal_username` / `portal_password`) — the web-services credentials
do not authenticate the portal.

Identify the order with `order_number` (the SanMar `SO-…` number — preferred,
since it is unique) or `po_number` (resolved against order history; errors if
the PO maps to more than one order). Each line is
`{style, color, size, reason, quantity?, details?, replacement?, image_path?}`:

- `reason` ∈ `SAMPLES`, `UNWANTED`, `ORDER_INCORRECT`, `INCORRECT_PRODUCT`,
  `DEFECTIVE_DAMAGED`. `UNWANTED` incurs a 20% restock fee.
- `details` (free text) and `replacement` (true/false) are **required** for
  `ORDER_INCORRECT`, `INCORRECT_PRODUCT`, and `DEFECTIVE_DAMAGED`.
- `image_path` (optional) uploads a photo, only for `DEFECTIVE_DAMAGED`.
- `quantity` defaults to the line's originally shipped pieces.

Flow: login → resolve order → open the initiate page → match each requested
line to a row by style/color/size → check item, set quantity, reason, and any
reason-specific fields. Pass `screenshot_path` to capture the filled page.

> **Status — final submit not yet implemented.** The flow is built up to the
> filled, validated form. The final **Continue → review → confirm** submission
> has not been reverse-engineered, so `confirm: true` returns a
> `not_implemented` result (nothing is filed) and `confirm: false` returns a
> `dry_run` preview. See [`references/returns_flow_notes.md`](references/returns_flow_notes.md)
> for the captured selectors and the remaining Step 5 to capture.

## PDF purchase-order intake

`parse-po-pdf` takes `{"pdf_path": "..."}` and returns a best-effort
`ParsedPurchaseOrder`: `po_number`, `order_date`, `ship_method`, `ship_to`,
`lines[]` (`style`, `color`, `size`, `quantity`, `unit_price`), `warnings[]`
for low-confidence fields, and `draft_for_submit` — a ready-to-pass
`purchase_order` object for `create-purchase-order`, populated only when the
parse is complete enough. **Always show the parsed PO back to the user for
approval before submitting.** Heuristic parsing cannot guarantee correctness
across every PO layout — treat the output as a draft.

## Mainframe color resolution

SanMar's inventory/pricing/PO endpoints query against the *mainframe* color
code (e.g. `ATHHTHR`), not the marketing `COLOR_NAME` (`Athletic Heather`).
When a marketing name is used, SanMar typically errors or returns nothing.

`check-inventory` and `get-pricing` auto-handle this: on error or an empty
response (and with `auto_resolve_color` defaulting to `true`) they download
`SanMarPDD/SanMar_SDL_N.csv` over SFTP, look up the matching
`SANMAR_MAINFRAME_COLOR`, and retry once. Pass `auto_resolve_color: false` when
you already have a known mainframe code. For explicit control, call
`lookup-mainframe-color` directly — its `status` is `matched`, `ambiguous`, or
`not_found`. The SDL CSV is cached locally for 24h (SanMar refreshes nightly);
pass `force_refresh: true` to bypass the cache.

## Endpoints

All on host `ws.sanmar.com:8080` in production:

- Pricing — `SanMarWebService/SanMarPricingServicePort`
- Product info — `SanMarWebService/SanMarProductInfoServicePort`
- Inventory (legacy) — `SanMarWebService/SanMarWebServicePort`
- Inventory (PromoStandards v2) — `promostandards/InventoryServiceBinding`
- PO submit — `SanMarWebService/SanMarPOServicePort`
- Order shipment / tracking — `promostandards/OrderShipmentNotificationServiceBinding`
- Invoicing — `SanMarWebService/InvoicePort`
- SFTP data feeds — `ftp.sanmar.com:2200` (SFTP/SSH, **not** TLS)

With `SANMAR_ENV=development`, the **PO submit** and **invoice** endpoints
switch to their `https://test-ws.sanmar.com:8080/...` counterparts; the
read-only pricing/product/inventory/tracking services are production-only.

SanMar must allowlist the calling IP. A connection timeout is most often a
missing IP allowlist entry, not an auth problem. FTP credentials are separate
from web-service credentials (see **Credentials**).

## Error model

Failures print `{"error": {...}}` and exit non-zero:

- `config_error` (exit 2) — missing/invalid credentials.
- `api_error` — SanMar returned a SOAP fault or `errorOccurred=true`. Includes
  `surface`, `operation`, and `retryable`. `retryable` is `false` for auth,
  schema, and invalid-style errors.
- `connection_error` — network/timeout talking to SanMar or its SFTP server
  (`retryable: true` for web-service transport failures).
- `validation_error` — bad input JSON, a missing required field, or an
  unparseable PDF.
- `usage` / `unknown_action` (exit 2) — bad CLI invocation; the message lists
  the valid `actions`.

Surface the human-readable `message` to the user. Do not retry on
`config_error`, `validation_error`, or a non-retryable `api_error`.

## References

- [`references/examples.md`](references/examples.md) — realistic agent prompts
  and end-to-end flows.
- [`references/web_services.md`](references/web_services.md) — SOAP service
  details (pricing, product info, inventory, PO submit, invoicing, tracking).
- [`references/purchase_orders.md`](references/purchase_orders.md) — PO submit
  payload shape and the pre-submit/enrichment flow.
- [`references/invoicing.md`](references/invoicing.md) — the InvoicePort query
  methods, response shape, the normalized `common` payables shape, and the FTP
  Daily Invoice / EDI-810 file formats.
- [`references/shipment_status.md`](references/shipment_status.md) — the OSN
  tracking response and the FTP Daily Shipment Status (ASN) file layout.
- [`references/ftp_feeds.md`](references/ftp_feeds.md) — the SDL/EPDD/dip feeds,
  inventory-by-warehouse, pricing files, and mainframe-color resolution.
- [`references/returns_flow_notes.md`](references/returns_flow_notes.md) — the
  reverse-engineered portal return flow (selectors, reason matrix, step map)
  backing `process-return`.
- [`references/auth_and_patterns.md`](references/auth_and_patterns.md) — auth
  fields and calling patterns.
