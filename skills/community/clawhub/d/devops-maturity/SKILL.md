---
name: devops-maturity
description: Assess DevOps maturity level in organizations, especially cloud-native or cloud-migrating companies. Use when someone asks about DevOps assessment, maturity audit, DevOps evaluation, CI/CD maturity, infrastructure automation assessment, DORA metrics evaluation, cloud operations readiness, SRE maturity, or wants to benchmark their DevOps practices. Also use for FinOps readiness checks, IaC maturity reviews, or organizational DevOps transformation planning.
---

# DevOps Maturity Assessment

Interactive assessment of an organization's DevOps maturity across 7 dimensions, producing a scored report with actionable recommendations.

## Assessment Workflow

1. Introduce the assessment — explain it takes ~10 minutes, covers 7 dimensions
2. Ask questions dimension by dimension — 3-4 questions per dimension
3. Score each dimension 0-6 based on the maturity model
4. Generate the final report with scores, visualization, and recommendations
5. Offer to deep-dive into any weak dimension

## Maturity Model (7 levels)

| Level | Name | Key Indicator |
|-------|------|---------------|
| 0 | Legacy | No cloud, no automation |
| 1 | Ad Hoc | First experiments, no strategy |
| 2 | Opportunistic | Point successes, inconsistent approaches |
| 3 | Systematic | Documented processes, org-wide acceptance |
| 4 | Measured | KPIs defined, data-driven management |
| 5 | Optimized | Continuous improvement from collected data |
| 6 | Advanced Cloud | Full cloud, proactive optimization |

## 7 Assessment Dimensions

For detailed questions and scoring criteria per dimension, read `references/dimensions.md`.

**Quick overview:**

1. **CI/CD & Deployment** — frequency, lead time, pipeline automation
2. **Infrastructure as Code** — IaC coverage, testing, drift detection
3. **Observability** — monitoring, logging, tracing, SLO/SLI
4. **Security (DevSecOps)** — shift-left, scanning, secrets management
5. **Culture & Organization** — Dev+Ops collaboration, blameless postmortems
6. **FinOps** — cost visibility, optimization, per-team budgeting
7. **Reliability (SRE)** — MTTR, change failure rate, auto-remediation

## Scoring Rules

- Score each dimension independently (0-6)
- Overall score = floor of weighted average (CI/CD and Reliability weighted 1.5x)
- Map overall score to maturity level name
- Flag any dimension scoring 2+ levels below overall as "critical gap"

## Report Format

Generate a report like this:

```
══════════════════════════════════════════
   DevOps Maturity Assessment Report
   Organization: [name]
   Date: [date]
══════════════════════════════════════════

   Overall Level: [X] — [Level Name]

   CI/CD & Deployment:    [bar] X/6
   Infrastructure as Code:[bar] X/6
   Observability:         [bar] X/6
   Security (DevSecOps):  [bar] X/6
   Culture & Organization:[bar] X/6
   FinOps:                [bar] X/6
   Reliability (SRE):     [bar] X/6

──────────────────────────────────────────
   Strengths:
   • [top 2-3 strong areas with specifics]

   Critical Gaps:
   • [dimensions 2+ levels below average]

   Top 3 Recommendations:
   1. [specific, actionable recommendation]
   2. [specific, actionable recommendation]
   3. [specific, actionable recommendation]

   Benchmark: Your org scores in the
   [top/middle/bottom] third of assessed
   organizations.
══════════════════════════════════════════
```

Use bar characters: ████░░ for visual scoring.

## After the Report

- Offer to deep-dive into the weakest dimension
- Suggest a re-assessment timeline (quarterly recommended)
- For recommendations, reference DORA State of DevOps findings when relevant
