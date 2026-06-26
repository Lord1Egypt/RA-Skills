# EKS Workload Best Practice Assessment Skill - Design Document

**Status**: Approved
**Date**: 2026-03-26
**Author**: AI Assistant + panlm

## Overview

Create a new skill `eks-workload-best-practice-assessment` that fills the workload-level
assessment gap explicitly identified in `aws-best-practice-research`. This skill focuses
on Kubernetes workload configurations that require `kubectl` and `awscli` access to evaluate,
complementing the existing infrastructure-layer assessment.

## Design Decisions

### Approach: Single comprehensive skill (Option A)

Selected over two-phase split (Option B) and per-dimension split (Option C) because:
- Consistent with existing `aws-best-practice-research` style
- Single invocation for users
- Research and assessment are two phases of one workflow, splitting adds friction

### Data Sources

- **context7 MCP** (`/websites/kubernetes_io`) — K8s official documentation
- **aws-knowledge-mcp-server** — EKS Best Practices Guide, AWS prescriptive guidance
- All queries executed **sequentially** to avoid rate limiting

### Check Item Model: Dynamic Research + Version-Aware + Baseline Framework

- **Dynamic**: Each execution queries context7 + aws-knowledge-mcp for latest best practices
- **Version-aware**: Detects K8s/EKS version, filters inapplicable checks (e.g., PSA for 1.25+, PSP for <1.25)
- **Baseline framework**: `check-dimensions.md` defines 8 dimensions with minimum check sets as fallback

### Relationship with Existing Skills

- Can invoke `aws-best-practice-research` for infrastructure-layer assessment
- Results merged into unified report with combined scorecard
- No overlap — this skill handles kubectl-required checks only

## 8 Assessment Dimensions

| # | Dimension | Prefix | Est. Items | Tools |
|---|-----------|--------|------------|-------|
| 1 | Workload Configuration | WL- | 12-15 | kubectl |
| 2 | Security | SEC- | 15-18 | kubectl, aws iam |
| 3 | Observability | OBS- | 8-10 | kubectl, aws cloudwatch |
| 4 | Networking | NET- | 10-12 | kubectl |
| 5 | Storage | STR- | 6-8 | kubectl, aws ec2 |
| 6 | EKS Platform Integration | EKS- | 8-10 | awscli, kubectl |
| 7 | CI/CD & GitOps | CICD- | 5-7 | kubectl |
| 8 | Image Security | IMG- | 6-8 | aws ecr, kubectl |

Total: ~70-88 check items (dynamic, version-dependent)

## Workflow

1. **Confirm scope** — full cluster or specified namespaces/workloads
2. **Environment detection** — K8s version, EKS platform version, node distribution
3. **Dynamic research** — query context7 + aws-knowledge-mcp per dimension (sequential)
4. **Infrastructure assessment** (optional) — invoke aws-best-practice-research
5. **Workload data collection** — kubectl commands (parallelizable)
6. **Per-dimension assessment** — evaluate each workload against each check item
7. **Report generation** — single comprehensive assessment report
8. **Remediation guidance** — critical issues + prioritized recommendations

## Report Output

### Assessment Report (single file)
- Cluster overview
- Compliance scorecard with rating scale, top 3 priorities, and quick stats
- Dimension-by-dimension assessment tables
- Per-workload detail
- Critical issues and prioritized remediation
- Data sources / reference links

## Directory Structure

```
eks-workload-best-practice-assessment/
  SKILL.md
  README.md
  README_CN.md
  references/
    check-dimensions.md
    kubectl-assessment-commands.md
    search-queries.md
    output-template.md
```

## Language Policy

Follow user's conversation language (consistent with all existing skills in this repo).
