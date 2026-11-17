---
name: endpoint-aiops
slug: endpoint-aiops
displayName: "Endpoint AIops"
summary: "Governed managed-endpoint ops — login-storm & drift analysis, 13 MCP tools with audit/budget/undo."
license: MIT
homepage: https://github.com/AIops-tools/Endpoint-AIops
tags: [aiops, mcp, governance, endpoint]
description: >
  Use this skill whenever the user needs to operate a managed-endpoint fleet (thin clients, VDI endpoints, centrally-managed devices) — a one-shot fleet health overview, endpoint inventory (list/get), a composite per-endpoint health score (which endpoints are worst?), login & boot sessions, login-storm analysis (detect morning login storms and rank the slowest login/boot contributors), patch/config drift (which endpoints deviate from the fleet baseline), and two guarded writes (assign a config profile, reboot an endpoint).
  Always use this skill for "endpoint fleet overview", "list managed endpoints", "which endpoints are worst", "endpoint health score", "rank endpoints by risk", "why is login slow this morning", "login storm", "boot time analysis", "patch drift", "config drift", "which endpoints are behind on patches", "assign a profile to an endpoint", or "reboot a thin client" when the context is an endpoint-management fleet.
  Do NOT use when the target is OT / industrial equipment (Modbus, OPC-UA, PLCs — use industrial-aiops), a hypervisor, a storage appliance, a backup product, a Kubernetes cluster, or a network device (negative routing hints only).
  Covers common managed-endpoint operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). The test suite is mock-based; not yet exercised against a live management server (see docs/VERIFICATION.md).
installer:
  kind: uv
  package: endpoint-aiops
argument-hint: "[endpoint id or describe your fleet task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["endpoint-aiops","uvx"]},"optional":{"env":["ENDPOINT_AIOPS_CONFIG","ENDPOINT_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Endpoint-AIops","emoji":"💻","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed managed-endpoint operations. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.endpoint-aiops/ (relocatable via ENDPOINT_AIOPS_HOME).
  Credentials: the endpoint-management server's API key is stored ENCRYPTED in ~/.endpoint-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'endpoint-aiops init' to onboard, or 'endpoint-aiops secret set <target>' to add one. The store is unlocked by a master password from ENDPOINT_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var ENDPOINT_<TARGET_NAME_UPPER>_APIKEY is still honoured as a fallback with a deprecation warning (migrate with 'endpoint-aiops secret migrate'). The credential is presented using the scheme the target's dialect declares — a static Authorization: Bearer header for the generic dialect, or an HTTP Basic login yielding a session cookie for igel-ums (which also needs a 'username' on the target). It is held only in memory; credentials are never logged or echoed.
  State-changing operations (assign-profile, reboot) require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (pre-check + budget guard + audit + risk-tier label). endpoint_assign_profile is high-risk and reversible (captures the prior profile, records an inverse reassign undo descriptor); endpoint_reboot is medium-risk with no undo (a reboot has no safe inverse).
  Webhooks: none — no outbound network calls beyond the configured endpoint-management REST API.
  SSL: verify_ssl defaults to true; disable only for self-signed lab certificates.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Verification status: the test suite is mock-based; the REST paths are modelled generically (/endpoints, /sessions, /version) and have not yet been exercised against a live server — docs/VERIFICATION.md defines the checklist.
---

# Endpoint AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by any endpoint-management vendor.** Product and trademark names belong to their owners. Source at [github.com/AIops-tools/Endpoint-AIops](https://github.com/AIops-tools/Endpoint-AIops) under the MIT license.

Governed managed-endpoint operations — **13 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.endpoint-aiops/`, token/runaway budget guard, undo-token recording, and descriptive risk tiers. The management-server API key is stored **encrypted** (`~/.endpoint-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package (`endpoint_aiops.governance`) — endpoint-aiops has no external skill-family dependency. The test suite is mock-based; a live management server has not yet been exercised (see `docs/VERIFICATION.md`).

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|:-----:|:-------------:|
| **Overview** | fleet health overview | 1 | 1 read |
| **Inventory** | endpoint list, get, health score | 3 | 3 read |
| **Sessions** | session list, login-storm analysis | 2 | 2 read |
| **Drift** | drift report, patch status, patch compliance | 3 | 3 read |
| **Remediation** | assign profile (high) | 1 | 1 write |
| | reboot (medium) | 1 | 1 write |

The analysis tools (`login_storm_analysis`, `drift_report`, `patch_status`, `patch_compliance`, `endpoint_health_score`) accept injected records for pure/offline analysis; `endpoint_health_score` and `patch_compliance` are injected-only, the others also pull live from a configured target.

## Quick Install

```bash
uv tool install endpoint-aiops
endpoint-aiops init       # interactive wizard: connection + encrypted API key
endpoint-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/endpoint-aiops
openclaw skills info endpoint-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Triage a fleet (`overview`): online/offline counts, stale endpoints, agent/patch spread
- Rank the fleet by risk (`endpoint_health_score`): a composite 0-100 per-endpoint score, worst first, with every deduction cited
- Diagnose a morning login storm (`session storm` / `login_storm_analysis`) and find the slowest login/boot contributors
- Find endpoints drifted from the fleet baseline (`drift report`) or behind on patches (`drift patch`)
- Assign a config profile to an endpoint (reversible) or reboot one (dry-run + double-confirm)

**Do NOT use when** the target is OT/industrial equipment (use industrial-aiops), a hypervisor, a storage appliance, a backup product, a container cluster, or a network device.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Managed-endpoint fleet: login storms, drift, profiles | **endpoint-aiops** (this skill) |
| OT / industrial edge (Modbus, OPC-UA, PLC, PROFINET) | the **industrial-aiops** line |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |
| Container/cluster lifecycle | a cluster ops skill |

## Common Workflows

### "Nobody can log in this morning" — diagnose the 9am login storm

1. `endpoint-aiops overview` → is this fleet-wide (offline/stale counts spiking) or confined to logins?
2. `endpoint-aiops session storm --since-hours 12 --window-s 300 --min-concurrent 10` → storm episodes with peak concurrency and distinct users/endpoints, plus `slowestByLogin` / `slowestByBoot`
3. `endpoint-aiops session list --since-hours 12` → inspect the raw sessions behind a suspicious episode (confirm the timestamps, don't trust the summary alone)
4. `endpoint-aiops drift report` → cross-check the laggards; a stray agent version or divergent profile is a common cause of slow logins
5. **Failure branch**: if `session storm` reports no episodes but users still complain, widen the window (`--window-s 900`) and lower `--min-concurrent` before concluding there is no storm; if the CLI errors on connectivity, run `endpoint-aiops doctor` first — the analysis is only as good as the session feed.

### Bring a drifted endpoint back to the fleet baseline (reversible)

1. `endpoint-aiops drift report` → the drifted endpoints and exactly which fields deviate from the fleet-majority baseline
2. `endpoint-aiops endpoint get <id>` → confirm you are about to change the right device and note its current profile
3. `endpoint-aiops endpoint assign-profile <id> <profile-id> --dry-run` → preview the exact `POST /endpoints/<id>/profile` call, changes nothing
4. `endpoint-aiops endpoint assign-profile <id> <profile-id>` → double confirmation; `high` risk. The prior profile is captured and an inverse reassign undo descriptor is recorded
5. **Failure branch**: if the endpoint misbehaves on the new profile, `endpoint-aiops undo list` then `endpoint-aiops undo apply <id>` restores the *captured* prior profile (not a guess); re-run `drift report` to confirm the fleet picture.

### Patch-compliance sweep before a maintenance window

1. `endpoint-aiops drift patch --target-patch 2024-06` → distribution of patch levels plus the endpoints behind the target
2. `endpoint-aiops endpoint list` → resolve the behind-target ids to hostnames/owners for the change ticket
3. `endpoint-aiops overview` → check how many of those are currently offline (an offline endpoint will not take the patch)
4. Reboot a stuck endpoint that has staged its patch: `endpoint-aiops endpoint reboot <id> --dry-run`, then without `--dry-run` (double confirmation)
5. **Failure branch**: `endpoint_reboot` is `medium` risk and declares **no undo** — a reboot has no safe inverse. If the endpoint does not come back, the audit record in `~/.endpoint-aiops/audit.db` holds its prior online state for the incident write-up; recovery is out-of-band (console/PXE), not via this tool.

### Offline post-incident analysis (no live server)

1. Export the incident's session and endpoint records from the management server into JSON
2. Call the analysis tools with injected records — `login_storm_analysis(sessions=[...])`, `drift_report(endpoints=[...])`, `patch_compliance(endpoints=[...])`, `endpoint_health_score(endpoints=[...])` — no connection or credentials required
3. `endpoint_health_score` returns a composite 0-100 per endpoint, worst first, with every deduction cited — use it to rank the remediation queue
4. **Failure branch**: if a tool rejects the injected records, the export is missing fields the analysis needs (e.g. session start/login-duration, or endpoint patch level) — re-export rather than hand-patching the data, so the numbers stay traceable to the source.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (a management-console account or API token
scoped to a read-only role — writes then fail at the server). There is no
read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.endpoint-aiops/audit.db` (relocatable via `ENDPOINT_AIOPS_HOME`): params, outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `ENDPOINT_AUDIT_APPROVED_BY` / `ENDPOINT_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `ENDPOINT_RUNAWAY_MAX=0`.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI.
- Reversible writes fetch the real before-state and record an inverse descriptor (`endpoint_assign_profile`→restore prior profile); the reboot (no safe inverse) records only the before-state.

## References

- `references/capabilities.md` — full tool + field reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
