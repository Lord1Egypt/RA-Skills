# container-host-aiops CLI reference

> Covers the Docker Engine API (unix socket or TCP), Portainer (management API), and
> Podman (rootful/rootless socket — Docker-compat + libpod). The Docker path has been
> exercised against a live daemon; Portainer and Podman responses are mock-validated
> only — see `docs/VERIFICATION.md`.

## Setup

```bash
container-host-aiops init                      # interactive wizard (Docker/Podman socket or Portainer)
container-host-aiops doctor                     # verify config, secrets, connectivity
                                                #   Docker/Podman: GET /version · Portainer: GET /api/endpoints
container-host-aiops doctor --skip-auth         # config/secret checks only (no connectivity)
```

## Secrets (Portainer only)

```bash
container-host-aiops secret set <target> [--value <token>]  # store a Portainer token (hidden prompt if no --value)
container-host-aiops secret list                            # list target names with a stored token
container-host-aiops secret rm <target>                     # delete a stored token
container-host-aiops secret migrate                         # import a legacy plaintext .env
container-host-aiops secret rotate-password                 # re-encrypt under a new master password
```

## Overview

```bash
container-host-aiops overview [--target <name>]   # one-shot host health
```

## Containers

```bash
container-host-aiops container list [--running]            # all states, or only running
container-host-aiops container inspect <id>
container-host-aiops container logs <id> [--tail 200]
container-host-aiops container stats <id>                  # CPU% / memory%
container-host-aiops container top <id>                    # processes inside
container-host-aiops container restarts                    # restart-count + exit-code summary
```

## Images / Volumes / Networks

```bash
container-host-aiops image list [--all]
container-host-aiops image inspect <id>                    # + build history
container-host-aiops image dangling
container-host-aiops image disk-usage

container-host-aiops volume list
container-host-aiops volume inspect <name>
container-host-aiops volume dangling

container-host-aiops network list
container-host-aiops network inspect <id>
```

## System

```bash
container-host-aiops system info
container-host-aiops system version
container-host-aiops system df                             # disk-usage breakdown
container-host-aiops system events [--since 3600] [--type container]
```

## Stacks

```bash
container-host-aiops stack endpoints          # Portainer target
container-host-aiops stack list               # Portainer target
container-host-aiops stack detail <stack_id>  # Portainer target
container-host-aiops stack compose            # Compose projects by label (docker OR podman) + health rollup
```

## Pods (Podman target)

```bash
container-host-aiops pod list                 # Podman pods (libpod); errors on docker/portainer
```

## Analyses (flagship)

```bash
container-host-aiops analyze restart-loop [--threshold 3]
container-host-aiops analyze resource-pressure [--cpu 80] [--mem 80]
container-host-aiops analyze bloat
```

## Manage (guarded writes — `--dry-run` + double confirmation)

```bash
container-host-aiops manage restart <id> [--dry-run]
container-host-aiops manage stop <id> [--dry-run]          # undo: start
container-host-aiops manage start <id> [--dry-run]         # undo: stop
container-host-aiops manage update <id> '{"Memory":1073741824}' [--dry-run]   # undo restores prior limits
container-host-aiops manage remove <id> [--force] [--volumes] [--dry-run]     # high; captures full inspect first
container-host-aiops manage prune-images [--all] [--dry-run]                  # high; dry-run lists candidates
container-host-aiops manage prune-volumes [--all] [--dry-run]                 # high; anonymous only unless --all
container-host-aiops manage recreate-stack <stack_id> [--endpoint-id N] [--dry-run]   # high; Portainer
```

## MCP server

```bash
container-host-aiops mcp          # stdio transport (or: container-host-aiops-mcp)
```

## Notes

- Every command accepts `--target <name>` (`-t`) to pick a configured host; omit for the default (first) target.
- The full 36-tool surface (all reads + writes) is exposed through the MCP server; the CLI is a convenient subset.
- `stack endpoints`/`list`/`detail` and `recreate-stack` require a `portainer` target; `stack compose` works on docker or podman; `pod list` requires a `podman` target.
