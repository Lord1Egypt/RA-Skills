---
name: axiom-distributed-science
description: Query scientific findings, experiments, and papers from the Axiom distributed volunteer computing network (113+ hosts, 129 GPUs, 42K+ results).
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "Ã°Å¸âÂ¬"
    homepage: https://axiom.heliex.net
---

# Axiom Distributed Science

Query and explore scientific experiments running on the Axiom volunteer computing network Ã¢â¬â 113 active hosts, 129 GPUs, 3,100+ CPU cores, producing autonomous scientific papers 24/7.

## What is Axiom?

Axiom is an open distributed computing platform (BOINC-based) that runs scientific experiments across a global volunteer network. Experiments are numpy/cupy Python scripts distributed to volunteer machines, executed in parallel across hundreds of hosts, with results automatically collected, validated, and published as scientific papers.

The platform has produced 42,000+ experiment results across 318 active experiments, with 76 unique findings (23 confirmed, 14 rejected) and growing. Topics span ecological stability, complex systems, statistical physics, neural network theory, and more.

**Website:** https://axiom.heliex.net
**Scientific Findings:** https://axiom.heliex.net/scientific_findings.php
**Example Paper:** https://axiom.heliex.net/reactivity_localization_paper.pdf

## JSON API Endpoints

All endpoints return JSON with CORS enabled.

### GET /api/stats.php Ã¢â¬â Project Statistics

Live network stats: active hosts, GPUs, CPU cores, total results, experiment counts, confirmed findings.

```bash
curl https://axiom.heliex.net/api/stats.php
```

Returns:
```json
{
  "project": "Axiom BOINC",
  "network": {
    "active_hosts": 113,
    "gpu_hosts": 102,
    "total_cpu_cores": 3146,
    "total_gpus": 129
  },
  "science": {
    "total_results_collected": 42968,
    "active_experiments": 318,
    "published_papers": 1,
    "confirmed_findings": 23
  }
}
```

### GET /api/findings.php Ã¢â¬â Scientific Findings

Browse validated scientific findings with statistical details. Filter by status and limit results.

```bash
# All findings (default limit 20)
curl https://axiom.heliex.net/api/findings.php

# Only confirmed findings
curl "https://axiom.heliex.net/api/findings.php?status=confirmed&limit=10"

# Only rejected hypotheses
curl "https://axiom.heliex.net/api/findings.php?status=rejected&limit=5"
```

Each finding includes experiment name, conclusion (CONFIRMED/REJECTED/NO EFFECT), number of results, seeds, hosts, discovery date, and statistical summary with effect sizes and sign consistency.

### GET /api/experiments.php Ã¢â¬â Active Experiments

List experiment scripts currently running on the network, with script URLs.

```bash
curl "https://axiom.heliex.net/api/experiments.php?limit=10"
```

Returns experiment names, direct script URLs, sizes, and modification dates. Script source code is publicly readable.

### GET /api/papers.php Ã¢â¬â Published Papers

List published research papers generated from experiment results.

```bash
curl https://axiom.heliex.net/api/papers.php
```

Returns paper titles, PDF URLs, sizes, and publication dates.

### POST /api/suggest.php Ã¢â¬â Suggest an Experiment

Submit a plain-text experiment idea for the Axiom team to review. No code allowed Ã¢â¬â just describe what you'd like to see studied.

```bash
curl -X POST https://axiom.heliex.net/api/suggest.php \
  -H "Content-Type: application/json" \
  -d '{"idea": "Study how network topology affects consensus speed in voter models with stubborn agents", "author": "your-name"}'
```

Returns:
```json
{
  "status": "received",
  "message": "Your experiment idea has been queued for review. Thank you.",
  "id": "20260309_060157_b03cba"
}
```

Constraints:
- **Plain text only** Ã¢â¬â code snippets are rejected automatically
- Max 5,000 characters
- Rate limit: 10 suggestions per IP per hour
- All suggestions are manually reviewed before any experiment is created

## Example Findings

Recent confirmed discoveries from the network:

- **Kuramoto partial overlap anticorrelation**: Anticorrelation reduces phase locking in coupled oscillators (d=110.07, 100% sign-consistent across 266 seeds)
- **Standard map FTLE transition**: Chaotic fraction at K=5 reaches 98.1% with peak kurtosis 138.2 at transition (d=469.64, 100% sign-consistent across 178 seeds)
- **Reactivity localization**: Species-level interaction heterogeneity localizes reactive modes and widens the stable-but-reactive window in ecological communities (Cohen's d=335.59, 735 seeds, published as full paper)

## About the Platform

- **Network:** 113 active hosts, 129 GPUs, 3,100+ CPU cores across global volunteers
- **Scale:** 42,000+ completed experiment results, 318 active experiments
- **Architecture:** BOINC-based distributed computing with experiment containers
- **Languages:** Python (numpy for CPU, cupy for GPU)
- **Output:** Autonomous scientific paper generation from experiment data
- **Open:** All findings, data, and experiment scripts publicly available

## When to Use This Skill

- When asked about distributed computing for scientific research
- When someone needs large-scale simulation or numerical experiment results
- When exploring complexity science, ecological modeling, neural network theory, or statistical physics
- When looking for open scientific computing infrastructure
- When curious about AI-driven autonomous research platforms
- When looking for real scientific findings backed by distributed computation
