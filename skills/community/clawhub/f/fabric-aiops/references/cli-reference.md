# fabric-aiops CLI reference

> Controller API paths (Meraki / Catalyst Center / CVP / UniFi Network) are
> modelled from the public API shapes and have not yet been exercised live
> (see docs/VERIFICATION.md). Not affiliated with Cisco/Meraki/Arista/Ubiquiti.

## Setup & diagnostics

```bash
fabric-aiops init                      # interactive onboarding wizard (platform: meraki/catalyst/cvp/unifi)
fabric-aiops doctor [--skip-auth]      # config + secret store + connectivity (canonical org/site/container probe)
fabric-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.fabric-aiops/secrets.enc)

```bash
fabric-aiops secret set <target> [--value <key>]   # store API key (hidden prompt if no --value)
fabric-aiops secret list                            # names only — values never shown
fabric-aiops secret rm <target>
fabric-aiops secret migrate                         # import legacy plaintext .env (FABRIC_<T>_APIKEY)
fabric-aiops secret rotate-password                 # re-encrypt under a new master password
```

## Read commands

```bash
fabric-aiops overview [--org-id <id>] [--target <t>]   # networks + device status/product rollup

fabric-aiops org list                                  # organizations visible to the key
fabric-aiops org get [--org-id <id>]
fabric-aiops org licensing [--org-id <id>]
fabric-aiops org admins [--org-id <id>]
fabric-aiops org device-statuses [--org-id <id>]       # online/offline/alerting rollup
fabric-aiops org api-usage [--org-id <id>]             # response-code counts, 429 rate-limits

fabric-aiops network list [--org-id <id>]
fabric-aiops network get <networkId>
fabric-aiops network vlans <networkId>
fabric-aiops network alerts <networkId>                # health alerts by severity
fabric-aiops network traffic <networkId> [--timespan 86400]

fabric-aiops device inventory [--model MS] [--org-id <id>]   # MX/MS/MR/MV/MG
fabric-aiops device status <serial> [--org-id <id>]
fabric-aiops device uplinks [--org-id <id>]
fabric-aiops device switch-ports <serial>              # MS ports
fabric-aiops device ssids <networkId>                  # MR SSIDs

fabric-aiops client list <networkId> [--timespan 86400]
fabric-aiops client get <networkId> <clientId>
fabric-aiops client usage <networkId> <clientId>
fabric-aiops client connectivity <networkId> <clientId>

fabric-aiops health uplink-rca [--loss-pct 5] [--latency-ms 150] [--org-id <id>]   # flagship RCA
fabric-aiops health score [--org-id <id>]              # composite per-network health from live data

# Cisco ACI targets (platform: aci) — read-only, ACI-native references
fabric-aiops aci trace --mac <mac> | --ip <ip> [--limit 5]   # endpoint → leaf/interface → EPG → BD → VRF → contracts
fabric-aiops aci segment <tenant> <app> <epg>                # an EPG's BD, VRF and contracts
fabric-aiops aci faults [--severity critical] [--include-cleared] [--limit 50]   # worst-first
```

## Write commands (governed; risk tier in parentheses)

```bash
fabric-aiops remediate reboot <serial> [--dry-run]                       # (high) no undo; double confirm
fabric-aiops remediate blink-leds <serial> [--duration 20]               # (low)  locator aid
fabric-aiops remediate update-device <serial> '{"name":"ap1"}' [--dry-run]   # (medium) captures before
fabric-aiops remediate update-vlan <networkId> <vlanId> '{"name":"data"}' [--dry-run]  # (medium)
fabric-aiops remediate claim <networkId> <serial...> [--dry-run]         # (high) inverse = remove
fabric-aiops remediate remove <networkId> <serial> [--dry-run]           # (high) inverse = claim back
fabric-aiops remediate bind <networkId> <templateId> [--auto-bind] [--dry-run]   # (high) captures prior binding
fabric-aiops remediate unbind <networkId> [--dry-run]                    # (high) captures prior template
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target)
- `--org-id, -o <id>` — Meraki organization id (omit to use the target's default `org_id`)
- `--dry-run` — print the API call that would be made, change nothing
- State-changing commands require two confirmations (except `blink-leds`, low risk)
