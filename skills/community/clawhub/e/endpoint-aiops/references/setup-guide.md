# endpoint-aiops setup & security guide

> Not yet exercised against a live endpoint-management server (see docs/VERIFICATION.md).

## 1. Install

```bash
uv tool install endpoint-aiops
```

## 2. Create credentials — the shape depends on the dialect

The target's **dialect** decides the port, the API base path *and* how to
authenticate, so create the credential the dialect expects:

**`generic` (default) — a static API key.** In your endpoint-management
server's web UI, create an API key (usually under a Credentials / API Keys
section). It is sent as `Authorization: Bearer <key>` against the REST API base
`<scheme>://<host>:<port><api_path>`.

**`igel-ums` — a UMS administrator account.** IMI does not accept a static
Bearer token; it logs in with HTTP Basic at `POST /umsapi/v3/login` and then
carries the returned `JSESSIONID` cookie. So an `igel-ums` target needs a
`username:` in `config.yaml` plus that account's **password** in the encrypted
store — not an API key. No gateway or auth adapter is needed.

⚠️ Give that account at least **Read/Browse permission at the Devices level**.
With fewer permissions IMI returns **empty lists rather than an error**, so an
under-privileged account looks exactly like an empty fleet. `endpoint-aiops
doctor` warns when a successful login returns no endpoints — do not dismiss it.

⚠️ The `igel-ums` dialect is **documented but not live-verified** (IGEL UMS has
no free edition). See `docs/VERIFICATION.md` in the repository.

## 3. Onboard

```bash
endpoint-aiops init
```

The wizard collects (non-secret) connection details into
`~/.endpoint-aiops/config.yaml` and stores the API key **encrypted** into
`~/.endpoint-aiops/secrets.enc`. Example config:

```yaml
targets:
  - name: ums1
    host: 10.0.0.30
    dialect: igel-ums          # sets IMI paths + port 8443 + /umsapi/v3
    scheme: https              # 'http' for a reverse-proxied server
    verify_ssl: false          # self-signed lab certs only
```

The wizard asks which **dialect** to use and prints the one it configured.
`generic` (the default) is a neutral placeholder — `/api/v2.0` on 443 — that no
shipped management server actually serves; it is only useful once you describe
your server's paths in a `dialect:` block. `igel-ums` targets IGEL UMS via IMI
and is **modelled from vendor documentation, not live-verified**.

`port` and `api_path` are still accepted and win over the dialect's defaults
when you set them.

## 4. Non-interactive use (MCP server / CI / cron)

Export the master password so the encrypted store can be unlocked without a
prompt:

```bash
export ENDPOINT_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Credential security

- The API key is **never** written to disk in plaintext. It lives only in
  `~/.endpoint-aiops/secrets.enc`, encrypted with Fernet (AES-128-CBC + HMAC),
  the key derived from your master password via scrypt. Only a per-store random
  salt and the ciphertext are on disk (chmod 600); the master password itself is
  never stored.
- A legacy plaintext env var `ENDPOINT_<TARGET_NAME_UPPER>_APIKEY` is still
  honoured as a fallback with a deprecation warning — migrate with
  `endpoint-aiops secret migrate` (it imports then renames the old `.env`).
- The key is held only in memory during a session and is never logged or echoed;
  exception text and tracebacks are scrubbed of secret-shaped strings before
  being written to the audit log.

## Audit-annotation env vars (optional)

The skill does not decide whether a write is permitted — that is the agent's
judgement or the connecting account's role. If you want the audit trail to
record *who* ran a destructive op and *why*, set these; they are recorded on the
row, never required, and gate nothing:

```bash
export ENDPOINT_AUDIT_APPROVED_BY='you@example.com'
export ENDPOINT_AUDIT_RATIONALE='why this destructive op is justified'
```

## Governance harness state

State lives under `~/.endpoint-aiops/` (relocate with `ENDPOINT_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with risk tier and any approver/rationale
- `undo.db` — inverse descriptors for reversible writes (e.g. `endpoint_assign_profile`)
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops

## Verify

```bash
endpoint-aiops doctor
```

`doctor` checks the config file, the encrypted store and its permissions,
that an API key is present per target, and (unless `--skip-auth`) connectivity
by hitting `/version`.
