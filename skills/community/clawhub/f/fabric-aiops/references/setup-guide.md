# fabric-aiops setup & security guide

> Not yet exercised against a live controller of any platform (Meraki
> organization, Catalyst Center appliance, CloudVision Portal instance, or
> UniFi controller) — see docs/VERIFICATION.md. Community-maintained; not affiliated
> with or endorsed by Cisco/Meraki/Arista/Ubiquiti.

## 1. Install

```bash
uv tool install fabric-aiops
```

## 2. Create the platform credential

**Cisco Meraki Dashboard (`platform: meraki`)** — in the Dashboard:
**Organization → Settings → API access → Generate API key**. Copy the key.
fabric-aiops sends it as `Authorization: Bearer <key>` (or, with
`auth_style: meraki-key`, `X-Cisco-Meraki-API-Key`) against the Dashboard API
base `https://api.meraki.com/api/v1`.

**Cisco Catalyst Center (`platform: catalyst`)** — use a Catalyst Center
account (a read-only role suffices for the current read subset) and store the
secret as a single `username:password` string. fabric-aiops exchanges it via
`POST /dna/system/api/v1/auth/token` (HTTP Basic) for a short-lived (~1 h)
`X-Auth-Token`, attached per request and auto-refreshed once on a 401. A
`base_url` is required (`https://<catalyst-center-host>`).

**Arista CloudVision Portal (`platform: cvp`)** — create a service-account
token in CloudVision: **Settings → Access Control → Service Accounts**.
fabric-aiops sends it as `Authorization: Bearer <token>`. A `base_url` is
required (`https://<cvp-host>`).

**UniFi Network (`platform: unifi`)** — create an **API key** in the UniFi
console (UniFi OS: **Settings → Control Plane → Integrations**; self-hosted
Network Server 9.0+: the admin's API-key page). fabric-aiops sends it as
`X-API-KEY` on every request (stateless). The legacy cookie login
(`POST /api/login`) is **not** supported — use an API key. A `base_url` is
required and encodes the controller layout:
- classic self-hosted controller: `https://<host>:8443`
- UniFi OS console (UDM / UDM-Pro / Cloud Key Gen2):
  `https://<console>/proxy/network` — keep the `/proxy/network` suffix; every
  API path is issued relative to it.

Set the target's `org_id` to the site's short name (e.g. `default`) —
device-scoped calls (device get, switch ports, restart) use it as the
`/api/s/{site}/` scope.

**Cisco ACI (`platform: aci`)** — use an APIC local or remote user whose role is
**read-only** (every ACI read is a GET; only the login is a POST) and whose
security domains cover the tenants you want to trace. An object outside them
may come back as an empty answer — reported as "does not exist, or not visible
to this account" because APIC answers both the same way — or as a 403, reported
as a privilege problem, not an expired session. After a refused login the tool
waits 60 s before sending the password again, so a changed password cannot turn
into one login attempt per read. Store
the secret as a single `username:password` string. fabric-aiops logs in via
`POST /api/aaaLogin.json`, carries the session cookie APIC returns, extends the
session via `/api/aaaRefresh.json` at half its `refreshTimeoutSeconds`, and logs
in again once if APIC answers 401/403. A `base_url` is required
(`https://<apic-host>`); `org_id` is not used. ACI answers the Meraki-shaped
tools with a teaching error — use `fabric-aiops aci trace | segment | faults`.

## 3. Onboard

```bash
fabric-aiops init
```

The wizard asks for the platform (`meraki` / `catalyst` / `cvp` / `unifi`), collects
(non-secret) connection details into `~/.fabric-aiops/config.yaml`, and stores
the secret **encrypted** into `~/.fabric-aiops/secrets.enc`. Example config:

```yaml
targets:
  - name: org1
    platform: meraki
    org_id: "123456"            # default organization id (optional)
    verify_ssl: true
    # base_url: https://api.meraki.eu/api/v1   # override only for a region/proxy
    # auth_style: meraki-key                    # use X-Cisco-Meraki-API-Key instead of Bearer
  - name: campus
    platform: catalyst
    base_url: https://catalyst.example.com     # required (per-install)
    org_id: "site-uuid"          # default site id (optional)
    # verify_ssl: false          # only for self-signed lab controllers
  - name: dc-fabric
    platform: cvp
    base_url: https://cvp.example.com          # required (per-install)
    org_id: "root"               # default container key (optional)
  - name: home-lab
    platform: unifi
    base_url: https://unifi.example.com:8443   # classic controller
    # base_url: https://console.example.com/proxy/network   # UniFi OS console
    org_id: "default"            # site short name (fills /api/s/{site}/ scopes)
```

## 4. Non-interactive use (MCP server / CI / cron)

Export the master password so the encrypted store can be unlocked without a
prompt:

```bash
export FABRIC_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Credential security

- The controller secret (Meraki API key / Catalyst Center `username:password`
  / CVP service-account token / UniFi API key) is **never** written to disk in plaintext. It lives only in
  `~/.fabric-aiops/secrets.enc`, encrypted with Fernet (AES-128-CBC + HMAC),
  the key derived from your master password via scrypt. Only a per-store random
  salt and the ciphertext are on disk (chmod 600); the master password itself is
  never stored.
- A legacy plaintext env var `FABRIC_<TARGET_NAME_UPPER>_APIKEY` is still honoured
  as a fallback with a deprecation warning — migrate with `fabric-aiops secret
  migrate` (it imports then renames the old `.env`).
- The key is held only in memory during a session and is never logged or echoed;
  exception text and tracebacks are scrubbed of secret-shaped strings before
  being written to the audit log.

## Audit-annotation env vars (optional)

The skill does not decide whether a write is permitted — that is the agent's
judgement or the connecting controller account's role. If you want the audit
trail to record *who* ran a destructive op and *why*, set these; they are
recorded on the row, never required, and gate nothing:

```bash
export FABRIC_AUDIT_APPROVED_BY='you@example.com'
export FABRIC_AUDIT_RATIONALE='why this destructive op is justified'
```

## Governance harness state

State lives under `~/.fabric-aiops/` (relocate with `FABRIC_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with risk tier and any approver/rationale
- `undo.db` — inverse descriptors for reversible writes (e.g. `update_device`,
  `bind_network_to_template`)
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops (also your first line of defense against Dashboard API
  rate limits)

## Verify

```bash
fabric-aiops doctor
```

`doctor` checks the config file, the encrypted store and its permissions, that a
secret (and, for on-prem platforms, a `base_url`) is present per target, and
(unless `--skip-auth`) connectivity via the canonical top-of-hierarchy read —
Meraki organizations, Catalyst Center sites, CVP containers, or UniFi sites —
which also exercises the platform's full auth flow (including the Catalyst
Center session-token exchange and, on unifi, the `X-API-KEY` header against
the configured base URL — the fastest way to confirm a UniFi OS console's
`/proxy/network` prefix is right).
