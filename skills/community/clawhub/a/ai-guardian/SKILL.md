---
name: ai-guardian
slug: ai-guardian
displayName: "Local LLM Guard for Ollama / llama.cpp"
summary: "Governed local-LLM observability: model policy, prompt scanner, capture proxy, 21 tools."
license: MIT
homepage: https://github.com/AIops-tools/AI-Guardian
tags: [aiops, mcp, governance, ai-guardian]
description: >
  Use this skill whenever the user needs to observe or govern on-endpoint local LLMs running on Ollama, llama.cpp (llama-server), LM Studio, or a local single-node vLLM — inventory installed/running models with an allow/deny verdict (shadow-AI detection), inspect VRAM residency, model license/params/capabilities and server version, view the model policy, detect model provenance/digest drift (re-pulled or tampered weights; strong for Ollama/llama.cpp, id-only and honestly weaker for LM Studio/vLLM), scan a prompt for secrets / PII / source-code / jailbreak with a weighted risk band, route a prompt THROUGH a guard that scans + policy-gates + records + runs-if-allowed (guarded_generate / observe_chat), query the observed-usage log, and roll up anomalies (shadow models, digest drift, high-risk + blocked prompts).
  Always use this skill for "what local models are installed", "find shadow / unsanctioned AI models", "which model is loaded in VRAM", "scan this prompt for secrets/PII before sending", "stop secrets leaking into a local model", "block a prompt with an API key", "detect a jailbreak / prompt injection", "set a model allowlist / denylist", "detect a tampered / re-pulled model", "audit local LLM usage", "guard my llama.cpp / LM Studio / local vLLM endpoint", or "the complement to IGEL AI Armor".
  Do NOT use for GPU inference CLUSTERS (multi-node / fleet-scale vLLM / Ray serving) — this is for single-endpoint LOCAL LLMs; point cluster/serving work to inference-aiops. Also not for hypervisors, storage, backup, Kubernetes, or network devices.
  Passive inventory/state auditing plus opt-in route-through content governance, with a bundled governance harness (audit, policy, token budget, undo, risk-tiers). A transparent capture proxy is v0.2 roadmap.
installer:
  kind: uv
  package: ai-guardian
argument-hint: "[model name, a prompt to scan, or describe your local-LLM task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["ai-guardian","uvx"]},"optional":{"env":["AI_GUARDIAN_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/AI-Guardian","emoji":"🛡️","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed local-LLM (Ollama) observability + content governance. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  Every tool call is audited to a local SQLite DB at ~/.ai-guardian/audit.db (relocatable via AI_GUARDIAN_AIOPS_HOME); the OBSERVED local-LLM usage log is a SEPARATE DB at ~/.ai-guardian/usage.db.
  Zero-config: ai-guardian defaults to the local Ollama at http://localhost:11434 with no token. Ollama endpoints usually run open on a trusted host, so a bearer token is OPTIONAL; when one is supplied it is stored ENCRYPTED in ~/.ai-guardian/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. The store is unlocked by a master password from AI_GUARDIAN_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var AI_GUARDIAN_<TARGET_NAME_UPPER>_TOKEN is still honoured as a fallback with a deprecation warning (migrate with 'ai-guardian secret migrate').
  The prompt scanner is deterministic and offline (no I/O, no network); route-through guards (guarded_generate/observe_chat) call Ollama only if the prompt's risk band is below block_threshold AND the model is allowed. The raw prompt is never stored — only its length + redacted findings.
  State-changing operations: remove_model (high, dry-run + double confirm at the CLI, undo re-pull); pull/unload/allowlist/denylist/pin/guarded writes are medium. All write tools pass through the @governed_tool decorator (pre-check + budget guard + audit + risk-tier label).
  Webhooks: none — no outbound network calls beyond the configured Ollama REST API.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Validation status: the scanner/policy/risk-band are deterministic offline logic; the core Ollama route-through (real generation + policy deny + undo capture) was exercised against a live Ollama 0.24.0 on 2026-07-13, while the remaining runtime API paths and the OpenAI-compatible dialects are exercised against mocked responses (see docs/VERIFICATION.md). Content governance is opt-in route-through in v0.1, a transparent capture proxy is v0.2 roadmap, and IGEL AI Armor interop is doc-level positioning.
---

# AI Guardian

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by Ollama, IGEL, or any AI-security vendor.** Product and trademark names belong to their owners. Source at [github.com/AIops-tools/AI-Guardian](https://github.com/AIops-tools/AI-Guardian) under the MIT license.

Governed observability + governance for **on-endpoint local LLMs (Ollama)** —
**21 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a
local unified audit log under `~/.ai-guardian/`, token/runaway budget guard,
undo-token recording, and descriptive risk tiers. It is the
**complement to IGEL AI Armor**: AI Armor governs *whether* a local model may run;
ai-guardian records *what it did* and gates *what leaves in the prompt*.

Ollama keeps **no queryable prompt history** (context is client-supplied each
request), so ai-guardian observes on two fronts: **passive inventory / state
auditing** over `/api/tags`, `/api/ps`, `/api/show`, `/api/version`; and **opt-in
route-through content governance** — a caller sends a prompt *through*
`guarded_generate` / `observe_chat`, which scans + policy-gates + records it and
only then calls Ollama.

> **Standalone**: the governance harness is bundled in the package
> (`ai_guardian.governance`) — no external skill-family dependency. A
> transparent capture proxy for other clients' traffic is v0.2 roadmap, and
> IGEL AI Armor interop is doc-level positioning.

## What This Skill Does

| Group | Tools | Count | Read/Write |
|-------|-------|:-----:|:----------:|
| **Inventory / state** | `list_models`, `running_models`, `model_details`, `server_status`, `vram_usage` | 5 | read |
| **Policy / provenance** | `policy_view`, `model_provenance` | 2 | read |
| **Content governance (read)** | `scan_prompt`, `usage_events`, `anomaly_report` | 3 | read |
| **Model lifecycle** | `pull_model` (medium), `remove_model` (high), `unload_model` (medium) | 3 | write |
| **Policy writes** | `set_model_allowlist`, `set_model_denylist`, `pin_model_digest` (all medium) | 3 | write |
| **Route-through guard** | `guarded_generate`, `observe_chat` (medium) | 2 | write |
| **Undo** | `undo_list`, `undo_apply` | 2 | undo |

`scan_prompt` is pure (no Ollama call). `guarded_generate` / `observe_chat` block
when the prompt's risk band `>= block_threshold` (default `high`) **or** the model
is disallowed; blocked calls never reach Ollama and are recorded as blocked.

## Quick Install

```bash
uv tool install ai-guardian-aiops
ai-guardian doctor          # works zero-config against a local Ollama
ai-guardian init            # optional: endpoint(s) + optional token + model allowlist
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/ai-guardian
openclaw skills info ai-guardian          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Inventory local models and **spot shadow AI** (`list_models` / `anomaly_report`): unsanctioned models show `allowed:false`
- **Scan a prompt before sending it** (`scan_prompt`): secrets / PII / source-code / jailbreak → a weighted risk band, no model call
- **Stop secrets or PII leaking into a local model** (`guarded_generate` / `observe_chat`): scan + policy-gate + record, then run only if allowed
- **Detect a tampered / re-pulled model** (`model_provenance`): current digest vs its pin → drift
- Enforce which models may run (`set_model_allowlist` / `set_model_denylist`) and pin trusted digests (`pin_model_digest`)
- Inspect VRAM residency (`running_models` / `vram_usage`) and audit observed usage (`usage_events`)

**Do NOT use when** the target is a GPU inference **cluster** (multi-node serving) — that is a different tool in the AIops-tools line. Also not for hypervisors, storage appliances, backup products, container clusters, or network devices.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| On-endpoint local LLM (Ollama): scan prompts, shadow-AI, provenance, policy | **ai-guardian** (this skill) |
| GPU inference **cluster** serving/ops | another AIops-tools skill for cluster serving |
| Hypervisor / storage / backup / container / network ops | the matching AIops-tools skill |

## Common Workflows

### 1. Find and shut down shadow (unsanctioned) local models

1. `ai-guardian doctor` → confirm the Ollama endpoint is reachable before you
   conclude a fleet has "no models" when it really has no connectivity
2. `ai-guardian overview` → endpoint status, model count, and what is loaded
   right now
3. `ai-guardian model list` (MCP: `list_models`) → every installed model with its
   allow/deny verdict; anything `allowed:false` is shadow AI
4. `ai-guardian guard anomalies` (MCP: `anomaly_report`) → a one-shot rollup of
   shadow models + digest drift + high-risk / blocked prompts, so you can tell a
   single stray pull from a pattern
5. `ai-guardian model running` / `vram_usage` → is the shadow model merely
   installed, or actually loaded and consuming VRAM right now?
6. Tighten policy so it cannot recur: `set_model_allowlist(["llama3.*", "qwen*"])`
   → future unsanctioned models are refused at `pull_model`. Reversible: the
   prior list is captured as the undo descriptor
7. Remove the offender: `ai-guardian model remove <model> --dry-run`, then re-run
   without `--dry-run` → **high** risk, double confirmation, needs
   `AI_GUARDIAN_AUDIT_APPROVED_BY`; the undo descriptor records a re-pull
8. **Failure branch**: if the new allowlist turns out to be too tight and blocks
   a sanctioned model, `ai-guardian undo list` → `undo apply <id>` restores the
   **prior** list exactly. If a removal was wrong, replaying the undo re-pulls
   the model — but the weights come from the registry, so confirm the digest
   afterwards with workflow 3 rather than assuming it is bit-identical.

### 2. Stop secrets and PII leaking into a local model

1. `ai-guardian guard scan "…text…"` (MCP: `scan_prompt`) → a **pure** call, no
   model involved: deterministic findings (secrets / PII / code / jailbreak) plus
   a weighted risk band. Use it to pre-check content offline before it ever
   reaches a model
2. `ai-guardian guard policy` (MCP: `policy_view`) → confirm which models are
   permitted and what the current thresholds are
3. Route real calls through the guard:
   `guarded_generate(model, prompt, block_threshold="high")` → the guard scans,
   records to the usage log, and **blocks before Ollama** if the risk band is
   `>= high` or the model is disallowed
4. `ai-guardian guard usage` (MCP: `usage_events(allowed=False)`) → review what
   was caught. The raw prompt is **never stored** — only its length and redacted
   findings, so reviewing the log cannot itself leak the secret
5. `ai-guardian guard anomalies` → confirm the rate of blocked prompts is falling
   after you educate the user or fix the calling integration
6. **Failure branch**: route-through is **opt-in** — anything that calls Ollama
   directly bypasses the guard entirely. If `usage_events` is suspiciously empty
   while `running_models` shows activity, you are looking at un-routed traffic,
   not a clean fleet. A transparent capture proxy is a v0.2 roadmap item; until
   then, treat guard coverage as coverage of what was routed, and say so.

### 3. Detect tampered or silently re-pulled model weights

1. `ai-guardian model list` / `model_details <model>` → read the current digest
   for the models you sanction
2. `pin_model_digest(model, digest)` → pin the trusted digest once, while you
   still trust it. Pinning after a suspected compromise pins the compromise
3. Later (or on a schedule): `ai-guardian guard provenance` (MCP:
   `model_provenance`) → any model whose current digest differs from its pin
   reports `status: DRIFT` — re-pulled or tampered weights
4. `usage_events` around the drift timestamp → was the drifted model used, and
   for what, before you noticed?
5. **Failure branch**: `DRIFT` is a statement about the digest, not about intent
   — a legitimate upgrade drifts identically to tampering. Investigate before
   removing: check whether a `pull_model` appears in the audit trail at
   `~/.ai-guardian/audit.db`. If it does not, treat it as untrusted and remove
   under workflow 1. Re-pin only once you have re-established what the digest
   *should* be.

### 4. Fleet hygiene review before a rollout

1. `ai-guardian overview` → the endpoint's current state at a glance
2. `ai-guardian model list` → the full inventory with allow/deny verdicts
3. `ai-guardian guard provenance` → every pinned model still matching its digest
4. `vram_usage` + `running_models` → what is resident and whether the endpoint
   has headroom for the model you are about to roll out
5. `unload_model <model>` → free VRAM from an idle model without removing it
   (reversible in practice — it reloads on next use)
6. `ai-guardian model pull <model>` → the pull is checked against the allowlist,
   so an unsanctioned rollout is refused rather than merely logged
7. `ai-guardian guard anomalies` → a clean rollup is the exit criterion for the
   review
8. **Failure branch**: if `pull_model` is refused, the model is not on the
   allowlist — widen the policy deliberately with `set_model_allowlist`
   (audited, reversible) rather than working around the guard. If the pull fails
   on VRAM, `unload_model` an idle model first; the audit trail records the
   failed attempt with `status=error` and no undo token.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the host and account you run it under (point it at a runtime the account
cannot administer, or hand the agent only the scan/observe tools). There is no
read-only switch, deny-rules file, or approval gate — content governance (the
model allow/deny policy and the `guarded_generate` block threshold) is a
separate, product-level control that stays.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.ai-guardian/audit.db` (relocatable via `AI_GUARDIAN_AIOPS_HOME`): params, outcome summary, status, duration, and the risk tier. Observed local-LLM usage lives in a **separate** `~/.ai-guardian/usage.db`.
- `AI_GUARDIAN_AUDIT_APPROVED_BY` / `AI_GUARDIAN_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `AI_GUARDIAN_RUNAWAY_MAX=0`.
- `remove_model` supports `--dry-run` + double confirmation at the CLI and records an undo (re-pull); allowlist/denylist writes record an undo → the prior list.
- The scanner is deterministic and offline; findings are redacted so a secret is never re-emitted.

## References

- `references/capabilities.md` — full 21-tool + endpoint reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, optional token, and connectivity
