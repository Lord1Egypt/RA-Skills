---
name: creditkarma-mcp
description: Access Credit Karma transaction data via MCP. Use when the user asks about their Credit Karma transactions, spending by category or merchant, account summaries, or wants to sync or query their financial data. Triggers on phrases like "sync my transactions", "what did I spend on", "show my Credit Karma data", "spending by category", "top merchants", or any request involving personal finance data from Credit Karma. Requires creditkarma-mcp installed and the creditkarma server registered (see Setup below).
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

**1. fetchproxy extension (easiest — no env vars):** Install the [fetchproxy 0.3.0 extension](https://github.com/chrischall/fetchproxy), sign into creditkarma.com once, and leave `CK_COOKIES` **unset**. The MCP reads HttpOnly `CKAT` + `CKTRKID` cookies on the first tool call via `chrome.cookies.get`, then operates direct-to-API from Node.

**2. ck_set_session MCP tool:** From within Claude, call `ck_set_session` with a Cookie header you copied from DevTools (see below). The tool persists it to `.env`.

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

### Sync
| Tool | Description |
|------|-------------|
| `ck_sync_transactions(force_full?)` | Sync transactions to local SQLite. Incremental by default (since last sync − 30 days). `force_full=true` re-fetches everything. |

### Query
| Tool | Description |
|------|-------------|
| `ck_list_transactions(start_date?, end_date?, account?, category?, merchant?, status?, min_amount?, max_amount?, limit?, offset?)` | Filtered, paginated transaction list |
| `ck_get_recent_transactions(limit?)` | N most recent transactions (default 20) |
| `ck_get_spending_by_category(start_date?, end_date?)` | Spending totals grouped by category |
| `ck_get_spending_by_merchant(start_date?, end_date?, limit?)` | Spending totals grouped by merchant |
| `ck_get_account_summary` | Transaction counts and totals per account |
| `ck_query_sql(sql)` | Read-only SQL query against the local database (SELECT only) |

## Workflows

**First-time setup:**
1. Easiest: install the [fetchproxy extension](https://github.com/chrischall/fetchproxy), sign into creditkarma.com, leave `CK_COOKIES` unset.
2. Or: copy the Cookie header from DevTools and either set `CK_COOKIES` in your config or call `ck_set_session(cookies)` from within Claude.
3. `ck_sync_transactions` → initial full sync

**Regular use:**
- `ck_sync_transactions` → pull latest transactions
- Then query with any of the query tools

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
accounts     (id, name, type, provider_name, display)
categories   (id, name, type)
merchants    (id, name)
sync_state   (key, value)
```

## Notes

- All query tools run against the local SQLite database — sync first
- Amounts: negative = expense/debit, positive = credit/income
- `ck_query_sql` only allows SELECT — no writes to Credit Karma data
- Sync saves a resume cursor — interrupted syncs can be resumed automatically
- `accounts.id` is a synthesized stable key in the form `<provider>|<last4>` (e.g. `Citi|2630`, `Ally|7133`) because CK's API returns empty `account.id` strings. The same card under two provider-name spellings shows as two rows.
