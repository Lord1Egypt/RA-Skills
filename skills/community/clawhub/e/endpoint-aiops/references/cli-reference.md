# endpoint-aiops CLI reference

> REST paths are modelled generically against an endpoint-management API and
> have not yet been exercised live (see docs/VERIFICATION.md).

## Setup & diagnostics

```bash
endpoint-aiops init                      # interactive onboarding wizard
endpoint-aiops doctor [--skip-auth]      # config + secret store + connectivity (/version)
endpoint-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.endpoint-aiops/secrets.enc)

```bash
endpoint-aiops secret set <target> [--value <key>]   # store API key (hidden prompt if no --value)
endpoint-aiops secret list                            # names only — values never shown
endpoint-aiops secret rm <target>
endpoint-aiops secret migrate                         # import legacy plaintext .env (ENDPOINT_<T>_APIKEY)
endpoint-aiops secret rotate-password                 # re-encrypt under a new master password
```

## Read commands

```bash
endpoint-aiops overview [--target <t>]        # online/offline, stale endpoints, agent/patch spread
endpoint-aiops endpoint list                  # all managed endpoints
endpoint-aiops endpoint get <endpoint_id>     # one endpoint detail
endpoint-aiops session list [--since-hours 24]           # recent login/boot sessions
endpoint-aiops session storm [--since-hours 24] [--window-s 300] [--min-concurrent 10]
endpoint-aiops drift report                   # endpoints drifted from the fleet-majority baseline
endpoint-aiops drift patch [--target-patch <level>]      # patch-level distribution + who's behind
```

## Write commands (governed; risk tier in parentheses)

```bash
endpoint-aiops endpoint assign-profile <endpoint_id> <profile_id> [--dry-run]   # (high) reversible; double confirm
endpoint-aiops endpoint reboot <endpoint_id> [--dry-run]                        # (medium) no undo; double confirm
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target)
- `--dry-run` — print the API call that would be made, change nothing
- State-changing commands (`endpoint assign-profile`, `endpoint reboot`) require two confirmations
