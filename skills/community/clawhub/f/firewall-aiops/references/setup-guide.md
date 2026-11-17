# firewall-aiops setup & security guide

> Both **OPNsense** (fully open-source) and **pfSense CE** (free) are self-hostable, so
> a home lab is the easiest place to run the live checklist in `docs/VERIFICATION.md`.
> The modelled REST paths are the largest verification debt.

## 1. Install

```bash
uv tool install firewall-aiops       # or: pipx install firewall-aiops
```

## 2. What you need per firewall

- **OPNsense** — an **API key + secret** pair (System → Access → Users → edit a user →
  API keys → create). firewall-aiops talks to the REST API on port **443** and presents
  the key+secret as HTTP Basic auth. Enable the OPNsense web GUI / API for the account.
- **pfSense** — the **REST API v2** package (pfSense-pkg-RESTAPI) installed and an **API
  key** issued by it. The API is under `/api/v2/...` on port **443**; the key is sent in
  an `X-API-Key` header.

## 3. Onboard with the wizard

```bash
firewall-aiops init
```

The wizard asks, per target, for the **platform** (`opnsense` / `pfsense`), the
**host**, the **port** (default 443), the **OPNsense API key** (OPNsense only, saved as
`username`), and the **secret** — the OPNsense API secret or the pfSense API key.
Non-secret connection details go to `~/.firewall-aiops/config.yaml`; the secret is
stored **encrypted** in `~/.firewall-aiops/secrets.enc`.

Example `config.yaml`:

```yaml
targets:
  - name: fw1
    platform: opnsense
    host: 192.0.2.1
    port: 443
    username: <opnsense-api-key>
    verify_ssl: true      # the default; set false ONLY for self-signed lab certs
  - name: edge
    platform: pfsense
    host: 192.0.2.2
    port: 443
    verify_ssl: true
    # scheme: http        # https is the default; set http ONLY when the GUI is
    #                     # published over plain HTTP behind a proxy terminating TLS
```

## 4. Master password (for non-interactive / MCP use)

The encrypted store is unlocked by a master password. For the MCP server, CI, or cron,
export it so no prompt is needed:

```bash
export FIREWALL_AIOPS_MASTER_PASSWORD='...'
```

On a TTY the CLI prompts interactively if the env var is unset.

## 5. Verify connectivity

```bash
firewall-aiops doctor
```

`doctor` checks the config file, the encrypted store and its permissions, that each
target has a secret, and (unless `--skip-auth`) live connectivity — a firmware/version
query on both platforms.

## Security notes

- The secret (OPNsense API secret / pfSense API key) is **never** written to disk in
  plaintext — only the scrypt salt and Fernet ciphertext are stored (chmod 600). The
  master password is never stored.
- A legacy plaintext env var `FIREWALL_<TARGET_NAME_UPPER>_SECRET` is honoured as a
  fallback with a deprecation warning (migrate with `firewall-aiops secret migrate`).
- The secret is presented as HTTP Basic auth (OPNsense) or an `X-API-Key` header
  (pfSense) at request time and held only in memory; secrets are never logged or echoed.
- `verify_ssl` defaults to true; set `false` only for self-signed lab certificates.
- `scheme` defaults to `https`; set `http` only when the GUI is published over plain
  HTTP behind a proxy that terminates TLS for it.
- Every MCP tool is audited to `~/.firewall-aiops/audit.db` (relocatable via
  `FIREWALL_AIOPS_HOME`). High-risk writes (`apply_changes`, `reconfigure`, `reboot`)
  are labelled risk=high and audited; `FIREWALL_AUDIT_APPROVED_BY` +
  `FIREWALL_AUDIT_RATIONALE` are optional audit annotations, recorded when set but
  never required.
- No webhooks, no telemetry, no outbound calls beyond the configured OPNsense / pfSense
  REST API. No post-install scripts or background services.
