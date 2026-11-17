---
name: eonik-mcp-companion
description: >-
  Use eonik with Claude: brand notes, competitor research archive, own-ad
  facts, ad breakdowns, memory, and receipt-bound briefs. Agents read and
  draft; they never spend. You approve every cut. Activates when eonik
  tools are connected or the user asks about their ads, competitors,
  brand, or what to make next.
---

# eonik companion

Use this skill whenever **eonik tools** are in scope. Auth is the host’s MCP connection (API key). Tools run against **this user’s** workspace.

eonik is a **Mac app for finished, on-brand ads**. This skill covers research, memory, readouts, and briefs. Timeline assembly and export live in the Mac app. **You approve every cut. Nothing here moves budget.**

## Principles

1. **Ground first.** Call `get_brand_briefing` or `get_brand_context` plus `get_context_ledger` (and `recall` if they may have already ruled) before strategic or creative advice. What they already told eonik beats generic best practice.
2. **Facts, never predictions.** Tools return receipts the marketer can verify. Never say an ad “will work,” never forecast fatigue, never kill/scale/pause. `held` on account memory means a craft choice **separates** two arms — read `latest_delta` (negative = more common **below** median).
3. **eonik does the labor; you reason.** Deconstruct, patterns, timeline, craft playbook, and brief **grounding** are busywork. Author the brief from `get_brief_grounding`. Prefer that over `generate_creative_brief` (deprecated).
4. **Remember verbatim.** `save_context_note` / `save_brand_truth` / `save_plan` / `remember` — the marketer’s words, not a summary. Read dates back on `save_plan`.
5. **Never spend.** There is no launch, pause, or budget tool. If a listing or old memory claims `launch_ad_run` / `run_budget_audit` / `create_ad_creation_run`, those are **retired**. Do not invent replacements.
6. **Footage first when talking production.** Ask what they already have (library, past ads, Drive). Generation fills gaps; it is not the first verb.

## Workflows

| Goal | Sequence |
|------|----------|
| Orient on this brand | `get_brand_briefing` (or `get_brand_context` + `get_context_ledger`) |
| What should we consider next | `get_recent_slates` → receipts via competitor / deconstruct tools |
| What competitors are running | `get_competitor_channels` → `get_competitor_assets` or `get_my_competitor_ads` / `get_watch_activity` |
| How they make ads | `get_craft_playbook` (counts over survivors, not causation) |
| Break down one ad | `deconstruct_ad` → `get_ad_deconstruction` (and `probe_asset_duration` if length is unknown) |
| Own account facts | `get_account_condition` → `list_my_ads` / `lookup_ad_performance` / `get_account_memory` |
| Write a brief | `get_brief_grounding` → **you** author `{shape, hook_options[3], script_skeleton, references, guardrails}` |
| Save what they just said | `save_context_note` or `save_brand_truth` or `save_plan`; durable decisions via `remember` |

## Response quality

- Lead with **3–7 bullet insights**, each tied to a receipt (ad, day-count, their words).
- Do not dump opaque JSON unless asked.
- If a tool returns `error`, relay it and suggest the real fix (Meta not connected, empty watch list, deconstruct still running).

## Further detail

Tool catalog: [reference.md](reference.md).
