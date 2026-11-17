---
name: codebase-inspection
version: 2.0.0
description: Advanced codebase analysis with HTML reports, git-aware diffs, trend tracking, SVG badges, CSV export, and CI/CD integration
tags: ["codebase", "analysis", "metrics", "devtools", "python", "cli", "ci", "reports", "open-source", "agent", "automation", "MIT"]
---

# Codebase Inspector

**Walk any directory and report language breakdowns, line counts, blank/comment lines, with HTML reports, git-aware diffs, trend tracking, SVG badges, CSV export, and CI integration.**

> *Keywords: codebase, analysis, metrics, devtools, python, cli, ci, reports, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

You can't manage codebase metrics you can't measure — and you can't see trends over time. Codebase Inspector solves this: Walk any directory and report language breakdowns, line counts, blank/comment lines, with HTML reports, git-aware diffs, trend tracking, SVG badges, CSV export, and CI integration.

**Best for:** Engineering leads, open-source maintainers, and CI pipelines.

## Features

- **Print a per-language LOC report**
- **Export CSV for dashboards**
- **Generate an HTML report**
- **Git-aware diff between snapshots**
- **Track trends and emit an SVG badge**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/codebase-inspection/main/codebase_inspector.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python codebase_inspector.py --help        # list options
```

## Use cases

1. Print a per-language LOC report
1. Export CSV for dashboards
1. Generate an HTML report
1. Git-aware diff between snapshots
1. Track trends and emit an SVG badge

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| tokei/scc | Adds git-aware diffs, trend tracking, HTML reports, and badges in one CLI. |
| Manual wc -l | Per-language breakdown with comment/blank counts. |
| Spreadsheet metrics | CSV + HTML + badge, CI-ready. |

## FAQ (SEO / AEO)

**Q: How many languages?**  
A: 25+ extensions recognized out of the box.

**Q: CI integration?**  
A: Yes — example GitHub Actions workflow asserts a language ratio.

**Q: Badges?**  
A: --badge emits an SVG you can drop in a README.

**Q: Offline?**  
A: Yes — no network, no telemetry.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test codebase-inspection
        run: python codebase_inspector.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/codebase-inspection)
