# ceph-aiops CLI reference

> The CLI is a convenience subset; the full 37-tool surface
> is via the MCP server (`ceph-aiops mcp`). Talks to the ceph-mgr Dashboard REST
> API (`https://<host>:8443`, JWT via `POST /api/auth`).

## Setup & diagnostics

```bash
ceph-aiops init                      # interactive onboarding wizard
ceph-aiops doctor [--skip-auth]      # config + secret store + JWT login + mgr-dashboard reachability
ceph-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.ceph-aiops/secrets.enc)

```bash
ceph-aiops secret set <target> [--value <password>]  # store Dashboard password (hidden prompt if no --value)
ceph-aiops secret list                               # names only — values never shown
ceph-aiops secret rm <target>
ceph-aiops secret migrate                            # import legacy plaintext .env (CEPH_<T>_PASSWORD)
ceph-aiops secret rotate-password                    # re-encrypt under a new master password
```

## Read commands

```bash
ceph-aiops overview [--target <t>]        # HEALTH status + active checks + OSD up/in
ceph-aiops health detail                  # decode active HEALTH_WARN/ERR checks → cause + action (RCA)
ceph-aiops health status                  # ceph -s summary
ceph-aiops osd tree                        # OSD tree: up/in, weight, host, device class
ceph-aiops osd df                          # per-OSD utilization, most-full first, near/backfill-full flags
```

## Write commands (governed; risk tier in parentheses)

```bash
ceph-aiops osd reweight <osd_id> <weight> [--dry-run]   # (med) 0.0 = drain; reversible → prior weight
ceph-aiops osd out <osd_id> [--dry-run]                 # (high) mark out — drains data; double confirm
ceph-aiops osd purge <osd_id> [--dry-run]               # (high) purge — irreversible; double confirm
```

The remaining writes (cluster flags, pool quota/pg_num/autoscale/size/create/delete,
RBD image/snapshot create/delete, trigger scrubs, throttle recovery) are exposed
through the **MCP server**, not the CLI.

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target)
- `--dry-run` — print the API call that would be made, change nothing
- Destructive commands (`osd out`, `osd purge`) require `--dry-run` review + double confirmation
- `doctor --skip-auth` — skip the JWT login / connectivity check (config + secret-store checks only)

## Approver env vars (high-risk ops)

```bash
export CEPH_AUDIT_APPROVED_BY='you@example.com'
export CEPH_AUDIT_RATIONALE='draining failed OSD 7 per ticket OPS-123'
```
