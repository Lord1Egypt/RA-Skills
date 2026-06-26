# Contributing — Agent Protocol

This repo is built by an agent swarm. Humans review, agents do most of the work.
This doc is the operating manual for agent contributors.

## The Loop

1. **Pick an issue** labeled `task` that has no assignee.
   - Filter: `is:open is:issue label:task no:assignee`
   - Comment on it: `Claiming this — starting now.`
   - Self-assign.

2. **Branch** off `main`:
   ```
   git checkout -b agent/<issue-num>-<short-slug>
   ```
   Example: `agent/12-fastmcp-skeleton`

3. **Read the dependencies.** Most tickets say "depends on: X". Don't start a
   ticket whose dependencies aren't merged yet.

4. **Implement.** Stay scoped to the ticket. If you find scope creep, open a
   new issue for it instead of expanding the current PR.

5. **Test.** Every ticket has a test requirement in its body. CI runs
   `pytest -q` on every push — green CI is non-negotiable.

6. **Interactive sanity check (mandatory before every commit to UI or MCP code — no exceptions):**

   #### UI tickets — Playwright required
   Run the full Playwright UI test suite locally before every commit that touches `ui/`:
   ```bash
   pip install playwright && playwright install chromium
   pytest tests/ui/ -v
   ```
   All tests must pass. Then manually verify the full page checklist:
   ```
   /login     — login form renders, username + password fields present
   /setup     — wizard loads
   /dashboard — Sync Now + Export Excel present
   /accounts  — accounts grouped by institution, balances shown, Connect a bank button present
   /ledgers   — ledger list renders, + Add ledger button present
   /settings  — page loads, home currency + timezone fields present
   /link      — page loads without error
   ```
   Every page must return 200. Every required button must be present.
   **Do not open a PR if any Playwright test fails or any page is broken.**

   #### MCP tickets — call tools directly
   For every new or changed MCP tool, call it in Python before committing:
   ```python
   import sys; sys.path.insert(0, '.')
   from dotenv import load_dotenv; load_dotenv()
   from server.main import <tool_name>
   result = <tool_name>(<args>)
   assert result.get('status') != 'not_implemented', f'still a stub: {result}'
   print(result)  # must show real data, not a placeholder
   ```
   **Do not open a PR if any tool returns `not_implemented` or throws an unhandled exception.**

   #### Infra / docs / schema tickets
   `pytest -q` is sufficient. No interactive check needed.

   #### PR body
   Include:
   - **Interactive check:** one line describing what you ran and that it passed
   - **Playwright:** `pytest tests/ui/ — N passed` (UI tickets only)

7. **Open a PR.**
   - Title: `[P<phase>] <ticket title>`
   - Body: must include `Closes #<issue-num>` so the issue auto-closes on merge
   - Use the PR template (auto-populated)

8. **Wait for review.** A human (or a reviewer agent) approves and merges.
   Don't self-merge.

## Documentation Requirements (mandatory on every PR)

Every PR that changes behaviour, routes, UI, or architecture **must** update docs in the same commit. Do not open a PR without doing this.

- **ARCHITECTURE.md** — update if you add/remove/change routes, pages, DB schema, design constraints, or out-of-scope items
- **README.md** — update if the user-facing behaviour changes (new page, removed feature, new install step)
- **`ui/server.py` route overview comment** (top of file) — keep the route list current
- **Inline docstrings** — every new route, MCP tool, and DB helper must have a docstring

If nothing in these files needs updating for your ticket, add a note in the PR body: *"No doc changes needed — internal-only change."* The PM will verify.

## Code Rules

- **Python 3.11+**
- **No dependencies beyond what's in `requirements.txt`.** Add new ones in a
  separate commit with justification in the PR body.
- **Keep modules small.** ARCHITECTURE.md says the whole codebase fits in
  ~10 files. Respect that.
- **No features outside ARCHITECTURE.md.** If you think something's missing,
  open an issue. Don't sneak it in.
- **Tests live in `tests/`.** Mirror the source layout
  (`server/db.py` → `tests/test_db.py`).
- **Integration tests live in `tests/integration/`.** These run each MCP tool
  against a real (in-memory / temp) SQLite DB to verify tool wiring, DB
  queries, and response shapes end-to-end.  Run them with
  `python3 -m pytest tests/integration/ -v`.

## MCP Tool Changes Require SKILL.md Updates

Any PR that adds, removes, or renames an `@mcp.tool` in `server/main.py` **must** update `SKILL.md` in the same commit:

- Add new tools to the correct section under `## Available MCP Tools`
- Include: tool name, one-line description, and key parameters
- Remove or correct entries for deleted/renamed tools

The `skill-md-sync` CI job enforces this automatically — PRs that drift will fail CI.

## Anti-Patterns (Don't Do These)

- ❌ Refactoring code outside your ticket
- ❌ Adding multi-user logic ("for future flexibility") — multi-profile is ✅ (see issue #131); concurrent sessions are ❌
- ❌ Building a CLI on top of MCP tools
- ❌ Adding a web UI element beyond the existing Plaid Link page
- ❌ Pulling in ORMs, async frameworks, or "nice to have" libraries
- ❌ Bundling multiple tickets in one PR
- ❌ Committing secrets, real Plaid tokens, or production data

## When in Doubt

- Re-read [ARCHITECTURE.md](./ARCHITECTURE.md) — it's the source of truth.
- Check [PLAN.md](./PLAN.md) for the implementation order.
- Leave a comment on the issue asking for clarification.

## Reviewer Notes

Reviewers (human or agent) should reject PRs that:
- Don't link an issue
- Have no tests for new code
- Touch files outside the ticket scope
- Add scope not covered by the ticket
- Break CI
