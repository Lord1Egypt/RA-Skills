# Changelog

## 1.0.0 - 2026-11-25

- Initial release: ASPL v0.1 reference engine (portable, env-configured)
- `--init` starter policy bootstrap
- Evaluate CLI: budgets, merchant allowlists (pinned + Trust Rank floor),
  approval thresholds, rail permissions
- Human approval flow (`--approve <eventHash> --approver`)
- Local hash-chained audit trail (~/.paycensus-gate/audit.jsonl), nothing uploaded
- Trust Rank data cached hourly from the public census (keyless)
