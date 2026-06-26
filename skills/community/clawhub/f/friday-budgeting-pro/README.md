# Friday Budgeting Pro

> AI-powered personal finance, on your own machine.

A local budgeting tool that uses AI to do the boring work for you: connecting
to your banks, classifying every transaction, and keeping a spreadsheet
up to date. It runs as a small daemon on your Mac with **multiple equal
ways to interact with it** - no single one is the "main" way.

**Local profiles. Local-only. AI does the heavy lifting; you stay in control.**

Supports multiple named local profiles — each with their own password, linked banks,
ledgers, and transactions. Only one profile can be active at a time (like switching
accounts on a Mac, not a SaaS system).

📐 [Read the architecture](./ARCHITECTURE.md) (this is the source of truth)

---

## How You Use It

The product runs as a small daemon. Three equal-peer ways to interact with
it - pick whichever fits the moment, mix and match freely:

| Adapter | What it covers in v0.1 |
|---|---|
| **🖥️ Web UI** (`127.0.0.1:6789`) | Setup + Profile (settings, password, sync, export, **linked accounts list**) + a minimal **Ledgers** page. |
| **💬 MCP** (OpenClaw, Claude Desktop, any MCP client) | Full feature surface: connect/disconnect banks, edit ledgers, review classifications, query spending, trigger exports. Conversational when paired with an LLM. |
| **⏰ Scheduler** (background) | Daily auto-sync, drift detection, proactive re-auth alerts via your chosen notification channel. |

None of these is "primary." The UI is intentionally small - it handles
setup, the things you tweak occasionally, and bank management. Reviewing
transactions, running queries, and anything fancy still lives in MCP or
the background.

---

## Install

### Production (from registry)

```bash
clawhub install friday-budgeting-pro
```

Installs the latest published version from the ClawHub registry.

### Dev / Local clone

```bash
git clone https://github.com/Riddy21/Friday_Budgeting_Pro bank-transactions
clawhub install ./bank-transactions
# or from anywhere:
clawhub install /path/to/bank-transactions
```

Installs directly from your local clone — skips the registry. Use this when
testing changes before publishing. The same three install hooks fire in both
modes:

| Hook | What it does |
|---|---|
| **pip** | `pip3 install -r requirements.txt` |
| **db-init** | Creates `~/.friday-bp/data.db` (SQLite) |
| **launchd** | Registers the daemon via `server/installer.py`, starts at login |

Either way, once installation completes open `http://127.0.0.1:6789` in your
browser to finish setup.

---

## Connecting to Plaid

1. Create a free account at https://dashboard.plaid.com
2. Team Settings → Keys → copy your **Client ID** and **Production Secret**
3. Ask your OpenClaw agent: `Set up my Plaid credentials — client ID is <your_id>, secret is <your_secret>`
4. Agent writes the config and you're ready to connect banks via the setup wizard.

For sandbox testing, use `env=sandbox` and your sandbox secret instead.

### Supported Banks

The Plaid Link modal supports **any institution Plaid supports in Canada** — there
is no hardcoded allow-list limited to RBC or BMO. You can connect any Canadian bank
or credit union Plaid supports. The integration uses `country_codes=["CA"]` and no
institution filtering.

**Wealthsimple** specifically:

| Product | Plaid support | Notes |
|---|---|---|
| **Wealthsimple Cash** (spending account) | ✅ Supported | Connects through the standard Plaid Link flow, same as any other bank |
| **Wealthsimple Trade / Invest** | ❌ Not via Plaid | Plaid's standard API does not cover Wealthsimple Trade/Invest brokerage accounts. An unofficial API route exists but is not implemented; tracked in issue [#31](https://github.com/Riddy21/Friday_Budgeting_Pro/issues/31) via `server/providers/wealthsimple.py` |

To connect Wealthsimple Cash: use the **+ Connect a bank** button in the UI or
ask your OpenClaw agent to `connect a bank`. Select Wealthsimple in the Plaid
Link modal and authenticate normally.

---

## First Run

When you visit `http://127.0.0.1:6789` for the first time, you see a
small setup wizard (6 short screens):

1. **Set a password** - protects your local dashboard.
2. **Pick how you want to be notified** about ambiguous transactions:
   - "Through OpenClaw chat" (if you use it)
   - "macOS notifications"
   - "Just show me a banner in the UI"
3. **Connect your first bank** - click **+ Connect a bank** and follow
   the Plaid login.
4. **Rental properties** *(optional)* - add any rental properties you want to
   track. Each property gets its own ledger (Rent income, Mortgage, Property tax,
   Maintenance, Insurance, Utilities) and can be linked to a specific bank account
   so its transactions auto-route there.
5. **Investment accounts** *(optional)* - Friday detects Wealthsimple, Questrade,
   and other investment accounts you’ve linked. Check any you want tracked in a
   shared **Investments** ledger.
6. **Done.** Lands on your Dashboard.

The system picks sensible defaults for everything else (Personal ledger
with standard rows, daily 6 AM sync, LLM confidence threshold 0.75).
Adjust any of it later from the Profile page or via MCP.

### Guided onboarding via your agent (issue #206)

After the wizard, your agent can walk you through a short conversational
interview — employer, subscriptions, utilities, rental properties —
then cross-reference your answers against what's actually in your
accounts and generate a personalised set of classification rules tagged
`[onboarding]`.  The whole flow is pure MCP:

- `list_setup_interview_questions` — the canonical question set
- `setup_interview(question_key, answer_text)` — persist an answer
  (upserts on `(user_id, question_key)`)
- `list_setup_interview` — read back the stored answers
- `analyze_recurring_merchants(min_occurrences?, lookback_days?)` —
  surface recurring merchants for the agent to reconcile with the
  interview answers
- `add_rule` / `add_hint` — create personalised rules + hints
- `sync` — re-classify with the new rules

The SKILL.md `onInstall` hook tells the agent to drive this flow
automatically after `clawhub install friday-budgeting-pro` completes.
You can also re-run it at any time by asking your agent to "redo my
Friday setup" or "update my profile".

---

## What the UI Looks Like (v0.1)

Three things, kept minimal:

**Setup wizard** - once, on first launch.

**Profile page** - the main ongoing page. Has:
- Display name + notification preference + LLM confidence slider
- Change password
- Log out
- Read-only system info (Plaid env, last sync time, daemon uptime)
- **Sync now** button
- **Export to Excel** button — available as a browser download at `/export/excel` (streams the workbook directly to your browser without saving to disk)
- **Linked Accounts** - compact list of connected banks with status pills
  and **Reconnect / Disconnect / + Connect a bank** buttons. No fancy
  cards, just a list.

**Ledgers page** - structure editor with drilldown. List your ledgers (default:
Personal), click into one to add/rename/remove line items, add new
ledgers when you need them (e.g. for a rental property). Each line item shows
its running total and transaction count; click to expand and see the individual
transactions classified to it (populated once auto-categorisation is active).

A **date range filter** at the top of the page lets you scope all totals to a
preset period: *This month* (default), *Last month*, *Last 3 months*, *This year*,
or *All time*. The selected period is reflected in the URL (`/ledgers?period=…`)
so views are shareable and bookmarkable.

Each ledger shows an **income vs expense breakdown**: line items are split into
an *Income* section and an *Expenses* section, with a footer row showing total
income, total expenses, and the **net** (income − expenses). The net is
highlighted green when positive (surplus) and red when negative (deficit).

Ledgers come in three types:
- **Personal** (default) — standard household budget with line items like Salary, Groceries, Dining, etc.
- **Property** — rental/investment property ledger with pre-seeded items: Rent income, Mortgage, Property tax, Maintenance & repairs, Insurance, Utilities.
- **Investment** — tracks investment accounts with Contributions and Dividends & Returns.

Create typed ledgers via MCP: `create_property_ledger('123 Main St')` or `create_investment_ledger('TFSA')`.
Link a bank account to a ledger so its transactions route there by default: `set_account_ledger(account_id, ledger_id)`.

Reviewing classifications, running queries, anything beyond the basics -
those still happen through the MCP adapter (your OpenClaw agent or any
other MCP client).

---

## What AI Does for You

After every sync, `classify_pending_transactions` automatically routes all
newly imported transactions into your ledger line items.  No manual step
needed — just sync and your budget is up to date.

Every transaction goes through **one unified LLM call** that combines
rules-first evaluation and free-form reasoning into a single prompt
_(issue #205)_:

1. **Unified classification** - the LLM sees your priority-ordered
   `classification_rules`, your full ledger tree, your hints, recent
   reviewed entries for the same merchant, the account name +
   description, and any transfer-detection hint — all in one shot.
   It tries the first matching rule; if none clearly apply, it picks the
   best line item from the ledger tree using the other context.
   Returns `rule_id`, `line_item_id`, `classification_type`, `confidence`,
   and `reasoning`.  When confidence < 0.7 the result is flagged as
   `uncertain`.
2. **Review queue** - if it's unsure or the LLM couldn't route it, the
   transaction lands in a review queue (`get_needs_review`).  You'll get
   a notification through your chosen channel.

**Transfer detection**: before classification, each transaction is checked
against internal transfer pairs (same amount, different accounts, within
3 days). Detected transfers are passed as context to the LLM so they are
classified as `transfer` rather than `spending`.

After 3 successful classifications of the same merchant, it becomes a
Tier 1 legacy rule automatically. The longer you use it, the less it asks.

### Classification Rules

Friday ships with **6 built-in (default) classification rules** that run before
the LLM sees a transaction.  They handle the most common patterns automatically:

| Priority | Rule | What it does |
|----------|------|--------------|
| 1 | **Pending skip** | Skips any transaction still marked pending |
| 10 | **Internal transfer** | Flags same-amount cross-account moves within 3 days as Transfer |
| 20 | **Investment contribution** | Marks outflows to Wealthsimple, Questrade, etc. as Transfer/Savings |
| 30 | **Credit card payment** | Identifies chequing→credit payments as Transfer (charges already tracked) |
| 40 | **Salary / payroll** | Marks bank-tagged payroll transactions as Income |
| 50 | **Bank fees** | Marks monthly account fees as Bank Fees (spending) |

Default rules can be **disabled** but not deleted.  You can add your own rules
(priority 100+) and reorder them via MCP tools: `list_rules`, `add_rule`,
`update_rule`, `reorder_rules`, `disable_rule`, `enable_rule`, `delete_rule`.

All active rules are visible in the **Settings page** (`/settings`) under
*Classification Rules*, shown in priority order.  The table is read-only —
editing is done via MCP/chat.

### Correcting Classifications via Chat

If a transaction is classified wrong, just tell your AI assistant:

```
You:    That $42 Uber from last Tuesday was an airport trip, not a regular ride.
Agent:  Got it — I'll reclassify it as Travel.
        Should I also create a rule so future Uber charges over $40 are
        automatically marked as Travel?
You:    Yes please.
Agent:  Done! Uber transactions will now be routed to Travel automatically.
```

Under the hood the agent uses `find_transactions` to locate the right
transaction (fuzzy match on merchant, date, and amount) and
`correct_transaction` to update the classification and optionally create a
priority-80 rule.  Every correction is audited: the original
`line_item_id` is preserved in `corrected_from_line_item_id` and the
timestamp is recorded in `corrected_at`.

---

## With OpenClaw (and any other MCP client)

The MCP adapter exposes the full feature set. Through OpenClaw or any
MCP-capable client:

```
You:    How's this month looking?
Agent:  May 2026 so far:
        Income:    $6,500
        Expenses:  $3,247
        Top: Groceries $487, Dining $312, Subscriptions $89
        Net: +$3,253

You:    Connect another bank
Agent:  Opening Plaid Link at http://127.0.0.1:6789/link?t=...
        - let me know when you're done.

You:    Export this year to Excel
Agent:  ✓ Wrote Personal Finances.xlsx to your Documents folder.

Agent:  Heads up - got a $312 Costco charge from yesterday that I'm
        not sure about. Personal groceries, or something else?
You:    Half personal groceries, half supplies for work
Agent:  ✓ Split 50/50, saved as a hint for similar charges.
```

Same engine, just a different way in. Other MCP clients (Claude Desktop,
Cursor, mcporter on the CLI) work too - anywhere you can call MCP tools.

---

## Privacy & Security

- 🏠 **Local-only.** Nothing this app runs is reachable from the public
  internet. Everything binds to `127.0.0.1`.
- 🔒 **Plaid bank tokens encrypted at rest** (Fernet, key in macOS Keychain)
- 🔑 **Password hashed with argon2id**, never sent to the browser
- 📁 **Your data lives in `~/.friday-bp/data.db`** (SQLite, yours)
- 🚫 **No telemetry**, no cloud sync, no third parties except Plaid + your
  chosen LLM
- ⏱️ **Sessions persist until you log out** - no idle timeout
- 🔄 **Bank sync runs in the background regardless** of whether you're logged into the UI

### How credentials and access tokens work

Friday stores two distinct kinds of Plaid secret, treated differently:

**Plaid API credentials** (`client_id` + `secret` from your Plaid dashboard)
- Stored in the `plaid_config` table in the local SQLite DB, scoped per
  profile. When you run `configure_plaid`, it's saved there first.
- Also written to a `.env` file (mode `0600`) so the daemon can load them
  on cold start, before any user logs in.
- Stored in **plaintext** — this is intentional. API credentials are
  developer-identifying, not account-level. They grant no bank access on
  their own and rotate instantly from the Plaid dashboard if needed.
- Resolution order at runtime: DB row for the active user → `.env` env vars.

**Per-bank access tokens** (from Plaid Link after you connect a bank)
- **Never stored in plaintext.** Encrypted with Fernet before hitting disk.
- The Fernet key lives in macOS Keychain (`keyring` lib), never in any file.
- A stolen `.db` without the Keychain entry cannot decrypt any access token.

See [ARCHITECTURE.md § Security](./ARCHITECTURE.md#security) for the full
threat model and design rationale.

---

## Multi-Currency Support

Friday Budgeting Pro stores and displays amounts in each account's native currency:

- **Currency stored at sync time** — `bank_accounts.currency` and `transactions.currency` are populated from Plaid's `iso_currency_code` during every sync
- **Prefix on every balance** — `C$` for CAD, `US$` for USD, `£` for GBP, `€` for EUR, ISO code for others
- **FX conversion** — coming in a follow-up PR (amount_home, frankfurter.app rates, home-currency toggle)

---

## What This Is Not (v0.1)

- Not a full web app. The UI is deliberately small: setup and profile only.
- Not a SaaS. Everything runs on your Mac, no cloud account.
- Not a generalized platform. Personal finances only.
- Not chat-only either. MCP is one of several equal-peer ways in.

---

## Testing

The regular test suite runs with pytest and needs no extra deps:

```bash
python3 -m pytest -q
```

### Browser tests (optional)

UI tests use Playwright and are **skipped automatically** when Playwright is not
installed, so CI is never broken by a missing dep. To activate them locally:

```bash
pip install playwright
playwright install chromium
python3 -m pytest tests/ui/
```

---

## Troubleshooting

**"Bank connection broken"** → Ask your OpenClaw agent (or any MCP client)
to reconnect that bank; it'll return a Plaid Link URL you click to fix.

**"I forgot my password"** → On the login page, click "Forgot password".
A recovery token is written to `~/.friday-bp/recovery.txt` (only you can
read it). Copy it into the reset page to set a new one.

**"Where's my data?"** → `~/.friday-bp/data.db`. Back it up.

**"The UI isn't loading"** → Check the daemon is running:
`launchctl list | grep friday-budgeting-pro`. Restart with
`launchctl kickstart -k gui/$UID/ai.openclaw.friday-budgeting-pro`.

**"How do I uninstall?"** → `clawhub uninstall friday-budgeting-pro`.
Your data file stays unless you delete it manually.

### Proactive Re-Auth Alerts

Friday will proactively notify you when a bank connection needs attention.
During the daily 06:00 sync, it checks for connections in these states:

- **`needs_reauth`** — Plaid login has expired (e.g. you changed your bank password).
  > ⚠️ Your BMO Bank of Montreal connection needs re-authorization. Say 'reconnect BMO Bank of Montreal' to open the re-auth flow.

- **`pending_expiration`** — Token is about to expire (some institutions rotate tokens).
  > ⚠️ Your TD Bank connection expires soon. Say 'reconnect TD Bank' to refresh it.

- **Never synced** — A connection was added but sync has never run.
  > ⚠️ Your Scotiabank connection needs re-authorization. Say 'reconnect Scotiabank' to open the re-auth flow.

Alerts are throttled to at most once every 24 hours per connection so you
won't be spammed. You can also ask your agent directly:
> "Do any of my bank connections need attention?"

and it will call `get_connections_needing_attention` and report back.

---

## License

MIT
