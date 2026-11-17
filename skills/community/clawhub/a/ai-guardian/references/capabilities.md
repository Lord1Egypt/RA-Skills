# ai-guardian capabilities

> 21 MCP tools (11 read, 8 write, 2 undo) over Ollama's REST API
> (default `http://localhost:11434`, usually no auth). The scanner / policy /
> risk-band are pure deterministic offline logic; the Ollama paths need live
> verification.

## Read tools (10)

| Tool | Ollama endpoint / pure | Returns |
|------|------------------------|---------|
| `list_models` | `GET /api/tags` | per-model: name, digest, sizeBytes, family, parameterSize, quantization, modifiedAt, **allowed** (allow/deny verdict — shadow → `false`) |
| `running_models` | `GET /api/ps` | per-loaded-model: name, digest, sizeVramBytes, expiresAt, allowed |
| `model_details` | `POST /api/show` | model, license, family, parameterSize, quantization, capabilities[] |
| `server_status` | `GET /api/version` | reachable, version (or error) |
| `vram_usage` | `GET /api/ps` | loadedModels, totalVramBytes, budgetBytes, overBudget, models[] |
| `policy_view` | pure (reads config) | allowedModels, deniedModels, pinnedDigests, note |
| `model_provenance` | `GET /api/tags` + config | driftCount, pinnedCount, models[]{model, currentDigest, pinnedDigest, status: ok/DRIFT/unpinned} |
| `scan_prompt` | **pure** (no model call) | riskBand, findingCount, byCategory, findings[]{category, kind, severity, preview(redacted)} |
| `usage_events` | reads `usage.db` | count, events[] (filter by model / risk_level / allowed / since / limit) |
| `anomaly_report` | `GET /api/tags` + `usage.db` | shadowModels[], digestDrift[], highRiskPrompts, blockedPrompts, totalObserved |

## Write tools (8)

| Tool | Risk | Ollama endpoint / effect | Undo / safety |
|------|------|--------------------------|---------------|
| `pull_model` | medium | `POST /api/pull` | **refused if it violates the deny/allow policy** |
| `remove_model` | **high** | `DELETE /api/delete` | captures the model manifest; records an undo (`pull_model` re-pull); CLI `--dry-run` + double confirm |
| `unload_model` | medium | `POST /api/generate` `keep_alive:0` | evict from VRAM; no undo |
| `set_model_allowlist` | medium | writes `config.yaml` | undo → prior allowlist (immutable replace, not append) |
| `set_model_denylist` | medium | writes `config.yaml` | undo → prior denylist (deny patterns always win) |
| `pin_model_digest` | medium | writes `config.yaml` | pin a model's expected provenance digest; undo → prior pin |
| `guarded_generate` | medium | scan → policy-gate → record → `POST /api/generate` if allowed | blocks when risk band `>= block_threshold` (default `high`) OR model disallowed; blocked never reaches Ollama; raw prompt never stored |
| `observe_chat` | medium | scan → policy-gate → record → `POST /api/chat` if allowed | same, for OpenAI-style `[{role,content}]` messages |

## The deterministic scanner (behind `scan_prompt` / the route-through guards)

Pure, offline, no network. Categories and weighted risk band:

- **secrets** — AWS access key (`AKIA…`, critical), private-key blocks (critical),
  GitHub token (critical), OpenAI `sk-…` (critical), Slack token (high), JWT
  (high), Google API key (high), assigned `api_key=…` / high-entropy fallback
  (medium).
- **pii** — email (low), US SSN (high), credit card **with a Luhn check** (high).
- **code_leak** — source/config heuristics (fires on >= 2 signals, medium).
- **jailbreak** — ignore-instructions / DAN / developer-mode / system-prompt-leak
  signatures (medium).
- **risk band** — weighted sum (low=1, medium=3, high=7, critical=15); bands
  low 0-2, medium 3-6, high 7-14, critical >=15 — and **any single critical
  dominates**. Findings are **redacted** (short masked preview only).

## Out of scope (by design)

- GPU inference-**cluster** serving/ops (multi-node) — a different AIops-tools tool
- Model training / fine-tuning
- Non-Ollama local-LLM runtimes
- ~~A transparent capture proxy for other clients' traffic~~ — **shipped**:
  `ai-guardian proxy serve` (CLI-only; it blocks while listening, so an MCP tool
  that started it would hang the caller). `proxy_guidance` composes the command
  and states the caveat: it is a **chokepoint, not an enforcement boundary**

Want one of these? Open an issue or PR — feedback and contributions welcome.
