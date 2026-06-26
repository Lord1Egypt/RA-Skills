---
name: system-health
description: System health monitoring and reports
---

# system-health

Monitor system health: CPU, memory, disk, processes, and network. Generate health reports.

## Usage

```bash
# Quick health check
python3 scripts/syshealth.py check

# Generate a full report
python3 scripts/syshealth.py report

# Continuous monitoring
python3 scripts/syshealth.py monitor --interval 60

# Specific checks
python3 scripts/syshealth.py check --category disk
```

## Commands

- `check` — Run a quick health check
- `report` — Generate a detailed system report
- `monitor` — Continuous monitoring with periodic checks

## Options

- `--category` — Check specific category: `cpu`, `memory`, `disk`, `network`, `processes`
- `--interval` — Monitoring interval in seconds (default: 60)
- `--output, -o` — Write report to file
- `--threshold` — Alert threshold percentage for disk/memory (default: 80)
