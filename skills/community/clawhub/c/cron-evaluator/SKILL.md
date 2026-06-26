---
name: cron-evaluator
description: |
  Cron Evaluator — Analyzes and scores cron jobs on a system for health, resource usage,
  collision risk, and resilience. Provides actionable suggestions for improvement.
  Use when: (1) auditing cron jobs, (2) detecting timing collisions, (3) optimizing cron performance,
  (4) planning systemd migration.
triggers:
  - "cron evaluation"
  - "cron audit"
  - "cron health"
  - "collision detection"
  - "cron optimization"
  - "systemd migration"
author: "Axioma Cluster"
date: "2026-05-17"
version: 1.0.0
tags:
  - cron
  - evaluation
  - system-administration
  - performance
  - systemd
  - scheduling
status: "active"
---

# Cron Evaluator

Evaluates cron job health across 4 pillars: Temporal, Resource, Resilience, and Pertinence.

## 4 Pillars

| Pillar | Checks | Score Range |
|--------|--------|-------------|
| **Temporal** | Midnight collision, frequency, jitter | 0-1 |
| **Resource** | Heavy commands (torch, docker, ollama) | 0-1 |
| **Resilience** | Logging, flock, timeout, error handling | 0-1 |
| **Pertinence** | Cron vs systemd timer recommendation | 0-1 |

## Usage

```bash
# Scan all cron jobs
python3 cron_evaluator_v3.py --scan

# Run health check
python3 cron_evaluator_v3.py --health

# Get improvement suggestions
python3 cron_evaluator_v3.py --suggest
```

## Health Thresholds

| Score | Status |
|-------|--------|
| >80% | 🟢 HEALTHY |
| 60-80% | 🟡 NEEDS_WORK |
| <60% | 🔴 CRITICAL |

## Key Checks

### Temporal Collision Detection
```python
# Two crons at 00:00 → suggest jitter
if cron1['time'] == '0 0 * * *' and cron2['time'] == '0 0 * * *':
    suggest("Add jitter: sleep $((RANDOM % 60))")
```

### Resource Signatures
```python
HEAVY_COMMANDS = ['torch', 'tensorflow', 'ollama', 'docker']
if any(h in command for h in HEAVY_COMMANDS):
    score -= 0.3  # Heavy resource consumer
```

### Resilience Verification
```python
CHECKS = {
    'logging': '>> /var/log/...' in command or '2>' in command,
    'flock': 'flock' in command,
    'timeout': 'timeout' in command,
    'error_handling': '||' in command
}
```

## Jitter Implementation

```bash
# BEFORE (collision risk)
0 2 * * * /path/to/script.sh

# AFTER (staggered with jitter)
0 2 * * * sleep $((RANDOM % 60)) && /path/to/script.sh
```

## Wrapper for Observability

```bash
# Wrapper that logs time/exit/memory
0 2 * * * /usr/bin/python3 /opt/evaluator/wrapper.py --task "TaskName" --cmd "/path/to/script.sh"
```

## Files

```
cron-evaluator/
├── SKILL.md                   # This file
├── scripts/
│   ├── cron_evaluator.py      # v1 (basic)
│   ├── cron_evaluator_v2.py   # v2 (enhanced)
│   ├── cron_evaluator_v3.py   # v3 (with KAN)
│   └── train_cron_kan.py     # KAN training script
├── data/
│   └── cron_training.json     # Training dataset
└── models/
    └── cron_kan.pt           # Trained KAN model
```

## KAN Model

The Cron KAN (16→32→16→8→4→3) predicts cron job quality from 16 features extracted from schedule and command patterns.