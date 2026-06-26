# Monitor Playbook

## When to use it

Use `monitor-run` when the user wants recurring asset watch instead of a one-off search.

Typical asks:

- daily or monthly monitoring for a known organization or product set
- alert on newly exposed or missing assets
- keep a professional Markdown report after each run
- preserve snapshot history for later review

## Core model

`monitor-run` is designed to be scheduler-friendly.

- first run: establish baseline
- later runs: compare against `latest_snapshot.json`
- outputs: `latest_snapshot.json`, `latest_diff.json`, `latest_report.md`, timestamped archives, optional current exports

The skill itself handles the monitoring logic. Scheduling can be done by OpenClaw automations or any external scheduler, but the command should always use a stable `--state-dir`.

## Recommended patterns

### Small recurring watch

```bash
python3 scripts/fofa_recon.py monitor-run \
  --query 'org="Example Corp"' \
  --state-dir results/monitor_example \
  --report-output results/monitor_example/latest_report.md
```

### Larger recurring watch

```bash
python3 scripts/fofa_recon.py monitor-run \
  --query-file queries.txt \
  --use-search-next \
  --max-pages 3 \
  --state-dir results/monitor_monthly \
  --fail-on-change
```

### Higher-confidence operational watch

```bash
python3 scripts/fofa_recon.py monitor-run \
  --query 'app="nginx" && country="US"' \
  --alive-check \
  --split-exports \
  --suggest-nuclei \
  --state-dir results/monitor_nginx
```

## Operating rules

- Keep `--state-dir` stable across runs.
- Prefer `--use-search-next` when the result set is large or the user explicitly wants continuous paging.
- Use `--fail-on-change` when the caller should treat asset drift as an alert condition.
- Use `--alive-check` when live reachability changes the user's decision.
- Use `--split-exports` when different teams or queries need separate handoff files.

## Report expectations

A good monitoring report should answer:

- Did the asset set grow, shrink, or stay stable?
- Which queries changed?
- Which new assets are worth reviewing first?
- Are any new assets on high-signal ports?
- Are there changes in HTTP status, title, server, or stack hints?

The generated report already includes:

- executive judgment
- per-query drift summary
- newly observed assets
- removed or missing assets
- changed existing assets
- current exposure snapshot
- recommended actions
- output file inventory

## Alert interpretation

- `alert_level: none`: no drift, or first run establishing a baseline
- `alert_level: low`: asset metadata changed, but inventory count stayed stable
- `alert_level: medium`: assets were added or removed
- `alert_level: high`: new assets appeared on ports that usually deserve faster review

## Practical advice for the agent

- Do not treat the first baseline run as an incident.
- If assets disappear, mention the chance of FOFA indexing delay before calling it decommissioning.
- If new assets appear on `22`, `3389`, `445`, `6379`, `7001`, `8080`, `8443`, `9200`, or `27017`, raise the priority in the summary.
- If the user wants a persuasive report, keep the main judgment short and then support it with concrete evidence from the diff.
