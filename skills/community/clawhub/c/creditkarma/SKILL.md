---
name: creditkarma
description: Access Credit Karma transaction data via MCP. Use when the user asks about their Credit Karma transactions, spending by category or merchant, account summaries, account balances, or wants to sync or query their financial data. Triggers on phrases like "sync my transactions", "what did I spend on", "show my Credit Karma data", "spending by category", "top merchants", or any request involving personal finance data from Credit Karma. Requires creditkarma-mcp installed and the creditkarma server registered (see Setup below).
---

# creditkarma-mcp

MCP server for Credit Karma — syncs transactions into a local SQLite database and provides natural-language querying tools.

- **npm:** [npmjs.com/package/creditkarma-mcp](https://www.npmjs.com/package/creditkarma-mcp)
- **Source:** [github.com/chrischall/creditkarma-mcp](https://github.com/chrischall/creditkarma-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "creditkarma": {
      "command": "npx",
      "args": ["-y", "creditkarma-mcp"],
      "env": {
        "CK_COOKIES": "CKTRKID=...; CKAT=eyJ...%3BeyJ...; ..."
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/creditkarma-mcp
cd creditkarma-mcp
npm install && npm run build
```

Then add to `.mcp.json`:

```json
{
  "mcpServers": {
    "creditkarma": {
      "command": "node",
      "args": ["/path/to/creditkarma-mcp/dist/index.js"],
      "env": {
        "CK_COOKIES": "CKTRKID=...; CKAT=eyJ...%3BeyJ...; ..."
      }
    }
  }
}
```

Or use a `.env` file in the project directory with `CK_COOKIES=<value>`.

### Getting CK_COOKIES (optional)

Three onboarding paths, in priority order:

**1. ContextMint Bridge extension (easiest — no env vars):** Install [ContextMint Bridge](https://github.com/nullnet-app/contextmint-bridge/releases) (Chrome: load the chrome zip unpacked; Safari: ships inside the ContextMint app, which has no public download yet — use Chrome for now). It is the fetchproxy extension renamed, same maintainer; source is public at https://github.com/nullnet-app/contextmint-bridge — build it, or check the release zip with `shasum -a 256 -c <zip>.sha256`. Then sign into creditkarma.com once, and leave `CK_COOKIES` **unset**. The MCP reads HttpOnly `CKAT` + `CKTRKID` cookies on the first tool call via `chrome.cookies.get`, then operates direct-to-API from Node.

**2. ck_set_session MCP tool:** From within Claude, call `ck_set_session` with a Cookie header you copied from DevTools (see below). The tool saves it to `~/.creditkarma-mcp/session` (0600), which the server reads back on every start.

**3. Manual (DevTools):**
1. Log in to [creditkarma.com](https://www.creditkarma.com) in Chrome
2. DevTools → **Network** → any creditkarma.com request → **Request Headers**
3. Right-click the `cookie` header → **Copy value**
4. Paste into `CK_COOKIES` in your Claude config

## Authentication

The MCP handles auth automatically once any of the three paths is configured.

- Access token: ~15 min TTL, auto-refreshed transparently
- Refresh token: ~8 hours TTL
- When expired:
  - **fetchproxy path:** sign back into creditkarma.com — the MCP reads fresh cookies on the next tool call
  - **env-var / ck_set_session path:** grab a fresh Cookie header from DevTools and update `CK_COOKIES` (or call `ck_set_session` again)

## Tools

### Auth
| Tool | Description |
|------|-------------|
| `ck_set_session(cookies)` | Store credentials — paste the full Cookie header from a signed-in creditkarma.com request |
| `ck_forget_session()` | Delete the saved-session file and clear in-memory credentials (local only; transactions DB kept) |

### Sync
| Tool | Description |
|------|-------------|
| `ck_sync_transactions(force_full?)` | Sync transactions to local SQLite. Incremental by default (since last sync − 30 days). `force_full=true` walks the whole history with no date cutoff — from the beginning, except that it continues a backfill paused by `max_pages`; after a failed or stuck sync it restarts from page 1. |

### Query
| Tool | Description |
|------|-------------|
| `ck_list_transactions(start_date?, end_date?, account?, category?, merchant?, status?, min_amount?, max_amount?, limit?, offset?, view?)` | Filtered, paginated transaction list, newest first; `view: "brief"` answers one line per transaction (`<merchant> <signed amount> — <date> — <status>`) |
| `ck_get_recent_transactions(limit?)` | N most recent transactions (default 25; `limit` on every listing tool is a whole number from 1 to 500, `offset` 0 or more) |
| `ck_get_spending_by_category(start_date?, end_date?, account?)` | Spending totals grouped by category |
| `ck_get_spending_by_merchant(start_date?, end_date?, category?, limit?)` | Spending totals grouped by merchant |
| `ck_get_account_summary` | Transaction counts and totals per account |
| `ck_get_account_balances(refresh?, include_matched?)` | Balance per account: institution, type, last 4, current balance, available credit and credit limit (cards), `balance_as_of`, `source` (`linked` — live from the aggregator, cards and loans included — or `credit_report`) and `stale`. Liabilities are negative. Prefer `linked` figures; credit-report balances lag 2–5 weeks — say so when quoting one. A credit-report row duplicating a linked account is hidden unless `include_matched` |
| `ck_query_sql(sql, max_rows?)` | Read-only SQL query against the local database (SELECT only; at most `max_rows` rows, default 500 / max 5000 — `truncated: true` means page with LIMIT/OFFSET or aggregate) |

## In context groups

On a host with context groups (mcp-host), every tool here except `ck_healthcheck` is in the **money** group.

- **Canonical read:** `ck_list_transactions` answers the group's *what's new* ask ("any new charges this week?"), over its `start_date`/`end_date` range, in its `brief` view. It takes no subject: one call covers every account, so the group never fans out per account.
- Nothing here answers *what's due* or *what's on* — Credit Karma's data carries no bill due dates — so those asks name no Credit Karma source.
- A compound ask spans groups: "what came in at school today, and any new charges?" asks school's sources and this one in one answer.
- The canonical read is the local database, so it is as fresh as the last `ck_sync_transactions`. This is a browser-bridged MCP (sign-in is read through ContextMint Bridge): when the bridge is not connected, the group answers that Credit Karma needs your browser open rather than calling it.

## Workflows

**First-time setup:**
1. Easiest: install [ContextMint Bridge](https://github.com/nullnet-app/contextmint-bridge/releases), sign into creditkarma.com, leave `CK_COOKIES` unset.
2. Or: copy the Cookie header from DevTools and either set `CK_COOKIES` in your config or call `ck_set_session(cookies)` from within Claude.
3. `ck_sync_transactions` → initial full sync

**Regular use:**
- `ck_sync_transactions` → pull latest transactions
- Then query with any of the query tools

**Balances:**
```
ck_get_account_balances                # last synced balances (ck_sync_transactions refreshes them)
ck_get_account_balances(include_matched: true)  # also show credit-report duplicates of linked accounts
ck_get_account_balances(refresh: true) # fetch live first
```

**Spending analysis:**
```
ck_sync_transactions
ck_get_spending_by_category(start_date: "2026-01-01", end_date: "2026-03-31")
ck_get_spending_by_merchant(start_date: "2026-01-01", limit: 10)
```

**Custom analysis with SQL:**
```sql
-- Monthly spending totals
SELECT strftime('%Y-%m', date) AS month, SUM(ABS(amount)) AS total
FROM transactions WHERE amount < 0
GROUP BY month ORDER BY month DESC

-- Spending by category this year
SELECT c.name, SUM(ABS(t.amount)) AS total
FROM transactions t JOIN categories c ON t.category_id = c.id
WHERE t.date >= '2026-01-01' AND t.amount < 0
GROUP BY c.name ORDER BY total DESC
```

## Database schema

```sql
transactions (id, date, description, status, amount, account_id, category_id, merchant_id, raw_json)
accounts     (id, name, type, provider_name, display, last4, account_urn,
              current_balance, available_balance, credit_limit,
              balance_as_of, balances_synced_at, balance_source, matched_account_id)
account_aliases (alias, account_id)
categories   (id, name, type)
merchants    (id, name)
sync_state   (key, value)
```

## Notes

- All query tools run against the local SQLite database — sync first
- Amounts: negative = expense/debit, positive = credit/income
- `ck_query_sql` only allows SELECT — no writes to Credit Karma data
- Sync saves a resume cursor — interrupted syncs can be resumed automatically
- `accounts.id` is a synthesized stable key in the form `<provider>|<last4>` (e.g. `Citi|2630`, `Ally|7133`) because CK's API returns empty `account.id` strings. The same card seen under two provider-name spellings (e.g. `X` vs `X - Credit Card`) is folded into one row: the account URN, or an `account_aliases` entry, resolves both spellings to the same id.
