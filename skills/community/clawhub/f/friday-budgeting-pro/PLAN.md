# Friday Budgeting Pro — Implementation Plan

> See [ARCHITECTURE.md](./ARCHITECTURE.md) for the design.
> This file is the build checklist, nothing more.

---

## Scope Reminder

- Single user (personal finance only)
- Conversational interface only (HAL → MCP tools)
- No CLI, no web UI except the unavoidable Plaid Link page
- OpenClaw handles scheduling (`cron` tool) and notifications
- Keep the codebase under ~10 files

If a feature isn't in ARCHITECTURE.md, **don't build it**.

---

## Build Order

### Phase 1: Foundation
- [ ] `db/schema.sql` — minimal schema (8 tables, see ARCHITECTURE.md)
- [ ] `server/db.py` — SQLite connection + helpers
- [ ] `server/main.py` — FastMCP skeleton, register tools

### Phase 2: Bank Connection
- [ ] `server/plaid_client.py` — Plaid SDK wrapper, token encryption (Fernet)
- [ ] `plaid_link/index.html` — minimal Plaid Link page
- [ ] MCP tools: `start_link`, `complete_link`, `list_connections`,
      `refresh_connection`, `disconnect`

### Phase 3: Transactions
- [ ] Plaid `/transactions/sync` integration with cursor persistence
- [ ] MCP tools: `sync`, `list` (with filters)

### Phase 4: Classification Engine
- [ ] `server/classifier.py` — three-tier engine
  - [ ] Tier 1: rule matching
  - [ ] Tier 2: LLM prompt builder + call
  - [ ] Tier 3: flag for review
  - [ ] Auto-promote (3-correct rule)
- [ ] `server/llm.py` — LLM call wrapper (uses HAL's provider, no separate config)
- [ ] MCP tools: `route`, `get_needs_review`, `add_hint`

### Phase 5: Setup
- [ ] MCP tool: `setup_status`
- [ ] MCP tool: `apply_initial_setup(banks, extra_ledgers?, hints?)`
- [ ] Default "Personal" ledger creation with standard line items
- [ ] After setup, auto-register OpenClaw cron job via `cron` MCP tool

### Phase 6: Reports
- [ ] MCP tools: `summary(period)`, `list_ledgers`
- [ ] `server/excel_export.py` — openpyxl Excel generation
- [ ] MCP tool: `export_excel(years?)`

### Phase 7: Skill Packaging
- [ ] `SKILL.md` — tells HAL when to invoke
- [ ] `package.json` — clawhub publish metadata
- [ ] `README.md` final pass
- [ ] Test: `clawhub install` from local path

### Phase 8: End-to-End Test
- [ ] Fresh install
- [ ] Setup conversation (3 questions)
- [ ] Bank link via Plaid Sandbox
- [ ] Sync + classify
- [ ] Trigger Tier 3 review prompt
- [ ] Export to Excel
- [ ] Verify daily cron job registered

### Phase 9: Publish
- [ ] `clawhub publish`
- [ ] Tag v0.1.0

---

## Out of Scope (Don't Build)

Anything not in ARCHITECTURE.md's "What This Is" section. Specifically:

- Multi-user / accounts
- Multiple ledgers by default (one "Personal" is the default)
- Business / nonprofit templates
- Investment / balance-sheet tracking
- Multi-currency
- Budget targets / forecasts
- Standalone scheduler
- Notification config UI
- Web dashboard
- CLI commands

If a real need emerges later, add a phase. Don't preemptively build.
