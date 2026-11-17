# endpoint-aiops capabilities

> 13 MCP tools (10 read, 3 write). REST paths are modelled generically against
> an endpoint-management API and have not yet been exercised live
> (see docs/VERIFICATION.md).

## Read tools (10)

| Tool | REST path | Returns |
|------|----------------|---------|
| `overview` | `GET /endpoints` (fold) | total, online, offline, stale[], agentVersionSpread, patchLevelSpread |
| `endpoint_list` | `GET /endpoints` | id, hostname, os, osBuild, agentVersion, patchLevel, profileId, online, lastSeenHours |
| `endpoint_get` | `GET /endpoints/{id}` | single endpoint detail (normalised) |
| `endpoint_health_score` | injected only | endpointsEvaluated, baseline{agentVersion,patchLevel,source}, summary{healthy,degraded,critical}, worst{items[]{endpoint,score,band,reasons[]},returned,limit,truncated}, note |
| `session_list` | `GET /sessions?since_hours=` | endpoint, user, loginMs, bootMs, timestamp, result |
| `login_storm_analysis` | `GET /sessions` or injected | stormCount, storms/slowestByLogin/slowestByBoot (each {items[],returned,limit,truncated}), slowLoginCount, failedLogins, thresholds |
| `drift_report` | `GET /endpoints` or injected | baseline, driftByField, driftedEndpoints{items[],returned,limit,truncated}, drifted/compliant counts |
| `patch_status` | `GET /endpoints` or injected | targetPatch, distribution, behind{items[],returned,limit,truncated}, behindCount |
| `patch_compliance` | injected only | endpointsEvaluated, targetPatch, targetSource, slaTargetPct, complianceRatePct, compliantCount, verdict, nonCompliantCount, nonCompliant{items[],returned,limit,truncated}, note |
| `undo_list` | local undo store | recorded, not-yet-applied reversible writes: undos[]{undoId, ts, originalTool, inverseTool, note}, returned, limit, truncated |

The analysis tools accept an injected `sessions=` / `endpoints=` list for
pure/offline analysis. `login_storm_analysis`, `drift_report` and `patch_status`
also pull live from a configured `target`; `endpoint_health_score` and
`patch_compliance` are injected-only (they score rows you already hold, e.g.
from `endpoint_list`).

## Write tools (3)

| Tool | Risk | REST path | Undo / safety |
|------|------|----------------|---------------|
| `endpoint_assign_profile` | **high** | `POST /endpoints/{id}/profile` | captures the prior profile; records an inverse "reassign prior profile" undo descriptor; CLI double-confirm + dry-run |
| `endpoint_reboot` | medium | `POST /endpoints/{id}/reboot` | captures prior online state; no safe inverse, no undo; CLI double-confirm + dry-run |
| `undo_apply` | medium | local undo store → inverse tool | executes a recorded inverse; the inverse runs through its own governed tool (its real risk tier is recorded there); single-use token; supports `dry_run` |

## Out of scope (by design)

- Endpoint **enrollment / de-enrollment**
- Image / OTA / firmware push
- Profile CRUD (create/delete config profiles) and user/group management
- OT / industrial equipment (use the `industrial-aiops` line)

Want one of these? Open an issue or PR — feedback and contributions welcome.

## Two payload conventions worth knowing

**Absent is not empty.** A field the management server did not report comes back
as `null`, never as `""`. The key is always present, so "the server had no value
for this" is visible rather than inferred.

**Capped lists announce themselves.** Every list that a `limit` can cut short is
a truncation envelope:

```json
{"items": [...], "returned": 25, "limit": 25, "truncated": true}
```

`truncated` is measured against the full result, not guessed from the returned
count matching the limit. When it is `true`, re-run with a higher `limit`.
Companion totals (`driftedCount`, `behindCount`, `stormCount`,
`nonCompliantCount`, the health `summary`) are always the full, uncapped
figures.
