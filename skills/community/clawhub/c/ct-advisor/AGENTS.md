# AGENTS.md — ct-advisor v1.3.26 (ct- series A-tier entry point)

> This document is ct-advisor's self-improvement contract. It follows ct-base AGENTS.md structure and is written in English per §4 (references·AGENTS are English-only for published ct- skills).

## Skill Overview

`ct-advisor`: the single front door for the entire `ct-*` clinical-trial skill family — a methodology & regulatory-evidence advisor (A-tier) that routes real-data / competitive-intel asks to sibling data skills (ct-registry / ct-safety / ct-literature / ct-samplesize / meta-analysis). **All domain expertise lives on the Coze cloud side. The local side retains ZERO knowledge base and performs ZERO local network retrieval.**

## 🔴 Core Architecture (v1.3.26, current)

**The local LLM is a PIPE, not an author.** Its ONE AND ONLY action is:

```bash
python scripts/entry.py --q "<user question>" [--attach "<path>"]
```

**Everything else — attachment gate, vague gate, clarify loop, Coze forwarding, skill delegation — is done by code inside entry.py. The local LLM has NO decision space.**

### Module layer map (the whole skill, 4 layers, one entry)

```
┌─ L0 ENTRY (agent's only callable) ──────────────────────────────┐
│  scripts/entry.py                                               │
│    ① attachment gate  → doc_memory.py / office_to_md.py        │
│    ② vague gate       → route.py (is_vague, regex-only)        │
│    ③ clarify loop     → clarify_loop.py (vague only)           │
│    ④ forward          → orchestrate.py                         │
│    ⑤ delegate stitch  → refine_answer.py --card-inline         │
│    ⑥ wrap + sha256    → stdout                                 │
├─ L1 ORCHESTRATION ──────────────────────────────────────────────┤
│  orchestrate.py   parallel Coze-fire + prefetch, merge, wrap   │
│  refine_answer.py card-inline executor (ct-skill results)      │
│  route_tool.py    deterministic tool prediction (predict)      │
│  handle_need_tool.py  run sibling ct-skill (install_sibling)    │
│  forward_guards.py  dedup_guard + scope_guard + doc_memory     │
├─ L2 ADAPTERS (network & contracts) ─────────────────────────────┤
│  adapters/refiner.py       CozeRefiner (sole backend)          │
│  adapters/sanitize.py      outbound PII scrub (ct-base §11)    │
│  adapters/coze_token_embedded.py  obfuscated public token      │
│  adapters/http_probe.py / install_sibling.py /                 │
│  probe_publication.py / bug_report.py                          │
├─ L3 SUPPORT ────────────────────────────────────────────────────┤
│  doc_memory.py    upload channel + doc_context envelope        │
│  office_to_md.py  stdlib OOXML→md ( >5MB path )                │
│  context_stitch.py conversation-history stitching              │
│  hardware_id.py   query_origin stamp    i18n.py  locale        │
│  check_coze.py    one-shot network/token diagnostic            │
│  tests: test_* (six suites, all green post-cleanup)            │
└─────────────────────────────────────────────────────────────────┘
```

**2026-11-09 · client handoff (default path)**: `handle_need_tool.execute_card` now
checks `_client_callable(tool)` **before** the tier gates. A locally registered sibling
returns `status=handoff` — an `@skill:<slug>` card with extracted params, missing
params, the skill's real deliverables and a Tier-B confidentiality note — which
`refine_answer._merge_answer` renders **in code** and `entry.py` emits through the
single exit. The agent's only callable is still `entry.py`; HARD GATE is unchanged.
`CT_ADVISOR_HANDOFF=0` restores the legacy CLI execution card (§20.19.7 red line 2).
`CT_ADVISOR_CLOUD_BRIEF` is now **default off**: once the client could invoke the full
skills, the non-audit brief shortcut was downgraded to opt-in.
`published` (SkillHub listing) is a distribution fact only — orthogonal to local
availability and to `tier` (the confidentiality boundary).

**2026-11-09 · return path (`entry.py --stitch`)**: `scripts/stitch_results.py` is a
local-only, stdlib-only backfill for mixed handoffs. It parses sibling output files
(md / txt / log / json / csv / tsv / xlsx) and stitches a deterministic summary
through the same `entry._emit_plain` exit — no second entry point, no Coze, no HTTP,
no LLM. Outputs may be Tier-B confidential, so F33 keeps everything on this machine
(extension allowlist, size / count / excerpt caps, credential-name denylist).
`--q` is optional in stitch mode only. Chinese mixed asks now resolve `cond` / `topic`
inside `route_tool.extract_params_for_tools`; the single-skill lexicon (37/37) is
untouched, and ct-safety never receives a Chinese `drug` (openFDA needs English).

**Removed in v1.2.0 (dead code, coze-only leftovers)**: `adapters/backend.py` / `data_context.py` / `qa_store.py` (legacy LocalBackend + QA-log seams, never on the entry chain), `_patch14*.py`, `drug_name_resolver.py`, `keyword_breadth.py`, `landscape_scorer.py`, `source_guard.py`, `r_libs.py`, `workflows.json`, `menu.json`, `test_modeB.py`, and all `*.park-20260924*` / `_TRASH-*` / `out/` snapshot dirs (~185 MB).

---

## Core Rules

### 1. Environment Detection
- Python via Anaconda (`C:\Tools\anaconda3\python.exe`).
- R via `C:\Tools\R-4.6.1\bin\x64\Rscript.exe` (used by sibling skills, not this one).

### 2. Code Execution
- **No code execution by the agent.** The agent calls `entry.py` which internally orchestrates everything.
- The agent MUST NOT call `route.py`, `refine_answer.py`, `orchestrate.py`, `clarify_loop.py`, or any other pipeline script directly.

### 3. Language Detection
- Follows OS locale; bilingual auto-switch via code (no agent action needed).

### 4. Security Red Line
- **No local knowledge base** — the `knowledge/` directory has been removed entirely.
  🔴 **Knowledge base ownership (user ruling 2026-11-09)**: all domain knowledge is
  maintained **only on the Coze endpoint** (`adapters/coze/knowledge/`) and shipped
  with the Coze package; never mirror it back into `config/`, `docs/` or the skill
  runtime. Three L1 methodology topics (`ref-topic-samplesize-methods` /
  `ref-topic-signal-methods` / `ref-topic-registry-semantics`), the L1 answer
  contract, `_CATEGORY_KNOWLEDGE` and `knowledge_index.json` are Coze-side assets.
  Local passes only `query_meta.domain_hint`; **never** put a domain in
  `scope_hint` (the cloud renders any non-empty value as "possibly out of scope").
- **No local network retrieval** — `search_refs.py`, `update_reference_index.py`, and `search-sites.md` have been removed.
- **No web search fallback** — if Coze fails, the user is told to retry; the LLM does not fabricate answers from its own knowledge.
- **Outbound authorization** — `ct-advisor.coze.site/run` is pre-whitelisted; the agent MUST NOT edit `config.json`.
- **Proxy resilience** — Coze calls and file uploads retry direct-bypass when system proxy env vars point at dead/half-dead local proxies (see refiner `_call_coze` and doc_memory upload paths).

### 5. Self-Improving
- Record LRN / ERR / FEAT entries per the self-improving-agent skill format.
- Promote recurring patterns to long-term memory automatically.
- Workflow/tool changes → workspace `AGENTS.md`; behavior → `~/.workbuddy/SOUL.md`.

---

## Self-Improving Trigger Conditions
- Record LRN / ERR / FEAT entries per the self-improving-agent skill format.
- Promote recurring patterns (Recurrence-Count ≥ 3, across ≥ 2 tasks) to long-term memory automatically.
- Behavior/communication/UX → `~/.workbuddy/SOUL.md`; workflow/tool/infrastructure → workspace `AGENTS.md`; cross-project user prefs → `~/.workbuddy/MEMORY.md`; project-level → `.workbuddy/memory/MEMORY.md`.

---

## Dependencies

### Sibling data/compute skills (routed via Coze, not embedded)
- `ct-registry` — trial-registry landscape
- `ct-safety` — FAERS safety signals
- `ct-literature` — published literature
- `ct-samplesize` — sample-size & power handoff
- `meta-analysis` — referral-only (forest / funnel / rob2 plots)

### Internal base
- `ct-base` (library, not invocable) — shared helpers and canonical BASE.md spec.

## Attachment handling (v1.2.0 · single 5 MB gate, FIRST step of entry.py)

| Size | Path | Mechanism |
|---|---|---|
| `< 5 MB` | **Upload original file, never convert locally** | `doc_memory.build_file_payload(allow_upload=True)` → Coze `/upload_file` → top-level `doc_context` (`mode=file_id`); auto-degrade to base64 forward (`mode=file`) on failure. Coze decodes ANY Office format natively (OOXML and OLE2 alike). |
| `> 5 MB` | Convert locally, then **upload the resulting `.md` as the attachment** — same `doc_context` channel — plus an ℹ️ notice | `office_to_md.py` (OOXML, stdlib) or direct read (`.txt/.md/.csv/.tsv/.json`); unsupported → explicit user prompt |

## Deliverable boundary (v1.24 · 2026-09-23)

The deliverable of this skill is **text only**. When the user asks for the revised document back, say on the **first line** that this feature is **not available** — only written suggestions — and then provide the suggestions as copy-ready text.

---

## 🔴 Workbench Frontend Testing (Standard Process — MANDATORY GATE)

The workbench frontend (`workbench/index.html` + `ct-advisor-proxy.py` + `wb-list.*` + `tokens.css`) is covered by a full automated regression suite in `workbench/tests/`. **This is a mandatory gate, not optional.**

**Trigger** — any content change to the files above (CSS tokenization, i18n dict edit, event binding, fetch contract, proxy logic).

**Standard loop** (full SOP in `references/WORKBENCH_TESTING.md`):
1. Baseline: run the suite, confirm green before changing anything.
2. Change: minimal root-cause fix, no unrelated refactor bundled in.
3. Run: `C:/Tools/anaconda3/python.exe workbench/tests/run_all.py` → exit `0` = green.
4. Gate: **any P0/P1 failure = red light, publish blocked.** P2/P3 may be deferred but must be logged.
5. Fix–regress: locate `file:line` from `report.json`, fix, re-run until green; no "marked fixed without a green re-run".
6. Verify: for P0/P1 fixes run `workbench/tests/verify_fixes.py` (before/after diff via `index.html.bak-*`).
7. Publish gate: only after full green + verify pass may `run_app.bat` / `publish-kit` proceed.

**Custody red lines** — never delete `workbench/index.html.bak-*` (verify_fixes needs it) or `workbench/tests/__requests.jsonl` mid-run.

**Why this exists** — one pass caught 6 real defects: `esc()` not escaping `>` (injection surface), `loadLang()` `a || b ? c : d` precedence silently reverting language on refresh, missing value whitelist crashing init on dirty lang, `seedSamples()` not marking dirty (example history lost on refresh), markdown blockquote regex coupled to the un-escaped `>` (latent regression when esc was fixed), and `sendConsole()` missing `const T=t()` (long-input hint silently dead). Behavior tests (L2) are the real gate; the static `a || b ? c : d` heuristic is only a warn signal.
