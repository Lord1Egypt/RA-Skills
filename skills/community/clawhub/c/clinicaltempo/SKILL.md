---
name: clawhub
description: >-
  Clinical Tempo / HealthTech Protocol — full repo context via public/llm-full.txt (or /llm-full.txt),
  tribal debugging via CLAWHUB.md, Tempo + MPP/x402 patterns, NHS routes, TIP-20 (viem/tempo),
  dance-extras live routes, EVVM on Tempo testnet. Use when: (1) Onboarding an agent or pasting
  system context, (2) Debugging 402/MPP, stale API, or port 8787 issues, (3) Editing docs that feed
  llm-full.txt, (4) Working on hub routes, server/index.js, or integrations (AgentMail, purl, OpenAI
  MPP, etc.), (5) EVVM deploy/docs, (6) Preparing a ClawHub or Copilot instruction bundle, (7)
  MPPScan/OpenAPI discovery at GET /openapi.json, (8) OpenClaw — optional **@anyway-sh/anyway-openclaw**
  plugin, (9) Publishing or consuming a ClawHub skill zip modeled on self-improving-agent rigor.
  For raw EVVM protocol depth, fetch https://www.evvm.info/llms-full.txt (not vendored in-repo).
metadata: {}
---

# Clinical Tempo · ClawHub context skill

**Clinical Tempo** is the reference **HealthTech Protocol** superapp: React hub + dedicated routes, Node/Express API, **Tempo** settlement, **MPP / x402** machine payments. This skill tells agents **where context lives** and **how to avoid known traps** (see `CLAWHUB.md`).

---

## Quick reference

| Situation | Action |
| --- | --- |
| Need **one file** with README + use cases + protocol + ClawHub | Load **`public/llm-full.txt`** or **`/llm-full.txt`** (running app). |
| **`402` / MPP / wallet** confusion | **`CLAWHUB.md`** + relevant route in **`server/index.js`**. |
| **UI works but API 404 / HTML** | Backend not running or **stale** process — restart **`npm run server`** (**`8787`**). |
| Verify live MPP handler exists | **`GET http://localhost:8787/api/dance-extras/live`** → JSON with `flowKeys`. |
| **Which screens exist** | **`src/hubRoutes.ts`**; hub **`/`**. |
| **Changed markdown** included in bundle | **`npm run build:llm`** (runs before **`npm run build`**). |
| **EVVM** (deploy, CLI, Tempo testnet) | **`docs/EVVM_TEMPO.md`**, **`/evvm`**; deep: **`https://www.evvm.info/llms-full.txt`**. |
| **MPPScan / OpenAPI** | **`GET /openapi.json`**; **`npm run discovery`** · **`docs/MPPSCAN_DISCOVERY.md`** |
| **OpenClaw + extra capabilities** | Optional plugin: **`openclaw plugins install @anyway-sh/anyway-openclaw`** — then restart gateway if needed; see **`references/openclaw-clinical-tempo.md`** |
| **Promotion** of a fix for future agents | Short entry under **Successes** or **Failures** in **`CLAWHUB.md`** (no secrets). |
| **TIP-20 mint** (`/nhs/tip20`) — issuer role + envelope `0x76` | **`CLAWHUB.md`** Success §10 / Failure §10; code **`src/tempoTip20Launch.ts`**. Mint needs **`ISSUER_ROLE`**; use **`writeContractSync(grantRole)`**, not **`grantRolesSync`** (batched tx type **0x76** breaks viem + browser wallets). |

---

## When to activate (triggers)

Use this skill automatically when:

1. The user @-mentions **`llm-full.txt`**, **`CLAWHUB`**, **Clinical Tempo**, **MPP**, **dance-extras**, or **Tempo testnet/mainnet**.
2. The task touches **`server/index.js`**, **`server/payments.js`**, or **`src/danceExtras*.ts`**.
3. Docs are edited that appear in **`scripts/build-llm-full.mjs`** (bundle sources).
4. The user uploads **ClawHub** / **OpenClaw** / **Copilot** context questions.

---

## Recommended: Cursor / IDE

1. **`@`** `public/llm-full.txt` for broad changes; **`@`** `CLAWHUB.md` when debugging past incidents.
2. Project rules: repo root **`AGENTS.md`** or **`.cursor/rules`** if present — align with **`README.md`**.

See **`references/openclaw-clinical-tempo.md`** for OpenClaw workspace file hints.

---

## Installation

**From this repository (authoritative):**

```bash
# Skill lives at:
.cursor/skills/clawhub/
```

**Manual copy to OpenClaw skills dir (optional):**

```bash
cp -r .cursor/skills/clawhub ~/.openclaw/skills/clinicaltempo-clawhub
```

**ClawHub (publish):** Zip **`clawhub/`** (this folder) so the listing includes **`SKILL.md`**, **`references/`**, **`assets/`**, **`hooks/`**, **`scripts/`**. See **`README.md`** in this folder for a file manifest.

### OpenClaw: optional **Anyway** plugin

This skill is **context-only**; **`@anyway-sh/anyway-openclaw`** extends the **OpenClaw** runtime with additional capabilities (separate from Clinical Tempo). Install when you want both:

```bash
openclaw plugins install @anyway-sh/anyway-openclaw
# If your setup requires it:
openclaw gateway restart
```

Pair with: **this skill** (or [ClawHub listing](https://clawhub.ai/arunnadarasa/clinicaltempo)) + optional **`clinicaltempo-clawhub`** hook. Details: **`references/openclaw-clinical-tempo.md`**.

---

## Repository map (where to look)

```
clinicaltempo/
├── public/llm-full.txt          # Generated — do not hand-edit; run npm run build:llm
├── CLAWHUB.md                   # Tribal knowledge: successes, failures, checklists
├── README.md                    # Routes, stack, quick start
├── HEALTHTECH_USE_CASES.md       # Flow-by-flow API contract
├── server/index.js              # Express routes, integrations, MPP proxies
├── server/openapi.mjs           # OpenAPI 3.1 for GET /openapi.json (MPPScan)
├── server/payments.js           # Chain IDs, charge helpers
├── src/hubRoutes.ts             # Hub directory of all /routes
├── src/danceExtrasLiveMpp.ts    # Browser MPP helpers (live flows)
├── src/danceExtrasJudgeWire.ts  # Judge-score wire snippets
├── .github/copilot-instructions.md
└── scripts/build-llm-full.mjs   # Source list for llm-full.txt
```

---

## First load (full orientation)

1. Prefer **`public/llm-full.txt`** (or **`/llm-full.txt`** from a running build) — includes **`CLAWHUB.md`** in the bundle.
2. Regenerate after doc edits: **`npm run build:llm`**.

### Bundle sources

Exact list: **`assets/LLM-BUNDLE-SOURCES.md`** (mirrors `build-llm-full.mjs`).

### EVVM: `llm-full.txt` vs `llms-full.txt`

| Artifact | Role |
| --- | --- |
| **`public/llm-full.txt`** (singular) | Clinical Tempo-generated; committed; **use first**. |
| **`https://www.evvm.info/llms-full.txt`** (plural) | Upstream EVVM protocol dump — **attach for EVVM-only depth**; do not duplicate into `public/` unless you intend to maintain a fork. |

---

## Debugging (tribal knowledge)

Read **`CLAWHUB.md`** for:

- What succeeded / failed (purl, AgentMail, **`402`** loops, **stale Express on 8787**, etc.)
- Repeatable checks (e.g. **`GET /api/dance-extras/live`**)

Deeper: **`references/troubleshooting.md`**.

---

## Key implementation pointers

| Topic | Location |
| --- | --- |
| Live MPP dance flows | **`POST /api/dance-extras/live/:flowKey/:network`** — **`GET /api/dance-extras/live`** |
| Hub routes | **`src/hubRoutes.ts`** |
| Browser MPP | **`src/danceExtrasLiveMpp.ts`**, **`src/danceExtrasJudgeWire.ts`** |
| Server | **`server/index.js`** |

Concrete snippets: **`references/examples.md`**.

---

## Copilot Chat integration

GitHub Copilot does not load this folder automatically. Options:

1. Commit **`/.github/copilot-instructions.md`** (already in Clinical Tempo repo).
2. Paste from **`references/copilot-and-agents.md`** into chat or org instructions.

**Quick prompts:**

- “Use **`llm-full.txt`** as context for this PR.”
- “Scan **`CLAWHUB.md`** for 8787 / MPP / purl before changing the server.”
- “After this task, suggest one **CLAWHUB** Success or Failure line (no secrets).”
- “Regenerate **`public/llm-full.txt`** — which files are inputs?” → **`assets/LLM-BUNDLE-SOURCES.md`**

---

## Promotion: CLAWHUB vs llm-full

| Content | Where |
| --- | --- |
| **Stable facts** (routes, env *names*, ports) | **`README.md`**, **`HEALTHTECH_USE_CASES.md`**, or relevant **`docs/*.md`** — then **`npm run build:llm`**. |
| **Incident / debugging narrative** | **`CLAWHUB.md`** Successes / Failures. |
| **EVVM upstream protocol** | Link **`https://www.evvm.info/llms-full.txt`**; keep **`docs/EVVM_TEMPO.md`** for Tempo-specific steps. |

---

## Verification script

From repo root (optional):

```bash
./.cursor/skills/clawhub/scripts/verify-clinical-tempo-context.sh
```

Checks that **`public/llm-full.txt`** exists and reminds you of the live MPP **`GET`** check.

---

## OpenClaw hook (optional)

Parity with [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent): injects a **virtual** `CLINICAL_TEMPO_CONTEXT_REMINDER.md` on **`agent:bootstrap`** (skips sub-agents). No network I/O.

```bash
# From this skill folder (or repo: .cursor/skills/clawhub/)
cp -r hooks/openclaw ~/.openclaw/hooks/clinicaltempo-clawhub

openclaw hooks enable clinicaltempo-clawhub
```

- **`hooks/openclaw/HOOK.md`** — metadata + enable/disable.
- **`hooks/openclaw/handler.js`** — CommonJS handler (primary).
- **`hooks/openclaw/handler.ts`** — TypeScript handler for OpenClaw (types from **`openclaw/hooks`** at runtime).

Full notes: **`references/openclaw-clinical-tempo.md`**.

---

## Best practices

1. **Never** paste real **`.env`** secrets into prompts — use **`.env.example`** names only.
2. After editing any file listed in **`build-llm-full.mjs`**, run **`npm run build:llm`** before claiming “docs are updated in the bundle.”
3. Prefer **`GET /api/dance-extras/live`** over guessing whether the server is new.
4. For EVVM, answer **no** to optional Sepolia registry registration until policy allows (see **`docs/EVVM_TEMPO.md`**).

---

## Operations manual (same rigor as [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent))

This skill mirrors that package’s **shape**: quick reference, OpenClaw integration, optional hooks/scripts, templates, and promotion — but maps “project memory” to **`CLAWHUB.md`** + **`README.md`** instead of only **`.learnings/`**.

### Promotion targets (where tribal knowledge goes)

| Finding | Promote to |
| --- | --- |
| Incident / workaround / “what broke” | **`CLAWHUB.md`** Successes or Failures |
| Stable routes, ports, env **names**, stack facts | **`README.md`**, **`HEALTHTECH_USE_CASES.md`**, or **`docs/*.md`**, then **`npm run build:llm`** |
| IDE default context | **`.github/copilot-instructions.md`** |
| OpenClaw workspace behavior | Workspace **`AGENTS.md` / `TOOLS.md`** (see **`references/openclaw-integration.md`**) |

Entry templates: **`assets/templates/CLAWHUB-ENTRY.md`**.

### Optional: `.learnings/` format (LRN / ERR / FEAT)

If you maintain a **parallel** log (e.g. in OpenClaw workspace), use the same ID patterns as self-improving-agent (**`LRN-YYYYMMDD-XXX`**, etc.). Starters ship under **`assets/learnings/`**. **Authoritative for this repo** remains **`CLAWHUB.md`**.

### Periodic review (before a large change)

```bash
# Grep CLAWHUB for an area
rg -n "MPP|402|8787|TIP-20|purl" CLAWHUB.md

# Confirm bundle is fresh after doc edits
npm run build:llm

# Smoke API (server must run on 8787)
curl -sS http://127.0.0.1:8787/api/dance-extras/live | head -c 400
```

### Detection triggers (load this skill when)

- User mentions **`llm-full.txt`**, **`CLAWHUB`**, **Clinical Tempo**, **HealthTech**, **Tempo**, **MPP**, **`402`**, **NHS**, **TIP-20**, **8787**, **ClawHub**, or **OpenClaw**.
- Editing **`server/index.js`**, **`scripts/build-llm-full.mjs`**, or **`src/hubRoutes.ts`**.
- Preparing a **zip** for [clawhub.ai](https://clawhub.ai/) or debugging a **published** install.

### Claude Code / Codex hooks (optional)

| Script | Role |
| --- | --- |
| **`scripts/activator.sh`** | Small XML-tagged reminder after each prompt (`UserPromptSubmit`) |
| **`scripts/error-detector.sh`** | Optional hint after Bash failures (`PostToolUse`) |

Configure **`.claude/settings.json`** or **`.codex/settings.json`** — full paths in **`references/hooks-setup.md`**.

### Multi-agent matrix

| Agent | How this skill applies |
| --- | --- |
| **Cursor** | `@` **`public/llm-full.txt`** + **`CLAWHUB.md`**; rules in **`.cursor/rules`** if present |
| **GitHub Copilot** | **`.github/copilot-instructions.md`** + **`references/copilot-and-agents.md`** |
| **OpenClaw** | Copy skill + optional **`hooks/openclaw`**; see **`references/openclaw-integration.md`** |
| **Claude Code** | Optional **`activator.sh`** hook |

### Skill extraction (new package from a fix)

When a CLAWHUB entry is **reusable across repos**, consider a standalone skill:

```bash
./.cursor/skills/clawhub/scripts/extract-skill.sh my-org-skill --dry-run
./.cursor/skills/clawhub/scripts/extract-skill.sh my-org-skill
```

Then replace the scaffold under **`.cursor/skills/my-org-skill/`** using **`assets/SKILL-TEMPLATE.md`**.

---

## Files in this package

| Path | Purpose |
| --- | --- |
| `SKILL.md` | This file — primary skill entry |
| `README.md` | Package manifest + upload notes for ClawHub |
| `_meta.sample.json` | Rename to `_meta.json` after ClawHub assigns IDs (optional) |
| `references/copilot-and-agents.md` | Paste blocks for Copilot / chat |
| `references/openclaw-clinical-tempo.md` | OpenClaw workspace + Anyway plugin |
| `references/openclaw-integration.md` | Full OpenClaw + ClawHub install guide |
| `references/hooks-setup.md` | Claude Code / Codex hook paths for `activator.sh` |
| `references/examples.md` | Concrete @-mentions, curls, patterns |
| `references/troubleshooting.md` | Common failures & fixes |
| `assets/LLM-BUNDLE-SOURCES.md` | What feeds `llm-full.txt` |
| `assets/SKILL-TEMPLATE.md` | Templates for new skills / forks |
| `assets/templates/CLAWHUB-ENTRY.md` | Success / Failure append shapes |
| `assets/learnings/*.md` | Optional LRN-style stubs (repo uses **`CLAWHUB.md`**) |
| `scripts/verify-clinical-tempo-context.sh` | Quick repo checks |
| `scripts/activator.sh` | Optional UserPromptSubmit reminder |
| `scripts/error-detector.sh` | Optional PostToolUse (Bash) hint |
| `scripts/extract-skill.sh` | Scaffold **`.cursor/skills/<slug>/`** |
| `hooks/openclaw/HOOK.md` | OpenClaw hook manifest |
| `hooks/openclaw/handler.js` | Bootstrap injector (CommonJS) |
| `hooks/openclaw/handler.ts` | Bootstrap injector (TypeScript) |
| `hooks/README.md` | Hook folder index |

---

## See also

- **Published skill:** [clawhub.ai/arunnadarasa/clinicaltempo](https://clawhub.ai/arunnadarasa/clinicaltempo) — browse **[ClawHub](https://clawhub.ai/)** for versioned skills
- **Ecosystem synergy (mpp-nanogpt-modal, nanochat, OpenClaw):** **`docs/ECOSYSTEM_SYNERGY.md`**
- Structural inspiration: [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) (references, assets, scripts, hooks, `.learnings` patterns)
- Clinical Tempo repo: **`README.md`**, **`CLAWHUB.md`**
