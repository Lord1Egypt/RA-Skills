# ai-guardian CLI reference

> The CLI is a convenience subset; the full 21-tool surface
> is via MCP (`ai-guardian mcp`). Works zero-config against a local Ollama
> (`http://localhost:11434`).

## Setup & diagnostics

```bash
ai-guardian init                      # interactive wizard: Ollama endpoint(s) + optional token + model allowlist
ai-guardian doctor [--skip-auth]      # config + policy summary + Ollama reachability (/api/version)
ai-guardian mcp                       # start the MCP server (stdio transport)
```

## Overview

```bash
ai-guardian overview [--target <t>]   # models installed/running, shadow count, observed-usage stats
```

## Models (inventory + guarded lifecycle)

```bash
ai-guardian model list [--target <t>]         # installed models with allow/deny verdicts
ai-guardian model running [--target <t>]      # loaded models (VRAM + expiry)
ai-guardian model details <model>             # license / parameters / capabilities
ai-guardian model pull <model>                # pull a model (refused if it violates policy)
ai-guardian model remove <model> [--dry-run]  # (high) delete a local model; dry-run + double confirm; undo re-pull
ai-guardian model unload <model>              # (medium) evict from VRAM (keep_alive:0)
```

## Guard (policy, provenance, prompt scanning, usage, anomalies)

```bash
ai-guardian guard policy                      # current model allow/deny policy + digest pins
ai-guardian guard provenance [--target <t>]   # installed digests vs their pins (drift detection)
ai-guardian guard scan "<text>"               # deterministic scan → findings + risk band (no model call)
ai-guardian guard usage [--limit 50]          # query the observed-usage log
ai-guardian guard anomalies [--target <t>]    # rollup: shadow models, digest drift, high-risk + blocked prompts
```

## Secrets (encrypted store ~/.ai-guardian/secrets.enc)

A bearer token is optional (rare for local Ollama).

```bash
ai-guardian secret set <target> [--value <token>]  # store a token (hidden prompt if no --value)
ai-guardian secret list                            # names only — values never shown
ai-guardian secret rm <target>
ai-guardian secret migrate                         # import legacy plaintext .env (AI_GUARDIAN_<T>_TOKEN)
ai-guardian secret rotate-password                 # re-encrypt under a new master password
```

## Common options & notes

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target, i.e. the local Ollama)
- `--dry-run` (on `model remove`) — print the API call that would be made, change nothing
- `model remove` requires two confirmations; set `AI_GUARDIAN_AUDIT_APPROVED_BY` (+ `AI_GUARDIAN_AUDIT_RATIONALE`) to record who/why on the audit row (optional)
- The route-through guards (`guarded_generate` / `observe_chat`) are MCP-only; use `guard scan` on the CLI to pre-check text without a model call
