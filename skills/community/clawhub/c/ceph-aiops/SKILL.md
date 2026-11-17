---
name: ceph-aiops
slug: ceph-aiops
displayName: "Ceph AIops"
summary: "Governed Ceph mgr ops: HEALTH_WARN RCA, OSD/PG/pool/RBD/CephFS/RGW, 37 tools."
license: MIT
homepage: https://github.com/AIops-tools/Ceph-AIops
tags: [aiops, mcp, governance, ceph]
description: >
  Use this skill whenever the user needs to operate or diagnose a Ceph cluster via its ceph-mgr Dashboard REST API — decode a HEALTH_WARN/ERR state into cause + action (cluster_health), read the cluster status, inspect OSDs (tree/df/perf), placement groups (summary/stuck/scrub), pools (list/usable capacity), RBD images and snapshots, CephFS/MDS and RGW status, monitors/managers, slow ops and capacity forecast — plus governed writes (set cluster flags, reweight/mark-in/mark-out/purge OSDs, trigger scrubs, set pool quota/pg_num/autoscale/size, create/delete pools, create/delete RBD images and snapshots, throttle recovery/backfill).
  Always use this skill for "ceph health", "what does this HEALTH_WARN mean", "PG_DEGRADED / OSD_NEARFULL / SLOW_OPS / MON_DOWN", "ceph -s", "which OSD is most full", "drain an OSD", "purge an OSD", "stuck PGs", "overdue scrub", "pool usable capacity", "set pool size / quota", "rebalance is too slow / throttle backfill", "RBD image or snapshot", "MDS behind on trimming", "RGW large omap", "mon quorum", or "days to nearfull" when the context is a Ceph cluster (cephadm, hypervisor-bundled Ceph, or MicroCeph).
  Do NOT use when the target is not Ceph — a hypervisor, a different storage appliance, a backup product, a Kubernetes cluster, or a network device. Route those to the appropriate other AIops-tools skill (negative routing hint only).
  Common Ceph ops with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: ceph-aiops
argument-hint: "[ceph question or describe your cluster task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["ceph-aiops","uvx"]},"optional":{"env":["CEPH_AIOPS_CONFIG","CEPH_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Ceph-AIops","emoji":"🐙","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed Ceph operations. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency. Works against vanilla ceph-mgr (cephadm / hypervisor-bundled Ceph / MicroCeph); no croit and no Kubernetes dependency.
  All write operations are audited to a local SQLite DB under ~/.ceph-aiops/ (relocatable via CEPH_AIOPS_HOME).
  Connection: the ceph-mgr Dashboard REST API over HTTPS (default port 8443). Authentication is username + password exchanged for a short-lived JWT at POST /api/auth; the mgr 'dashboard' module must be enabled. The username lives in config.yaml; the password is stored ENCRYPTED in ~/.ceph-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'ceph-aiops init' to onboard, or 'ceph-aiops secret set <target>' to add one. The store is unlocked by a master password from CEPH_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var CEPH_<TARGET_NAME_UPPER>_PASSWORD is still honoured as a fallback with a deprecation warning (migrate with 'ceph-aiops secret migrate'). The password is held only in memory and exchanged for a JWT at request time; secrets are never logged or echoed.
  State-changing operations require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (pre-check + budget guard + audit + risk-tier label). High-risk destructive ops (osd_mark_out, osd_purge, pool_delete, set_pool_size, rbd_image_delete, rbd_snapshot_delete) require dry-run + double confirmation; reversible writes (osd_reweight, cluster_flag_set, set_pool_quota/pg_num/autoscale, throttle_recovery) capture the prior state and record an inverse undo descriptor.
  Webhooks: none — no outbound network calls beyond the configured ceph-mgr Dashboard REST API.
  SSL: verify_ssl defaults to true; disable only for self-signed lab certificates.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Validation status: behaviour is exercised against mocked Dashboard responses; multi-node rebalance behaviour and the write ops have not been run against a live cluster (a single-node MicroCeph running 'ceph-aiops doctor' is the cheapest live path; see docs/VERIFICATION.md). The Dashboard API has no ETag/pagination, so none are exposed.
---

# Ceph AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by the Ceph project or any storage vendor.** Product and trademark names belong to their owners. Source at [github.com/AIops-tools/Ceph-AIops](https://github.com/AIops-tools/Ceph-AIops) under the MIT license.

Governed Ceph operations via the **ceph-mgr Dashboard REST API** — **37 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.ceph-aiops/`, token/runaway budget guard, undo-token recording, and descriptive risk tiers. The Dashboard password is stored **encrypted** (`~/.ceph-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk. The flagship `cluster_health` turns raw HEALTH_WARN/ERR check codes into plain-language cause + suggested action.

> **Standalone**: the governance harness is bundled in the package (`ceph_aiops.governance`) — ceph-aiops has no external skill-family dependency. Works against vanilla ceph-mgr (cephadm / hypervisor-bundled / MicroCeph); no croit, no Kubernetes.

## What This Skill Does

| Group | Tools | Count | Read or Write |
|-------|-------|:-----:|:-------------:|
| **Health** | cluster_health (flagship RCA), cluster_status | 2 | 2 read |
| **OSD** | osd_tree, osd_df, osd_perf | 3 | 3 read |
| | cluster_flag_set, osd_reweight, osd_mark_in, osd_mark_out, osd_purge | 5 | 5 write |
| **PG** | pg_summary, pg_dump_stuck, scrub_status | 3 | 3 read |
| | trigger_scrub, trigger_deep_scrub | 2 | 2 write |
| **Pool** | pool_ls, pool_df | 2 | 2 read |
| | set_pool_quota, set_pool_pg_num, set_pool_autoscale, pool_create, set_pool_size, pool_delete | 6 | 6 write |
| **RBD** | rbd_ls | 1 | 1 read |
| | rbd_image_create, rbd_snapshot_create, rbd_image_delete, rbd_snapshot_delete | 4 | 4 write |
| **CephFS / RGW** | cephfs_status, rgw_status | 2 | 2 read |
| **Cluster-ops** | mon_status, mgr_status, slow_ops, capacity_forecast | 4 | 4 read |
| | throttle_recovery | 1 | 1 write |
| **Undo** | undo_list, undo_apply | 2 | 2 undo |

Totals: **37 tools — 17 read, 18 write, 2 undo.** The MCP server exposes all 37; the CLI is a convenience subset.

## Quick Install

```bash
uv tool install ceph-aiops
ceph-aiops init       # interactive wizard: mgr host/port/username + encrypted Dashboard password
ceph-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/ceph-aiops
openclaw skills info ceph-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Decode a **HEALTH_WARN/ERR** state (`cluster_health` / `health detail`) — cause + action per active check (`PG_DEGRADED`, `OSD_NEARFULL`, `SLOW_OPS`, `MON_DOWN`, `LARGE_OMAP_OBJECTS`, …)
- One-shot triage (`overview`): HEALTH status + active checks + OSD up/in counts
- Inspect OSDs (`osd_tree` / `osd_df` most-full first / `osd_perf` slowest first), PGs (`pg_summary` / `pg_dump_stuck` / `scrub_status`), pools (`pool_ls` / `pool_df` usable capacity)
- Investigate slow requests (`slow_ops`), MDS trimming lag (`cephfs_status`), RGW large-omap (`rgw_status`), mon quorum (`mon_status`), and days-to-nearfull (`capacity_forecast`)
- Safely **drain + purge** an OSD, change **pool size/quota**, or **throttle a slow rebalance** (governed writes with dry-run + undo)

**Do NOT use when** the target is not Ceph (a hypervisor, another storage appliance, a backup product, a container cluster, or a network device). Route those to the appropriate **other AIops-tools** skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Ceph: HEALTH_WARN RCA, OSD/PG/pool/RBD/CephFS/RGW, rebalance, slow ops | **ceph-aiops** (this skill) |
| Any non-Ceph target (hypervisor, other storage, backup, cluster, network) | the appropriate **other AIops-tools** skill |

## Common Workflows

### 1. "The cluster went HEALTH_WARN overnight" — decode it (read-only)

1. `ceph-aiops doctor` → confirm the mgr Dashboard is reachable and the JWT login works before trusting anything else
2. `ceph-aiops overview` → HEALTH status, the list of active check codes, and OSD up/in counts in one shot
3. `ceph-aiops health detail` (MCP: `cluster_health`) → each **active** check translated into what it means, the likely cause, and a suggested action
4. Drill into the implicated resource: `PG_DEGRADED` → `pg_dump_stuck`; `OSD_NEARFULL` → `ceph-aiops osd df` (most-full first); `SLOW_OPS` → `slow_ops`; `MON_DOWN` → `mon_status`; `LARGE_OMAP_OBJECTS` → `rgw_status`
5. **Failure branch**: if `doctor` fails on auth, the Dashboard password is wrong or the store is locked — re-run `ceph-aiops secret set <target>` (or export `CEPH_AIOPS_MASTER_PASSWORD` for non-interactive use). If `doctor` fails on reachability, the mgr `dashboard` module is likely not enabled; no read is issued against an unauthenticated session.

### 2. Retire a failing OSD: drain, mark out, purge (governed)

1. `ceph-aiops health detail` → confirm the OSD is genuinely the problem (e.g. `OSD_SLOW_PING_TIME`, repeated `SLOW_OPS` on one id) rather than a cluster-wide symptom
2. `ceph-aiops osd df` → confirm the id, and that the remaining OSDs have room to absorb its data before you drain anything
3. `ceph-aiops osd reweight <id> 0.0` → start a gradual drain; reversible, the prior CRUSH weight is captured as the undo descriptor
4. `ceph-aiops osd out <id> --dry-run`, then re-run without `--dry-run` → **high** risk, double confirmation, needs `CEPH_AUDIT_APPROVED_BY`
5. Wait for `ceph-aiops health status` / `pg_summary` to show all PGs `active+clean` — do not purge while backfill is running
6. `ceph-aiops osd purge <id> --dry-run`, then re-run without `--dry-run` → **high**, irreversible
7. **Failure branch**: if client I/O tanks during the drain, stop and reverse — `ceph-aiops undo list` then `ceph-aiops undo apply <id>` restores the prior weight (and `osd_mark_in` reverses the mark-out). Purge has no undo, which is exactly why it comes last and after `active+clean`.

### 3. Recovery is starving client I/O

1. `ceph-aiops health detail` → confirm the cluster is actually backfilling/recovering (`PG_DEGRADED`, `PG_BACKFILL_FULL`) rather than hitting a different bottleneck
2. `slow_ops` → check whether client requests are genuinely being blocked, and by which OSDs
3. `throttle_recovery(max_backfills=1, recovery_max_active=1)` → **med** risk, reversible; the prior `osd_max_backfills` / `osd_recovery_max_active` are captured as the undo descriptor
4. Re-check `slow_ops` and `pg_summary` — recovery is slower but client latency should recover
5. Once the cluster is quiet, raise the values back (or `ceph-aiops undo apply <id>` to restore the exact prior settings)
6. **Failure branch**: if throttling does not help, the bottleneck is not recovery — go back to `osd_perf` (slowest OSDs first) and `mon_status`; do not keep lowering the throttle, you will only extend the degraded window.

### 4. A pool is running out of usable capacity

1. `ceph-aiops overview` → look for `POOL_NEARFULL` / `OSD_NEARFULL` among the active checks
2. `pool_df` → per-pool usage with **usable capacity = raw ÷ size** (a `size=3` pool reports a third of raw — this is where most "but the disks aren't full" confusion comes from)
3. `capacity_forecast` → days-to-nearfull at the current fill rate, so you know whether this is a this-week problem or a this-quarter one
4. Buy time reversibly first: `set_pool_quota` (med, undo → prior quota) or `set_pool_autoscale` (med, undo) to let pg_num track the new size
5. Only if a replica change is genuinely the answer: `set_pool_size --dry-run` then the real call — **high** risk, because lowering `size` reduces durability and any change forces cluster-wide data movement
6. **Failure branch**: if the resulting rebalance saturates the cluster, apply workflow 3 (`throttle_recovery`) rather than reverting the size mid-flight; if the size change itself was wrong, `ceph-aiops undo apply <id>` replays the recorded prior value — but expect a second full rebalance.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (a ceph-mgr Dashboard account with a
read-only role — writes then fail at the mgr). There is no read-only switch,
policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.ceph-aiops/audit.db` (relocatable via `CEPH_AIOPS_HOME`): params, outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `CEPH_AUDIT_APPROVED_BY` / `CEPH_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `CEPH_RUNAWAY_MAX=0`.
- Destructive writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI.
- Reversible writes fetch the real before-state and record an inverse descriptor (`osd_reweight`→restore prior weight, `cluster_flag_set`→toggle back); irreversible ops (`osd_purge`, `pool_delete`, RBD deletes) record only the before-state.

## References

- `references/capabilities.md` — full tool → API-path → returns reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
