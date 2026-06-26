---
name: fofamap
description: Use this skill when the user wants FOFA-based asset discovery, host profiling, distribution statistics, icon_hash generation, query refinement after zero-result searches, or cautious follow-up vulnerability triage. It is for security recon tasks that need deterministic FOFA API calls instead of an interactive CLI.
homepage: https://github.com/asaotomo/FofaMap
license: MIT
metadata: {"short-description":"FOFA recon, monitoring, live checks, asset handoff, and local self-improvement","clawdbot":{"emoji":"🗺️","primaryEnv":"FOFA_API_KEY","requires":{"env":["FOFA_EMAIL","FOFA_API_KEY"],"bins":["python3"]},"files":["scripts/fofa_recon.py","references/setup.md","references/query-playbook.md","references/analysis-playbook.md","references/permission-playbook.md","references/monitor-playbook.md","references/redteam-hunt-playbook.md","references/report-templates.md","references/evolution-playbook.md","references/syntax-arsenal.md","references/syntax-corpus.tsv"]}}
---

# fofamap

## Overview

This skill turns natural-language recon requests into a stable FOFA workflow:

1. pick the right FOFA operation,
2. detect the FOFA membership tier and capability profile,
3. run deterministic API calls through `scripts/fofa_recon.py`,
4. broaden the search when FOFA returns no useful data,
5. verify live web reachability when it matters,
6. track inventory drift with snapshot comparisons when the task is recurring,
7. export clean handoff files when the user needs deliverables,
8. summarize findings with clear caveats and next steps,
9. learn from prior runs so the next query, report, and handoff improve.

This skill is distilled from the FofaMap project, but packaged for skill use instead of an interactive application. The host agent should do the reasoning, and the helper script should do the FOFA API work. The workflow keeps the project's key tactics: action routing, permission-aware field selection, zero-result reflection, live reachability verification, export-oriented delivery, and targeted follow-up suggestions. It now also keeps a bounded local memory so the skill can reflect on failed runs, recurring friction, and strong report patterns without turning into an uncontrolled self-modifying black box.

For setup, the user only needs to provide FOFA credentials:

- `FOFA_EMAIL`
- `FOFA_API_KEY`

## When To Use

Use this skill when the user asks for any of the following:

- find exposed assets, subdomains, services, or product fingerprints with FOFA
- profile a single IP or domain with FOFA host aggregation
- analyze distribution data such as country, port, title, ASN, or organization rankings
- run recurring asset monitoring and compare new, removed, or changed exposures
- derive an `icon_hash` query from a target website
- retry a failed FOFA search with broader, smarter fallback queries
- decide whether the findings justify a separate validation step such as `nuclei`

Do not use this skill for:

- general web scraping unrelated to FOFA
- active exploitation by default
- network scanning without explicit user approval
- tasks that require guaranteed real-time validation beyond FOFA's indexed data

## Quick Start

If credentials are not configured yet, read [references/setup.md](references/setup.md).

Required credentials for this skill:

- FOFA email
- FOFA API key

Core helper:

- `scripts/fofa_recon.py login`
- `scripts/fofa_recon.py search --query 'app="nginx" && country="US"'`
- `scripts/fofa_recon.py search --query 'app="nginx" && country="US"' --alive-check --output nginx_us.xlsx`
- `scripts/fofa_recon.py search-next --query 'title="login"' --fields host,ip,port,title --max-pages 3`
- `scripts/fofa_recon.py search-next --query 'app="nginx"' --size 100 --max-pages 2 --output nginx_deep.xlsx`
- `scripts/fofa_recon.py search --query 'cert.subject.org="Google"' --fields ip,port,product,product.version,cert.is_valid`
- `scripts/fofa_recon.py host --target 8.8.8.8`
- `scripts/fofa_recon.py host --target 8.8.8.8 --report-output host_report.md`
- `scripts/fofa_recon.py stats --query 'app="Redis"' --fields country,port,org`
- `scripts/fofa_recon.py stats --query 'app="Redis"' --fields country,port,org --report-output stats_report.md`
- `scripts/fofa_recon.py alive-check --target example.com --target 1.1.1.1:8443 --output alive.csv`
- `scripts/fofa_recon.py monitor-run --query 'org="Example Corp"' --state-dir results/monitor_example --report-output results/monitor_example/latest_report.md`
- `scripts/fofa_recon.py monitor-run --query-file queries.txt --use-search-next --max-pages 3 --state-dir results/monitor_monthly --fail-on-change`
- `scripts/fofa_recon.py project-run --query 'app="nginx" && country="US"' --query 'app="grafana" && country="US"' --alive-check --split-exports`
- `scripts/fofa_recon.py learn-review`
- `scripts/fofa_recon.py icon-hash --url https://example.com`

## Workflow

### 1. Choose the correct mode

- Use `search` when the user wants concrete assets.
- Use `search-next` when the user wants deeper harvesting through FOFA's official continuous paging cursor API.
- Use `host` when the user gives one IP or one domain and wants details.
- Use `stats` when the user wants rankings, trends, or distribution.
- Use `icon-hash` when the user wants similar assets by favicon.
- Use `monitor-run` when the same queries will be rerun on a schedule and the user cares about newly added, removed, or changed assets.

`host` returns a normalized `host_profile` when FOFA exposes richer host data such as domains, protocols, ISP, rules, or per-port rule hints.

`stats` returns a normalized `stats_summary` with `consumed_fpoint`, `required_fpoints`, and `lastupdatetime` when FOFA includes them.

### 2. Read the FOFA capability profile first when permissions matter

Run `scripts/fofa_recon.py login` before planning when the user needs:

- `host` or `stats` and you are not sure the account supports those APIs
- advanced export fields such as `product`, `body`, `product.version`, `cert.is_valid`, or `icon`
- a field-heavy handoff where you need to know what FOFA will actually return

The helper returns a `permission_profile` object with:

- `vip_level` and human-readable tier name
- `can_use_host_api` and `can_use_stats_api`
- `allowed_search_fields`
- `documented_search_export_field_count`
- `data_limit`
- `default_search_fields_csv`
- `search_field_presets`

Use that profile to choose fields before issuing the search.

### 3. Start conservative

Default to safe, broadly available fields unless the user explicitly needs premium FOFA fields. The helper script already falls back to a safe field set if a higher-tier field request is rejected.

Before using advanced fields or highly specific filters, check [references/query-playbook.md](references/query-playbook.md), [references/permission-playbook.md](references/permission-playbook.md), and [references/syntax-arsenal.md](references/syntax-arsenal.md).

When the user intent is fuzzy, exploratory, or hunt-style, search [references/syntax-corpus.tsv](references/syntax-corpus.tsv) by product, tag, rule name, or artifact string and use it to generate one precise query plus one or two controlled fallback queries. Treat the corpus as a seed library, not a hard limit on what FOFA combinations are allowed.

If the task is attack-infrastructure hunting, takeover review, honeypot suspicion, or cloud/API leak discovery, also load [references/redteam-hunt-playbook.md](references/redteam-hunt-playbook.md).

If the user wants a polished report, persuasive delivery, or a specific analyst angle, also load [references/report-templates.md](references/report-templates.md) and choose a suitable `--report-profile` such as `attack-infrastructure`, `abnormal-exposure`, or `takeover-risk`.

If the task is recurring, long-running, or the user explicitly wants the skill to improve from experience, also load [references/evolution-playbook.md](references/evolution-playbook.md). The helper writes local episodic and semantic memory under `results/fofamap_memory/` by default and exposes `learning_artifacts` plus `learn-review`.

When the user wants more than one ordinary page of results, prefer `search-next` over repeatedly emulating page numbers. It follows FOFA's official `/api/v1/search/next` cursor flow and returns `next_cursor_to_resume`, `has_more`, `requested_size`, `effective_size`, and `cursor_trace` so later runs can resume cleanly and explain any FOFA size cap that was applied.

### 4. If the result set is empty, reflect and retry

Do up to three progressively broader retries:

1. remove the most brittle geographic or version-specific filter
2. replace `host=` with broader `title=`, `body=`, or product-style matching when appropriate
3. keep only the most distinctive keyword plus a coarse scope such as country or protocol

State clearly that the later attempts are broader fallback queries, not equivalent matches.

### 5. Summarize like an analyst

When reporting results, include:

- the user goal in one line
- the FOFA query or queries used
- the scope and major findings
- any important field or subscription limitations
- a cautious next-step recommendation

When the report needs to feel complete and operator-ready, choose a report profile instead of writing in a generic voice. Use:

- `standard` for baseline delivery
- `attack-infrastructure` for clustering, campaign-style, or suspicious infra review
- `abnormal-exposure` for admin panels, storage leakage, API exposure, and unusual services
- `takeover-risk` for dangling domains, placeholder pages, and ownership gaps

### 6. Add live verification when it changes the answer

Use `--alive-check` or `alive-check` when the user wants:

- a current reachable subset of FOFA results
- dead assets filtered out before handoff
- a cleaner candidate list for later validation work

If the user asks for a deliverable, prefer exporting the checked result set so the handoff includes the current HTTP status.

### 7. Export for handoff, not just for storage

Use:

- `xlsx` when handing off to analysts, red teams, or non-technical stakeholders
- `csv` when another tool or script will consume the result

If live checks were run, include the HTTP status in the export. This preserves one of the most practical parts of the original project: not just finding assets, but packaging them for the next operator.

### 8. Gate active follow-up

If the user wants active validation, ask or confirm before running tools such as `nuclei`, curl-based checks, or login probes. FOFA is passive indexed intelligence; active testing is a separate consent boundary.

### 9. Prefer project mode for real jobs

When the user has multiple queries, wants delivery files, or needs a mini operation bundle, prefer `project-run`. It preserves one of the original project's best ideas: a single task should leave behind a project directory with exports, `targets.txt`, a suggested Nuclei command, and a Markdown report.

If the user explicitly wants active scanning and has authorization, `project-run --run-nuclei` can extend that workflow into a local Nuclei scan and fold the log summary into the report.

### 10. Use monitor mode for recurring asset watch

Use `monitor-run` when the user asks for daily, weekly, or monthly asset tracking.

- The first run establishes a baseline snapshot.
- Later runs compare against `latest_snapshot.json` and report added, removed, and changed assets.
- Prefer a stable `--state-dir` so scheduled runs always compare against the same monitoring profile.
- Add `--use-search-next` for larger inventories and `--fail-on-change` when an automation should raise an alert on drift.
- The command leaves behind `latest_snapshot.json`, `latest_diff.json`, `latest_report.md`, timestamped archives, and optional per-query exports.

## Working Rules

- Prefer the helper script over ad hoc HTTP code so the workflow stays consistent.
- Keep output compact and analyst-friendly. Raw JSON is fine when another tool will consume it; otherwise summarize it.
- Call out when FOFA data may be stale, partial, or permission-limited.
- If the user asks for premium-only fields, inspect `permission_profile` first. The helper script will also drop known over-tier fields before the request and report that downgrade explicitly.
- For high-risk follow-up suggestions, separate "observed from FOFA" from "needs live validation."
- When the task is analytical rather than mechanical, use the reporting patterns in [references/analysis-playbook.md](references/analysis-playbook.md).
- When the task needs an operator handoff, create files, not just chat output.
- When local memory exists, read the latest reflection before repeating a similar task so the agent actually benefits from prior runs.

## References

- [references/setup.md](references/setup.md): environment variables and command examples
- [references/query-playbook.md](references/query-playbook.md): query patterns, field guidance, retry heuristics, and triage suggestions
- [references/permission-playbook.md](references/permission-playbook.md): vip-level capability model, field presets, and tier-aware field matching
- [references/analysis-playbook.md](references/analysis-playbook.md): distilled tactics from the original AI and MCP workflows
- [references/monitor-playbook.md](references/monitor-playbook.md): recurring asset monitoring, drift analysis, baseline handling, and report strategy
- [references/redteam-hunt-playbook.md](references/redteam-hunt-playbook.md): attack infrastructure, deception, takeover, and cloud leak hunting tactics
- [references/report-templates.md](references/report-templates.md): fixed report lenses and persuasive delivery structure
- [references/evolution-playbook.md](references/evolution-playbook.md): local memory, self-reflection, self-repair, and learn-review workflow
- [references/syntax-arsenal.md](references/syntax-arsenal.md): how to use the team's FOFA syntax corpus for divergent query planning
- [references/syntax-corpus.tsv](references/syntax-corpus.tsv): extracted rule corpus from the workbook for grep-based query seeding
