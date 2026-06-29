---
name: amazon-sp-api
description: "Amazon Seller Central SP-API wrapper (Python) — orders, catalog, FBA inventory, reports (incl. restock recommendations), and financial events. SigV4 + LWA refresh handled internally; works with any marketplace and region."
homepage: https://developer-docs.amazon.com/sp-api/
metadata:
  {
    "openclaw":
      {
        "emoji": "🛒",
        "requires":
          {
            "bins": ["python3"],
            "env":
              [
                "AMAZON_SP_API_REFRESH_TOKEN",
                "AMAZON_SP_API_CLIENT_ID",
                "AMAZON_SP_API_CLIENT_SECRET",
                "AMAZON_SP_API_AWS_ACCESS_KEY_ID",
                "AMAZON_SP_API_AWS_SECRET_ACCESS_KEY",
              ],
          },
        "primaryEnv": "AMAZON_SP_API_REFRESH_TOKEN",
      },
  }
---

# Amazon Seller Central — SP-API

Run the bundled `scripts/amazon_api.py` for every Amazon SP-API operation. The script handles the full LWA refresh + AWS SigV4 signing chain internally so the agent only ever deals with structured JSON.

```bash
python3 "{baseDir}/scripts/amazon_api.py" <command> [options]
```

Background: Amazon's Selling Partner API (SP-API) is the replacement for MWS. Auth needs two layers — an LWA refresh token for `x-amz-access-token`, and IAM credentials for SigV4 request signing. Both are required for every call. Tokens auto-refresh; the agent does not.

## First run — install the one Python dependency

The script uses [`httpx`](https://www.python-httpx.org/). If a command fails with `ModuleNotFoundError: No module named 'httpx'`, install it once:

```bash
python3 -c "import httpx" || python3 -m pip install httpx
```

## Setup

Set five required env vars. The cleanest place is your shell rc or your secrets manager (1Password CLI, direnv, systemd EnvFile, etc.). **Never** paste secrets into chat.

```bash
export AMAZON_SP_API_REFRESH_TOKEN="Atzr|…"          # LWA refresh token
export AMAZON_SP_API_CLIENT_ID="amzn1.application-oa2-client.…"
export AMAZON_SP_API_CLIENT_SECRET="…"
export AMAZON_SP_API_AWS_ACCESS_KEY_ID="AKIA…"       # IAM user with SP-API role assumed
export AMAZON_SP_API_AWS_SECRET_ACCESS_KEY="…"
```

Two optional knobs (sensible defaults — UK marketplace, EU region):

```bash
export AMAZON_SP_API_MARKETPLACE_ID="A1F83G8C2ARO7P"  # default: UK
export AWS_REGION="eu-west-1"                          # default: EU endpoint
```

Region → endpoint mapping the script uses:

| AWS_REGION    | SP-API endpoint                              | Region label |
|---------------|----------------------------------------------|--------------|
| `us-east-1`   | `https://sellingpartnerapi-na.amazon.com`    | NA           |
| `eu-west-1`   | `https://sellingpartnerapi-eu.amazon.com`    | EU (default) |
| `us-west-2`   | `https://sellingpartnerapi-fe.amazon.com`    | Far East     |

Marketplace ids: <https://developer-docs.amazon.com/sp-api/docs/marketplace-ids>.

## Workflow rules

1. **Start with `--summary` on every list command.** SP-API responses are big and lossy to read in full — only drop `--summary` after you've narrowed to specific ids.
2. **Filter at the API.** Every list command exposes the same filters as Seller Central (`--status`, `--since`, `--type`, `--skus`). Push them down; don't paginate everything.
3. **Reports are async.** `reports`/`create-report`/`get-report`/`get-report-document` are the four-step ritual. For restock specifically, use the `restock-report` shortcut — it does create → poll-every-10s → download in one call.
4. **Token caching is in-process only.** Each script invocation refreshes LWA once and caches for ~1 hour, but nothing is persisted to disk — there are no secrets on the filesystem after the process exits.

## Commands

### Orders

```bash
python3 "{baseDir}/scripts/amazon_api.py" orders --summary
python3 "{baseDir}/scripts/amazon_api.py" orders --status Unshipped --summary
python3 "{baseDir}/scripts/amazon_api.py" orders --since 2026-01-01 --summary
python3 "{baseDir}/scripts/amazon_api.py" orders --status Shipped --since 2026-01-01 --limit 50

python3 "{baseDir}/scripts/amazon_api.py" order <AmazonOrderId>
python3 "{baseDir}/scripts/amazon_api.py" order-items <AmazonOrderId> --summary
```

Status values: `Unshipped`, `PartiallyShipped`, `Shipped`, `Canceled`, `Pending`, etc.

### Catalog

```bash
python3 "{baseDir}/scripts/amazon_api.py" catalog-item <ASIN>
```

### FBA Inventory

```bash
python3 "{baseDir}/scripts/amazon_api.py" inventory --summary
python3 "{baseDir}/scripts/amazon_api.py" inventory --skus "SKU1,SKU2" --summary
```

### Reports

```bash
# List existing report runs
python3 "{baseDir}/scripts/amazon_api.py" reports --summary
python3 "{baseDir}/scripts/amazon_api.py" reports --type GET_FLAT_FILE_OPEN_LISTINGS_DATA --summary

# Kick off a new report
python3 "{baseDir}/scripts/amazon_api.py" create-report --type GET_FLAT_FILE_OPEN_LISTINGS_DATA
python3 "{baseDir}/scripts/amazon_api.py" create-report \
    --type GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL --start 2026-01-01 --end 2026-01-31

# Poll until it's DONE
python3 "{baseDir}/scripts/amazon_api.py" get-report <reportId>

# Download + parse the report document (TSV → JSON)
python3 "{baseDir}/scripts/amazon_api.py" get-report-document <reportDocumentId>
python3 "{baseDir}/scripts/amazon_api.py" get-report-document <reportDocumentId> --output report.tsv
```

### Restock Inventory Report (single-shot)

```bash
# Creates report, polls until done, downloads — all in one step
python3 "{baseDir}/scripts/amazon_api.py" restock-report
python3 "{baseDir}/scripts/amazon_api.py" restock-report --output restock.tsv
```

Output fields: Product Name, SKU, ASIN, FNSKU, sales over last 30 days, units sold, available, inbound, total units, days of supply, recommended replenishment qty, recommended ship date, alert status. Use this rather than re-implementing the create/poll/download loop.

### Finances

```bash
python3 "{baseDir}/scripts/amazon_api.py" finances --since 2026-01-01
python3 "{baseDir}/scripts/amazon_api.py" finances --order-id <AmazonOrderId>
python3 "{baseDir}/scripts/amazon_api.py" finances --since 2026-01-01 --limit 50
```

## Common report types

| Report type                                          | What it is                                         |
|------------------------------------------------------|----------------------------------------------------|
| `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`       | Restock recommendations (use `restock-report` shortcut) |
| `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`            | Active FBA inventory details                       |
| `GET_FBA_MYI_ALL_INVENTORY_DATA`                     | All FBA inventory (incl. archived)                 |
| `GET_AFN_INVENTORY_DATA`                             | FBA inventory quantities                           |
| `GET_FBA_INVENTORY_PLANNING_DATA`                    | Inventory planning (aged, excess, fees)            |
| `GET_FLAT_FILE_OPEN_LISTINGS_DATA`                   | Active listings (flat file)                        |
| `GET_MERCHANT_LISTINGS_ALL_DATA`                     | All listings                                       |
| `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL`        | FBA shipments                                      |
| `GET_LEDGER_SUMMARY_VIEW_DATA`                       | Inventory ledger (reconciliation)                  |
| `GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE`          | Returns                                            |
| `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE`            | Settlement reports                                 |

Full list: <https://developer-docs.amazon.com/sp-api/docs/report-type-values>.

## Output shape

Every list command emits:

```json
{ "count": N, "<resource>": [ … ] }
```

`<resource>` matches the command name (`orders`, `items`, `inventory`, `reports`). Single-record commands print the resource directly. Errors print `{ "error": "...", "detail": "..." }` with a non-zero exit status.

## Useful patterns

- **Daily ops health-check.** `orders --status Unshipped --summary` for the queue, then `inventory --summary` for stock posture, then `finances --since <today-1>` for settlement deltas.
- **Restock planning.** `restock-report --output restock.tsv` — one command, agent gets back the parsed rows ready for spreadsheet aggregation or chart rendering.
- **Reconcile a single order's money flow.** `order <id>` then `order-items <id>` then `finances --order-id <id>` shows what was sold, what shipped, and what Amazon paid out for that specific order.

## Notes

- **Rate limits** are per-endpoint and tight. The script retries 429 with the server-provided `Retry-After`.
- **Region drift.** If you set `AWS_REGION` to a value not in the table above, the script falls back to the EU endpoint. Override with one of the three known regions to be explicit.
- **Reports are eventually consistent.** A `DONE` report can take several minutes for large date ranges. `restock-report` polls for up to 10 minutes (60 polls × 10s); beyond that, fall back to `create-report` + `get-report`/`get-report-document` and poll on your own schedule.
- **Endpoint docs:** <https://developer-docs.amazon.com/sp-api/>.

Always invoke `scripts/amazon_api.py` for SP-API work in this skill — do not hand-roll SigV4 or LWA calls, always start list commands with `--summary`, and surface errors verbatim instead of guessing — that is how this skill is meant to be used.
