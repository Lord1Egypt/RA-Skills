---
name: container-host-aiops
slug: container-host-aiops
displayName: "Container Host AIops"
summary: "Governed Docker + Portainer container-host ops: reads, RCA analyses, guarded writes. 38 tools."
license: MIT
homepage: https://github.com/AIops-tools/Container-Host-AIops
tags: [aiops, mcp, governance, container-host]
description: >
  Use this skill whenever the user needs to operate a single container host through the Docker Engine API, Portainer, or Podman — a one-shot host overview; container reads (list/inspect, logs tail, CPU/memory stats, top processes, restart summary); image reads (list, inspect with history, dangling, disk usage); volume reads (list, inspect, dangling); network reads (list, inspect); system reads (info, version, df disk-usage, recent events); Portainer stacks + endpoints; Compose-project rollups (list_compose_stacks, docker+podman); Podman pods (list_pods, podman-only); three flagship analyses — restart-loop RCA (crash-looping containers + cause/action), resource-pressure analysis (CPU/memory vs limits), and image & volume bloat (prune candidates + reclaimable bytes); and eight guarded writes (restart/stop/start/remove a container, prune images/volumes, update resource limits, recreate a Portainer stack).
  Always use this skill for "Docker host overview", "which containers are crash-looping", "restart loop", "why does this container keep restarting", "container CPU/memory usage", "docker logs", "which containers are near their limits", "resource pressure", "dangling images/volumes", "reclaim disk", "prune images", "stop/start/restart a container", "update a container's memory limit", "Portainer stacks", "compose stacks", "Podman pods" when the context is a Docker, Portainer, or Podman container host.
  Do NOT use when the target is a cluster orchestrator, a hypervisor, a storage appliance, a backup product, network device config, or OT/industrial equipment — route those to the appropriate other AIops-tools skill. This is for NON-orchestrator container hosts.
  Governed Docker/Portainer/Podman container-host operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). Exercised against a live Docker Engine 27.5.1 daemon (doctor, overview, the three flagship analyses, and a governed stop_container with audit + undo recorded); the Portainer and Podman API paths are covered by the mock suite only. See docs/VERIFICATION.md.
installer:
  kind: uv
  package: container-host-aiops
argument-hint: "[container/image/volume id or describe your container-host task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["container-host-aiops","uvx"]},"optional":{"env":["CONTAINER_HOST_AIOPS_CONFIG","CONTAINER_HOST_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Container-Host-AIops","emoji":"🐳","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed Docker + Portainer + Podman container-host operations. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency. Multi-platform by construction (a platform registry); a per-target 'platform' field (docker / portainer / podman) selects the API shape.
  All write operations are audited to a local SQLite DB under ~/.container-host-aiops/ (relocatable via CONTAINER_HOST_AIOPS_HOME).
  Connection: a Docker target speaks the Docker Engine API over a local unix socket (httpx uds transport, default /var/run/docker.sock — treat socket access as root-equivalent) or a TCP host; a Portainer target speaks the Portainer management API over HTTPS with an X-API-Key token, and also proxies the Docker API of a managed endpoint at /api/endpoints/{id}/docker/...; a Podman target speaks over the rootful/rootless service socket (autodetected: $XDG_RUNTIME_DIR/podman/podman.sock, then /run/podman/podman.sock), reusing the Docker-compat paths at the root plus libpod-native endpoints (pods) under the libpod prefix.
  Credentials: only Portainer needs a secret — its API token is stored ENCRYPTED in ~/.container-host-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. A local Docker or Podman socket needs no secret. Run 'container-host-aiops init' to onboard, or 'container-host-aiops secret set <target>' to add a Portainer token. The store is unlocked by a master password from CONTAINER_HOST_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var CONTAINER_HOST_<TARGET_NAME_UPPER>_TOKEN is still honoured as a fallback with a deprecation warning (migrate with 'container-host-aiops secret migrate'). The token is sent in the X-API-Key header at request time and held only in memory; secrets are never logged or echoed.
  State-changing operations require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (budget/runaway guard + audit + risk-tier label — it records, it does not authorize) and take a dry_run preview. Prune previews list what would be removed + reclaimable bytes before doing it. Mutating/reversible writes fetch the real before-state first and record a faithful inverse undo descriptor (stop→start, update_container→restore prior limits); irreversible ops (remove, prune, recreate) record only the before-state.
  Webhooks: none — no outbound network calls beyond the configured Docker socket / TCP host or the Portainer API base URL.
  SSL: verify_ssl defaults to true; disable only for a self-signed Portainer / TLS Docker daemon. A unix-socket Docker target does not use TLS.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  VERIFICATION: Exercised against a live Docker Engine 27.5.1 daemon (doctor, overview, the three flagship analyses, and a governed stop_container with audit + undo recorded); the Portainer and Podman API paths are covered by the mock suite only. Community-maintained; not affiliated with or endorsed by Docker/Portainer/Podman — trademarks belong to their owners.
---

# Container Host AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by Docker, Inc., Portainer.io, or any container-platform vendor.** Product and trademark names belong to their owners. Source at [github.com/AIops-tools/Container-Host-AIops](https://github.com/AIops-tools/Container-Host-AIops) under the MIT license.

Governed Docker + Portainer + Podman container-host operations — **38 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.container-host-aiops/` (MCP + CLI alike), a runaway/budget safety guard, and undo-token recording. It records every operation; whether a write is permitted is the agent's or the account's call, not the skill's. A Docker target speaks the Docker Engine API over a unix socket or TCP; a Portainer target speaks the Portainer API (and proxies Docker); a Podman target speaks over its rootful/rootless socket (Docker-compat + libpod). The Portainer API token is stored **encrypted** (`~/.container-host-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk; a local Docker/Podman socket needs no secret.

> **Standalone**: the governance harness is bundled in the package (`container_host_aiops.governance`) — container-host-aiops has no external skill-family dependency. **Verification**: Exercised against a live Docker Engine 27.5.1 daemon (doctor, overview, the three flagship analyses, and a governed stop_container with audit + undo recorded); the Portainer and Podman API paths are covered by the mock suite only. See `docs/VERIFICATION.md`.

## What This Skill Does

| Domain | Tools | Count | Read or Write |
|--------|-------|:-----:|:-------------:|
| **Overview** | one-shot host health | 1 | 1 read |
| **Containers** | list/inspect, logs, stats, top, restart summary | 6 | 6 read |
| **Images** | list, inspect (+history), dangling, disk usage | 4 | 4 read |
| **Volumes** | list, inspect, dangling | 3 | 3 read |
| **Networks** | list, inspect | 2 | 2 read |
| **System** | info, version, df, events | 4 | 4 read |
| **Stacks** | endpoints, stacks, stack detail (Portainer), compose-stack rollup (docker+podman) | 4 | 4 read |
| **Pods (Podman)** | list pods (libpod) | 1 | 1 read |
| **Analyses (flagship)** | restart-loop RCA, resource pressure, image/volume bloat | 3 | 3 read |
| **Writes** | remove container, prune images, prune volumes, recreate stack | 4 | 4 write (high) |
| | restart, stop, start, update container | 4 | 4 write (medium) |

The three analyses accept injected data for offline analysis, or pull live from a configured target. Portainer endpoints/stacks require a `portainer` target; `list_compose_stacks` works on docker or podman; `list_pods` requires a `podman` target.

## Quick Install

```bash
uv tool install container-host-aiops
container-host-aiops init       # interactive wizard: Docker/Podman socket or Portainer target
container-host-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/container-host-aiops
openclaw skills info container-host-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Triage a host (`overview`): version + container state rollup + disk headline
- Find crash-looping containers (`analyze restart-loop` / `restart_loop_rca`): ranked by restart count with a likely cause and action from the exit code, plus a log tail
- Spot resource pressure (`analyze resource-pressure` / `resource_pressure_analysis`): CPU%/mem% vs each container's limits, worst first, with a recommendation
- Reclaim disk (`analyze bloat` / `image_and_volume_bloat`): dangling images + volumes + build cache as prune candidates with reclaimable bytes
- List/inspect containers, images, volumes, networks; tail logs; read stats/top
- Restart/stop/start a container, update its resource limits (reversible), remove a container, prune images/volumes, or recreate a Portainer stack — all with dry-run + double-confirm

**Do NOT use when** the target is a cluster orchestrator, a hypervisor, a storage appliance, a backup product, network device config, or OT/industrial equipment.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Docker / Portainer single-host container ops | **container-host-aiops** (this skill) |
| A cluster orchestrator's workloads/rollouts | a cluster ops skill |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |
| OT / industrial edge (Modbus, OPC-UA, PLC) | the industrial-aiops line |

## Common Workflows

### 1. A container is crash-looping

1. `container-host-aiops doctor` → confirm the socket/endpoint is reachable before you
   trust any read.
2. `container-host-aiops analyze restart-loop` → containers ranked by restart count,
   each with a likely cause read off the real exit code (137 OOM/SIGKILL, 143 SIGTERM,
   139 segfault, 127 bad entrypoint, …), a recommended action, and a log tail.
3. `container-host-aiops container logs <id> --tail 200` → read the actual crash output;
   `container-host-aiops container inspect <id>` → confirm the exit code, restart policy,
   and configured limits the RCA cited.
4. If the cause is memory: `container-host-aiops analyze resource-pressure --mem 75` →
   see how close the container runs to its ceiling, then
   `container-host-aiops manage update <id> '{"Memory": 1073741824}' --dry-run` and
   re-run without `--dry-run` (double-confirm; the write captures the prior limits as its
   undo descriptor).
5. `container-host-aiops manage restart <id>` → bring it up on the new limit, then
   re-run `analyze restart-loop` to confirm the loop stopped.
6. **Failure branch**: if it still loops, the limit was not the cause — reverse the
   change with `container-host-aiops undo list` → `undo apply <id>` (restores the *prior*
   limits, not a guess) and go back to step 3 with the fresh log tail. If the container
   will not stop at all, `manage remove <id> --force --dry-run` first: force-remove is
   high-risk and irreversible, so read the dry-run before committing.

### 2. The host is out of disk

1. `container-host-aiops system df` → where the space actually went (images vs
   containers vs volumes vs build cache).
2. `container-host-aiops analyze bloat` → dangling images, dangling volumes, and build
   cache as ranked prune candidates with reclaimable bytes per item.
3. `container-host-aiops image dangling` and `container-host-aiops volume dangling` →
   eyeball the concrete list before deleting anything. A "dangling" volume holding data
   you still want is the classic way this goes wrong.
4. `container-host-aiops manage prune-images --dry-run` → exactly what would be removed;
   re-run without `--dry-run` (double-confirm, high risk).
5. `container-host-aiops manage prune-volumes --dry-run` → **read this one carefully**;
   volume pruning destroys data and records no undo. Note that Docker's default
   prune removes only ANONYMOUS unused volumes — the preview reports the named
   unused ones it will not touch as `alsoUnusedNamed*`; add `--all` to include
   them. Only then re-run for real.
6. `container-host-aiops system df` again → confirm the space came back.
7. **Failure branch**: pruning is not reversible. If you removed a volume you needed,
   the undo store cannot help — restore from your backup. The dry-run in steps 4–5 is
   the only safety net, which is why both are separate confirm-gated steps.

### 3. "Everything on this box is slow"

1. `container-host-aiops overview` → one-shot: platform/version, container counts by
   state, and the headline resource picture.
2. `container-host-aiops analyze resource-pressure --cpu 80 --mem 80` → running
   containers ranked against **their own limits**, each row citing the measured
   percentage rather than a verdict.
3. `container-host-aiops container stats <id>` and `container-host-aiops container top <id>`
   → confirm the top offender at the process level before you act on it.
4. `container-host-aiops system events` → correlate the pressure with what changed
   (a recent deploy, restart storm, or image pull).
5. Act on the worst offender: `manage update <id> '{"NanoCpus": 2000000000}'` to cap it
   (dry-run first, undo-recorded), or `manage stop <id>` to shed it entirely.
6. **Failure branch**: if capping the top container just moves the pressure elsewhere,
   the host is genuinely undersized rather than misconfigured — reverse your change with
   `undo apply <id>` so you are not left with a half-applied limit, and take the sizing
   result to whoever owns capacity.

### 4. Stack drift after a bad deploy (Portainer)

1. `container-host-aiops stack endpoints` → the endpoints this Portainer manages;
   `container-host-aiops stack list` → the stacks on the one you care about.
2. `container-host-aiops stack detail <stack-id>` → the stack's current definition;
   `container-host-aiops stack compose <stack-id>` → the compose file it is running from.
3. `container-host-aiops container list --running` and
   `container-host-aiops container restarts` → which of the stack's containers are
   actually unhealthy versus merely restarted.
4. `container-host-aiops manage recreate-stack <stack-id> --dry-run` → preview the
   redeploy; re-run without `--dry-run` (double-confirm, high risk).
5. Validate with `container-host-aiops overview` and `analyze restart-loop`.
6. **Failure branch**: `recreate-stack` redeploys from the stack's stored definition — if
   that definition is itself the broken thing, recreating will faithfully reproduce the
   breakage. Fix the compose source in Portainer first, and use
   `container-host-aiops undo list` to check what the session already changed before
   layering another write on top.

### Offline analysis (no live host)

Pass data straight to the analysis tools — `restart_loop_rca(containers=[...])`, `resource_pressure_analysis(samples=[...])`, or `image_and_volume_bloat(dangling_images=..., dangling_volumes=..., df=...)` — to analyse an exported dataset without connecting to a host.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (a read-only Docker socket, a Portainer
account without write scope — writes then fail at the server). There is no
read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.container-host-aiops/audit.db` (relocatable via `CONTAINER_HOST_AIOPS_HOME`): params, outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `CONTAINER_HOST_AUDIT_APPROVED_BY` / `CONTAINER_HOST_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `CONTAINER_HOST_RUNAWAY_MAX=0`.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI; prune previews list what would be removed + reclaimable bytes.
- Mutating/reversible writes fetch the real before-state and record an inverse descriptor (stop→start, update_container→restore prior limits); irreversible ops record only the before-state.

## References

- `references/capabilities.md` — full tool + field reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
