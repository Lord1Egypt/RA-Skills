# firewall-aiops CLI reference

> Covers OPNsense (REST `/api/...`) and pfSense (REST v2 `/api/v2/...`). Responses are
> validated against mocks; see `docs/VERIFICATION.md` for the live-run checklist.

## Setup & diagnostics

```bash
firewall-aiops init                      # interactive wizard (asks for the platform: opnsense/pfsense)
firewall-aiops doctor                    # check config, secrets, connectivity
                                         #   firmware/version query on both platforms
firewall-aiops doctor --skip-auth        # config/secret checks only (no network)
firewall-aiops mcp                       # start the MCP server (stdio)
```

## Secrets (encrypted store)

```bash
firewall-aiops secret set <target> [--value <secret>]  # store OPNsense secret / pfSense key (hidden prompt if no --value)
firewall-aiops secret list                             # list target names with a stored secret (values never shown)
firewall-aiops secret rm <target>                      # delete a stored secret
firewall-aiops secret migrate                          # import legacy plaintext .env into the encrypted store
firewall-aiops secret rotate-password                  # re-encrypt under a new master password
```

## Overview & rules

```bash
firewall-aiops overview                        # one-shot: version + gateway/interface health + rule count
firewall-aiops rules list [--interface wan]    # list filter rules (optionally on one interface)
firewall-aiops rules show <uuid>               # one rule's full detail
firewall-aiops rules toggle <uuid> --disable   # governed write: dry-run + double-confirm
firewall-aiops rules toggle <uuid> --enable --dry-run
```

## Firewall log

```bash
firewall-aiops log                             # recent firewall-log entries
firewall-aiops log --action block --limit 50   # only blocked traffic
```

## Notes

- `--target/-t` selects a named target from `config.yaml`; omit for the default (first).
- `overview`, `rules`, and `log` are the CLI subset; the full read surface (NAT,
  aliases, VPN, DHCP, diagnostics), the three flagship analyses, and the remaining
  governed writes (alias entry add/remove, kill_states, restart_service, apply_changes,
  reconfigure, reboot) are exposed through the MCP server (`firewall-aiops mcp`).
- High-risk writes (`apply_changes`, `reconfigure`, `reboot`) are labelled risk=high
  and audited. `FIREWALL_AUDIT_APPROVED_BY` (and `FIREWALL_AUDIT_RATIONALE`) are
  optional audit annotations, recorded when set but never required.
