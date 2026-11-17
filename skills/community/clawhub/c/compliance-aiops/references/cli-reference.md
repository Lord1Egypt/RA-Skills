# compliance-aiops CLI reference

> Evidence, not certification. Reads the local audit trails governed
> AIops tools write (`~/.*-aiops/audit.db`) read-only. No external API, no
> network, no platform credentials. The CLI is a convenience subset; the full
> 19-tool surface is available over MCP.

## Setup & diagnostics

```bash
compliance-aiops init                      # discover sibling audit DBs, set org name, optional signing key
compliance-aiops doctor                    # which sibling audit DBs are present/readable
compliance-aiops overview                  # audit sources + per-framework covered/total counts
compliance-aiops mcp                        # start the MCP server (stdio transport)
```

## Reports (read-only)

```bash
compliance-aiops report sources                    # discovered audit sources + row counts
compliance-aiops report coverage <framework>       # per-control coverage (hipaa|pci_dss|soc2|gdpr)
compliance-aiops report gaps <framework>           # controls with no/weak evidence + honest caveat
compliance-aiops report approvals                  # high-risk write ops + approver + rationale
compliance-aiops report exceptions                 # denied / error / budget_exceeded ops
```

## Bundles (evidence artifacts)

```bash
compliance-aiops bundle generate <framework> [--since <iso>] [--until <iso>] [--period <7d|24h|2w|last-7-days>] [--sign]
                                                   # hash-chain-sealed bundle → ~/.compliance-aiops/bundles/
compliance-aiops bundle verify <path>              # re-verify chain + seal head (+ signature)
compliance-aiops bundle list                       # list generated bundles
compliance-aiops bundle export <path> --format <markdown|csv|json>
compliance-aiops bundle schedule <framework> [--cron "0 2 * * 1"] [--period 7d] [--sign]
                                                   # print a ready-to-paste cron line; WRITES NOTHING, no daemon
```

## Secrets (optional bundle-signing key, encrypted ~/.compliance-aiops/secrets.enc)

Only needed if you sign bundles; there are no platform credentials.

```bash
compliance-aiops secret set <name> [--value <key>]   # store signing key (hidden prompt if no --value)
compliance-aiops secret list                          # names only — values never shown
compliance-aiops secret rm <name>
compliance-aiops secret migrate                       # import a legacy plaintext key
compliance-aiops secret rotate-password               # re-encrypt under a new master password
```

## Notes

- `<framework>` is one of `hipaa`, `pci_dss`, `soc2`, `gdpr`, `iso27001`, `djcp_l3`.
- `--since` / `--until` bound the evidence period (ISO-8601). The hash chain is
  over evidence records only, so the same `(framework, period, sources)`
  reproduces the same `chainHead`.
- `--period` is a convenience relative window (`7d` / `24h` / `2w` /
  `last-7-days`) resolved to a since/until pair ending "now"; used only when
  `--since` / `--until` are not given. `bundle schedule` prints a cron line for
  running that periodically — it starts no daemon and writes nothing.
- `--sign` requires a stored signing key; unlock non-interactively by exporting
  `COMPLIANCE_AIOPS_MASTER_PASSWORD`.
- Bundles are the only files written (under `~/.compliance-aiops/bundles/`); the
  source audit DBs are opened read-only.
