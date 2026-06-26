---
name: friday-budgeting-pro
description: >
  AI-powered personal finance tracker. Connects to your banks via Plaid,
  auto-classifies transactions, syncs daily, and exports to Excel. Supports
  multiple ledgers including personal household, rental properties, and
  investments. Ask your agent about spending, connect banks, manage ledgers,
  classify transactions, or trigger exports.
homepage: https://github.com/Riddy21/Friday_Budgeting_Pro
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "os": ["darwin"],
        "requires": { "bins": ["python3"] },
        "mcp":
          {
            "server": "friday-budgeting-pro",
            "transport": "stdio",
            "command": "python3",
            "args": ["-m", "server.main"],
          },
        "install":
          [
            {
              "id": "pip",
              "kind": "shell",
              "command": "pip3 install --break-system-packages -q -r requirements.txt",
              "label": "Install Python dependencies",
            },
            {
              "id": "db-init",
              "kind": "shell",
              "command": "python3 -c \"import server.db as d, server.paths as p; d.init_db(p.DB_PATH)\"",
              "label": "Initialize database",
            },
            {
              "id": "launchd",
              "kind": "shell",
              "command": "python3 -m server.installer install",
              "label": "Install daemon (launchd plist + OpenClaw MCP registration)",
            },
          ],
        "uninstall":
          [
            {
              "id": "launchd-remove",
              "kind": "shell",
              "command": "python3 -m server.installer uninstall",
              "label": "Remove daemon",
            },
          ],
        "onInstall":
          "Friday Budgeting Pro is installed.  Walk the user through the guided onboarding flow:\n1. Call setup_status — if not 'complete', send the URL from get_ui_url() and instruct the user to complete the 3-step browser wizard (set a password, pick a notification channel, and optionally connect their first bank).  Poll setup_status until it returns 'complete'.\n2. Once the wizard is done and an initial sync has run, run the personalisation interview.  Use list_setup_interview_questions to get the canonical question list, then ask each one conversationally (skip ones the user already volunteered).  Call setup_interview(question_key, answer_text) to persist each answer.\n3. Call analyze_recurring_merchants to cross-reference the user's interview answers with recently-synced transactions.  Reconcile gaps (e.g. user mentioned Netflix but it's not in transactions yet, or there's a recurring charge they didn't mention).\n4. For each identified pattern, propose and create a classification rule via add_rule (use a description that starts with '[onboarding]' so the user can see what was auto-generated) and add classification hints via add_hint.  Examples: 'Deposits from TENSTORRENT are Salary & Income', 'Disney Plus charges are Entertainment & Subscriptions'.\n5. Call sync once more so the newly-installed rules classify any remaining transactions, then call get_needs_review_summary and, if count > 0, present the summary field to the user in one message.\n6. After setup the user can add rental properties or investment ledgers at any time via natural language ('add a ledger for my 123 Main St rental', 'track my Wealthsimple account') — use create_property_ledger / create_investment_ledger as needed.  They can also update classification rules ('add a rule that Home Depot over $200 goes to Rental Maintenance') via add_rule / update_rule / delete_rule.  No UI needed for any of this.",
      },
  }
---

# Friday Budgeting Pro

AI-powered personal finance on your own Mac. Connects to your banks via Plaid,
classifies transactions automatically (and asks when unsure), syncs in the
background, and exports to Excel. Supports personal, rental property, and
investment ledgers. A small local UI handles setup and management; everything
else happens through your agent.

## Setup

After install, open `http://127.0.0.1:6789` in your browser to:
1. Set a password for the local dashboard
2. Connect your first bank via Plaid
3. Done — daily sync runs automatically via launchd

## Sync Pipeline & LLM Classification

Every `sync()` call runs the full pipeline automatically in one shot:

```
Plaid fetch → rule-based classification → LLM classification → review queue
```

1. **Plaid fetch** — pulls added/modified/removed transactions via cursor-based incremental sync
2. **Rule classification** — auto-promoted `routing_rules` match instantly (no LLM cost)
3. **LLM classification** — `classify_pending_transactions` runs on anything rules didn't catch;
   each transaction gets one unified LLM call (`classify_transaction`) with rules + ledger
   tree + hints + merchant history all in a single prompt
4. **Review queue** — uncertain or unroutable transactions surface in `get_needs_review()`

### LLM Backend — automatic two-tier fallback

| Tier | What happens |
|---|---|
| **Primary** | POST to OpenClaw local gateway (`http://127.0.0.1:18789/v1/chat/completions`, model `openclaw/default`) |
| **Fallback** | Anthropic SDK directly (`claude-3-5-haiku-20241022`) when gateway is unreachable |

Both the gateway port/token and the Anthropic API key are **auto-discovered** from
OpenClaw's own config files — no manual env-var setup needed on a standard install:

- Gateway port + token → `~/.openclaw/openclaw.json` (`gateway.port` / `gateway.auth.token`)
- Anthropic key → `~/.openclaw/agents/main/agent/auth-profiles.json` (`anthropic:default`)

Env vars that override auto-discovery (all optional):
`OPENCLAW_API_URL`, `OPENCLAW_GATEWAY_PORT`, `OPENCLAW_GATEWAY_TOKEN`,
`OPENCLAW_LLM_MODEL`, `ANTHROPIC_API_KEY`

## When to Use This Skill

Invoke for any personal finance request:

- Spending summaries ("how much did I spend on dining this month?")
- Bank connections ("connect my TD account", "reconnect my BMO")
- Transaction queries ("what was that $47 Amazon charge?")
- Classification ("mark that Home Depot charge as rental property maintenance")
- Corrections ("that Uber on Friday was a work trip")
- Exports ("export my finances to Excel")
- Sync ("sync my transactions")
- Ledger management ("add a rental property ledger", "show my property income")
- Rules ("add a rule that Wealthsimple transfers are savings")
- Settings ("set my home currency to CAD", "what timezone am I using?")

## Available MCP Tools

### Profiles
- `list_profiles` — list all local user profiles (usernames)

### Setup
- `setup_status` — check if first-run setup is complete (`not_started | in_progress | complete`)
- `apply_initial_setup(banks_to_link, rental_properties?, investment_account_ids?, extra_ledgers?, hints?)` — initialize ledgers, notifications, and first sync in one call

### Banks
- `start_link(plaid_env?)` — generate Plaid Link URL to connect a bank
- `complete_link(public_token, plaid_env?)` — exchange public token after user completes Plaid Link
- `list_connections` — list connected banks and their status (`active | needs_reauth`)
- `get_connections_needing_attention` — list connections that need user action (reauth or expiring soon)
- `refresh_connection(id)` — re-authenticate a broken connection (Update Mode)
- `disconnect(id)` — remove a bank connection and its data
- `set_account_description(account_id, description)` — set classifier context for an account (e.g. "Primary spending account")

### Ledgers
- `list_ledgers` — show all ledgers (personal/property/investment) and their line items
- `get_ledger(ledger_id, period?)` — get a single ledger with all line items and classified transactions for the period
- `add_ledger(name)` — create a new ledger
- `add_line_item(ledger_id, name, item_type)` — add a line item (`income | expense`) to a ledger
- `remove_line_item(id)` — remove a line item
- `set_account_ledger(account_id, ledger_id)` — link a bank account to a default ledger for automatic routing
- `create_property_ledger(name, description?)` — create a property ledger with default line items (Rent income, Mortgage, Property tax, Maintenance, Insurance, Utilities)
- `create_investment_ledger(name)` — create an investment ledger (Contributions, Dividends/Returns)

### Transactions
- `sync` — pull latest transactions from all connected banks
- `list(filters?)` — query transactions (supports date, ledger, category, account filters)
- `get_needs_review` — transactions that need manual review: uncertain classifications (confidence < 0.7) or unrouted transactions with no line item assigned
- `get_needs_review_summary` — **call this immediately after every `sync`**; returns a pre-formatted batch message (`count`, `summary`, `transactions`) ready to present to the user in one message. Use `summary` as-is for the user-facing message. Includes merchant, amount, date, account, and classifier reasoning for each transaction.
- `route(transaction_id, allocations)` — manually assign a transaction to a ledger/line item
- `add_hint(text)` — add a natural-language classification hint for the LLM
- `list_hints` — list all classification hints
- `remove_hint(id)` — remove a classification hint

### Onboarding (issue #206)
- `list_setup_interview_questions` — return the canonical onboarding interview prompts (employer, subscriptions, utilities, etc.)
- `setup_interview(question_key, answer_text)` — persist a user answer for a given question key (upsert on `(user_id, question_key)`)
- `list_setup_interview` — return all stored interview answers for the active user
- `analyze_recurring_merchants(min_occurrences?, lookback_days?)` — scan recent transactions and return recurring merchants with their inferred category for cross-referencing during onboarding

### Corrections
- `find_transactions(merchant?, date?, amount?, account?, days_window?)` — fuzzy-search transactions by merchant name, ISO date (±`days_window` days), amount (±$0.50), or account name; returns up to 10 matches with their current classification
- `correct_transaction(transaction_id, line_item_id, create_rule?, rule_description?)` — reclassify a transaction; set `create_rule=True` to also create a rule so future matches are classified the same way automatically

### Classification Rules
- `list_rules` — list all classification rules sorted by priority (lower = evaluated first)
- `add_rule(name, description, rule_type, line_item_id?, priority?)` — add a natural-language rule (`transfer | savings | spending | income | skip`)
- `update_rule(id, **fields)` — update a rule's name, description, type, priority, or enabled state
- `reorder_rules(ids)` — set new priority order by passing an ordered list of rule IDs
- `disable_rule(id)` — disable a rule (skipped during classification)
- `enable_rule(id)` — re-enable a disabled rule
- `delete_rule(id)` — delete a user-created rule (default rules cannot be deleted, only disabled)
- `list_auto_promoted_rules` — list auto-promoted routing rules with audit metadata
- `undo_auto_promoted_rule(rule_id)` — revert an auto-promoted rule and its affected entries

### Reports
- `summary(period)` — spending totals by category for a period (e.g. `this_month`, `last_month`)
- `export_excel(years?)` — generate Excel workbook and return download URL

### Settings
- `get_setting(key)` — get an app setting; valid keys: `home_currency`, `timezone`
- `set_setting(key, value)` — update an app setting
  - `home_currency`: one of `CAD`, `USD`, `EUR`, `GBP`
  - `timezone`: any non-empty IANA timezone string (e.g. `America/Toronto`, `UTC`, `Asia/Tokyo`)

### UI & Auth
- `get_ui_url(page?)` — return the local dashboard URL, optionally deep-linked to a page
- `set_ui_password(current_password, new_password)` — change the UI login password
- `reset_ui_password` — generate a password-reset recovery token
- `configure_plaid(client_id, secret, env)` — update Plaid API credentials

## Do / Don't

**Do**
- Always use the MCP tools — never guess from general knowledge
- Call `sync` before answering spending questions if data may be stale
- **After every `sync`, call `get_needs_review_summary` and, if `count > 0`, present the `summary` field to the user in a single message** — do not send one message per transaction
- Use `list_rules` to show what classification rules are active before adding new ones
- Open `start_link` when the user wants to connect or reconnect a bank
- Use `create_property_ledger` for rental properties — it seeds the right line items automatically
- Respect that all data is local and private
- When the user replies with classifications for uncertain transactions:
  1. Call `correct_transaction(transaction_id, line_item_id)` for each corrected item
  2. Check if the merchant is recurring by calling `find_transactions(merchant=<name>)` — if 2+ past transactions exist, propose adding a rule via `add_rule` (tag description with `[from-correction]`)
  3. Apply the rule only after the user confirms

**Don't**
- Don't answer general finance questions ("what is inflation?") — this skill is for personal accounts only
- Don't store tokens or credentials in plain text
- Don't expose DB paths, encryption keys, or internal implementation details
- Don't try to open the Plaid UI yourself — return the URL and let the user click
- Don't call `delete_rule` on default rules — they can only be disabled
