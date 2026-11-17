# ai-guardian setup & security guide

> The scanner / policy / risk-band are deterministic offline logic; the Ollama
> API paths need live verification (see `docs/VERIFICATION.md`).

## 1. Install

```bash
uv tool install ai-guardian-aiops
```

## 2. Zero-config default

ai-guardian works **out of the box** against the local Ollama at
`http://localhost:11434` with **no token** — Ollama endpoints usually run open on
a trusted host. You can go straight to:

```bash
ai-guardian doctor        # Ollama reachability + policy summary
ai-guardian overview
```

Run `init` only if you want to name multiple endpoints, add a token, or set a
model allowlist.

## 3. Onboard (optional)

```bash
ai-guardian init
```

The wizard records (non-secret) connection details and the optional model policy
into `~/.ai-guardian/config.yaml`. If the endpoint requires a bearer token (rare
for local Ollama), it is stored **encrypted** into `~/.ai-guardian/secrets.enc`.
Example config:

```yaml
targets:
  - name: local
    host: localhost
    port: 11434
    scheme: http
    verify_ssl: false          # self-signed HTTPS lab certs only
allowed_models:                # shell globs; empty = allow-all
  - "llama3.*"
  - "qwen*"
denied_models: []              # deny patterns always win
pinned_digests: {}             # model -> expected provenance digest (drift detection)
```

The **policy** (`allowed_models` / `denied_models` / `pinned_digests`) is
**non-secret** config — it lives in `config.yaml`, not the encrypted store.

## 4. Optional bearer token

Most local Ollama setups need no token. If yours does:

```bash
ai-guardian secret set local        # hidden prompt for the token
```

For non-interactive use (MCP server / CI / cron), export the master password so
the encrypted store can be unlocked without a prompt:

```bash
export AI_GUARDIAN_AIOPS_MASTER_PASSWORD='your-master-password'
```

### Token security

- A token is **never** written to disk in plaintext. It lives only in
  `~/.ai-guardian/secrets.enc`, encrypted with Fernet (AES-128-CBC + HMAC), the
  key derived from your master password via scrypt. Only a per-store random salt
  and the ciphertext are on disk (chmod 600); the master password is never stored.
- A legacy plaintext env var `AI_GUARDIAN_<TARGET_NAME_UPPER>_TOKEN` is still
  honoured as a fallback with a deprecation warning — migrate with
  `ai-guardian secret migrate` (it imports then renames the old `.env`).
- The token is held only in memory and is never logged or echoed; exception text
  is scrubbed of secret-shaped strings before being written to the audit log.

## 5. Audit-annotation env vars (optional)

The skill does not decide whether a write is permitted — that is the agent's
judgement or the permission of the host/account you run it under. If you want the
audit trail to record *who* ran a destructive op and *why*, set these; they are
recorded on the row, never required, and gate nothing:

```bash
export AI_GUARDIAN_AUDIT_APPROVED_BY='you@example.com'
export AI_GUARDIAN_AUDIT_RATIONALE='decommissioning an unused model'
```

## Two separate SQLite databases

State lives under `~/.ai-guardian/` (relocate the governance state with
`AI_GUARDIAN_AIOPS_HOME`):

- `audit.db` — the **governance audit log**: every ai-guardian *tool call*, with
  risk tier and any approver/rationale.
- `usage.db` — the **observed local-LLM usage log**: route-through prompts
  (`guarded_generate` / `observe_chat`) with model, actor, prompt length, risk
  band, redacted findings, and allowed/blocked. **The raw prompt is never stored.**
- `undo.db` — inverse descriptors for reversible writes (e.g. `remove_model` →
  re-pull, allowlist/denylist → prior list).
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops.

## Verify

```bash
ai-guardian doctor
```

`doctor` checks the config file, the model policy summary, the encrypted store and
its permissions (if present), and (unless `--skip-auth`) Ollama reachability by
hitting `/api/version`. It works with zero config, defaulting to the local Ollama.
