# Setup

## Required environment variables

- `FOFA_EMAIL`
- `FOFA_API_KEY`

## Optional environment variables

- `FOFA_BASE_URL`
  Default: `https://fofa.info`
- `FOFA_TIMEOUT`
  Default: `60`
- `FOFAMAP_MEMORY_DIR`
  Default: `results/fofamap_memory`
- `FOFAMAP_DISABLE_LEARNING`
  Default: unset

## Basic checks

```bash
export FOFA_EMAIL="you@example.com"
export FOFA_API_KEY="your_fofa_key"
python3 scripts/fofa_recon.py login
```

`login` returns both raw account data and a normalized `permission_profile`, including:

- `vip_level`
- `can_use_host_api`
- `can_use_stats_api`
- `allowed_search_fields`
- `default_search_fields_csv`
- `search_field_presets`

## Common commands

```bash
python3 scripts/fofa_recon.py search --query 'app="nginx" && country="US"'
python3 scripts/fofa_recon.py search --query 'app="nginx" && country="US"' --alive-check --output nginx_us.xlsx
python3 scripts/fofa_recon.py search-next --query 'title="login"' --fields host,ip,port,title --max-pages 3
python3 scripts/fofa_recon.py search-next --query 'body="admin"' --size 800 --max-pages 2
python3 scripts/fofa_recon.py search --query 'body="login"' --fields host,ip,port,title,server
python3 scripts/fofa_recon.py search --query 'cert.subject.org="Google"' --fields ip,port,product,product.version,cert.is_valid
python3 scripts/fofa_recon.py search --query 'asn="45102" && body="login"' --report-output infra_report.md --report-profile attack-infrastructure
python3 scripts/fofa_recon.py host --target 1.1.1.1
python3 scripts/fofa_recon.py host --target 1.1.1.1 --report-output host_report.md --report-profile abnormal-exposure
python3 scripts/fofa_recon.py stats --query 'app="Redis"' --fields country,port,org
python3 scripts/fofa_recon.py stats --query 'app="Redis"' --fields country,port,org --report-output stats_report.md --report-profile abnormal-exposure
python3 scripts/fofa_recon.py alive-check --target example.com --target 1.1.1.1:8443 --output alive.csv
python3 scripts/fofa_recon.py monitor-run --query 'org="Example Corp"' --state-dir results/monitor_example --report-output results/monitor_example/latest_report.md --report-profile abnormal-exposure
python3 scripts/fofa_recon.py monitor-run --query-file queries.txt --use-search-next --max-pages 3 --state-dir results/monitor_monthly --fail-on-change
python3 scripts/fofa_recon.py project-run --query 'app="nginx" && country="US"' --query 'app="grafana" && country="US"' --alive-check --split-exports --report-profile abnormal-exposure
python3 scripts/fofa_recon.py project-run --query-file queries.txt --alive-check --run-nuclei
python3 scripts/fofa_recon.py learn-review --output evolution_review.md
python3 scripts/fofa_recon.py icon-hash --url https://example.com
```

## Notes

- The helper prints JSON so it can be consumed directly by an agent.
- FOFA account tier affects which response fields are allowed and whether `host` or `stats` APIs are available.
- For tier-sensitive work, call `login` first and inspect `permission_profile`.
- `search` returns `field_resolution`, including `dropped_fields` when a requested field is above the current FOFA tier.
- `search-next` follows FOFA's continuous paging API and accepts `--next-cursor id` as a compatibility sentinel, but the helper prefers omitting `next` on the first request.
- `search-next` reports `requested_size`, `effective_size`, and `size_limit_reasons` when FOFA's documented `body` or `cert/banner` caps force the page size down.
- Search retries should broaden query logic before increasing result volume.
- Treat FOFA results as indexed intelligence, not live confirmation.
- `search --alive-check` adds live web reachability to the result set and can export that handoff directly.
- `--report-profile` is available on `search`, `search-next`, `project-run`, `monitor-run`, `host`, and `stats`.
- Use `attack-infrastructure`, `abnormal-exposure`, or `takeover-risk` when the user wants a stronger narrative than the standard delivery report.
- The helper keeps local memory by default in `results/fofamap_memory`, including `runs.jsonl`, `semantic-patterns.json`, and `latest_reflection.md`.
- Set `FOFAMAP_DISABLE_LEARNING=1` if you need a no-memory run.
- Use `learn-review` to turn accumulated episodes into a readable evolution summary.
- `monitor-run` is designed for daily, weekly, or monthly automation. The first run creates a baseline; later runs compare against `latest_snapshot.json` and write `latest_diff.json` and `latest_report.md`.
- Keep `--state-dir` stable for recurring monitoring jobs so the same asset set is compared over time.
- `--output` supports `csv` and `xlsx`.
- `project-run` creates a project directory with merged exports, per-query exports when requested, `targets.txt`, a Markdown report, and a suggested Nuclei command.
- `host --report-output` and `stats --report-output` generate analyst-friendly Markdown deliverables.
- `project-run --run-nuclei` and `nuclei-run` should only be used on authorized targets.
