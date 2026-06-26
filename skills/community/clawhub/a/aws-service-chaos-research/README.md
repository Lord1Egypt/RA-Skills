[English](README.md) | [中文](README_CN.md)

# AWS Service-Specific Chaos & HA Testing Research Skill

An agent skill that generates comprehensive chaos engineering and high availability testing scenarios for any AWS service, using a **Scenario-Library-first** approach.

## Problem Statement

When planning chaos engineering or HA verification for AWS services, engineers face several challenges:

- **FIS Scenario Library is console-only** — AWS's curated composite scenarios (e.g., AZ Power Interruption) cannot be queried via CLI or API, so they are easily overlooked.
- **FIS action availability varies by region** — an action available in `us-east-1` may not exist in `ap-southeast-1`, leading to incorrect assumptions.
- **Even without native FIS actions, Scenario Library still applies** — composite scenarios like AZ Power Interruption can indirectly affect services that have no dedicated FIS actions (e.g., MSK), but users often don't realize this.
- **Documentation is scattered** — relevant information lives across User Guides, Blogs, Well-Architected Lenses, Troubleshooting pages, and FIS references, making manual consolidation time-consuming.

## What This Skill Does

1. **Scenario Library Research** — Reads the latest FIS Scenario Library documentation to discover AWS-curated composite resilience testing scenarios. This always runs first (highest priority).
2. **FIS Action Discovery** — Queries `aws fis list-actions` (or falls back to documentation search) to find service-specific fault injection actions in the target region.
3. **Documentation Research** — Searches official AWS documentation via [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) for HA/DR best practices, failure modes, and testing approaches.
4. **Report Generation** — Compiles all findings into a structured markdown report file (saved locally with `YYYY-mm-dd-HH-MM-SS-{service}-chaos-research.md` naming), containing scenario matrices, priority rankings, implementation best practices, and actionable next steps.

## Prerequisites

| Dependency | Required For | Notes |
|-----------|-------------|-------|
| [aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) | Scenario Library + documentation research | Provides `aws___search_documentation`, `aws___read_documentation`, `aws___recommend` tools |
| AWS CLI (`aws`) | FIS action discovery (preferred) | Falls back to documentation search if unavailable |

## Workflow Overview

```
Step 1: Identify target service + resolve region
         ↓
Step 2: Read FIS Scenario Library documentation [HIGHEST PRIORITY]
         ├── Scenario Library overview + scenario reference pages
         ├── Detailed scenario pages (AZ Power Interruption, AZ Slowdown, etc.)
         └── Extract sub-actions, resource tags, durations, prerequisites
         ↓
Step 3: Query FIS actions (list-actions --region)
         ├── 3a: Fetch all FIS actions in region
         ├── 3b: Filter for service-specific actions
         └── 3c: Optionally collect cross-cutting actions
         ↓
         ┌─── ≥1 service-specific actions ───┐─── 0 actions ───┐
         ↓                                    ↓                  │
Step 4: FIS-Enriched Path              Step 5: Doc-Only Path    │
         ├── 4a: Group by failure domain  ├── 5a: 6 doc searches │
         ├── 4b: Service built-in faults  ├── 5b: Read top pages │
         └── 4c: 5 doc searches           └── 5c: Alternatives   │
         ↓                                    ↓                  │
         └────────────────┬───────────────────┘                  │
                          ↓
Step 6: Save report to local file (YYYY-mm-dd-HH-MM-SS-{service}-chaos-research.md)
```

## Report Structure

Reports are saved directly to local markdown files (not printed to terminal). File names
use the format `YYYY-mm-dd-HH-MM-SS-{service}-chaos-research.md`. For multi-service
requests, one file is generated per service. A brief summary (file paths, key stats,
top 3 priorities) is printed to the terminal.

Every generated report contains these 7 sections:

| # | Section | Content |
|---|---------|---------|
| 1 | **Executive Summary** | Service, region, FIS support status, relevant Scenario Library scenarios, key recommendation |
| 2-N | **Per-Service Sections** | FIS native scenarios, service built-in fault injection, environment observations (or alternative testing methods if no FIS actions) |
| N+1 | **Scenario Library and Cross-Cutting** | Scenario Library composite scenarios (highest priority), cross-cutting actions (optional) |
| N+2 | **Recommended Test Priority** | All scenarios ranked P0-P3 with rationale and FIS experiment hints (action + target placeholders) for quick experiment creation |
| N+3 | **Implementation Best Practices** | Stop conditions, steady state definition, DNS/connection handling, blast radius control |
| N+4 | **Reference Materials** | Links from actual search results only (never fabricated) |
| N+5 | **Next Steps** | 3-4 actionable suggestions |

## Priority Guidelines

| Level | Criteria | Example |
|---|---|---|
| **P0 Must Test** | Scenario Library composite scenarios directly affecting the service; primary failover | AZ Power Interruption (with RDS failover), ElastiCache TestFailover |
| **P1 High** | AZ-level isolation, network partition | AZ Application Slowdown, `network:disrupt-connectivity` |
| **P2 Medium** | Performance degradation, replica failure | Read replica lag, Cross-AZ Traffic Slowdown |
| **P3 Optional** | API throttling, cross-region DR, cross-cutting actions | `inject-api-throttle-error`, Cross-Region Connectivity |

## Dual-Path Architecture

The skill automatically selects one of two paths based on FIS action availability:

**FIS-Enriched Path** (≥1 native actions found):
- Organizes FIS actions by failure domain (Instance, Storage, Network, AZ, Region, API)
- Checks for service built-in fault injection (e.g., Aurora `ALTER SYSTEM CRASH`, ElastiCache `test-failover`)
- Runs 5 sequential documentation searches for supplementary context

**Documentation-Only Path** (0 native actions):
- Runs 6 sequential documentation searches covering HA, DR, chaos, best practices, troubleshooting, and API references
- Compiles indirect FIS methods and AWS API/Console alternatives
- Scenario Library findings from Step 2 still apply

## Tool Dependencies

| Group | Tool | Purpose |
|---|---|---|
| **A — Scenario Library** | `aws___read_documentation` | Read FIS Scenario Library pages (console-only, cannot be queried via CLI) |
| **B — FIS Actions** | AWS CLI `aws fis list-actions` | Preferred: real-time FIS action query for target region |
| **B — FIS Actions** | `aws___search_documentation` | Fallback: search FIS action reference when CLI is unavailable |
| **C — Documentation** | `aws___search_documentation` | Search official docs (blogs, user guides, troubleshooting) |
| **C — Documentation** | `aws___read_documentation` | Read full documentation pages |
| **C — Documentation** | `aws___recommend` | Discover related documentation |

**Constraint:** All documentation research uses only Group A/B/C tools. SearXNG and other external search engines are not used.

## Directory Structure

```
aws-service-chaos-research/
├── SKILL.md                              # Main skill definition (agent instructions)
├── README.md                             # This file (PRD / user documentation)
├── README_CN.md                          # Chinese version
└── references/
    ├── search-queries.md                 # Search query templates + FIS Scenario Library URLs
    └── output-template.md                # Report output format specification
```

## Usage Examples

**Single service:**
```
"RDS chaos testing in us-west-2"
"How to test HA of ElastiCache Redis?"
"对 EKS 做混沌测试"
```

**Multiple services:**
```
"Chaos testing for EKS, RDS, MSK, and ElastiCache in us-west-2"
"帮我生成 us-east-1 区域 Aurora 和 DynamoDB 的混沌测试报告"
```

**Service without FIS actions:**
```
"How resilient is my MSK cluster?"
"OpenSearch fault injection testing"
"对 MSK 做高可用验证"
```

## Key Design Decisions

1. **Scenario Library first, always** — FIS Scenario Library composite scenarios are the most realistic resilience tests because they simulate multi-service failures simultaneously (e.g., AZ power outage affects compute, network, and database at once). They are always fetched before individual FIS actions.

2. **Scenario Library is documentation-driven** — Unlike FIS actions which can be queried via `list-actions`, Scenario Library scenarios are console-only. The skill must read documentation to discover them, making Step 2 a documentation fetch step, not a CLI step.

3. **Region-aware throughout** — FIS action availability varies by region. The skill resolves the target region first, passes `--region` to all CLI calls, and clearly states the region in the output.

4. **Sequential MCP requests** — All documentation searches and page reads are executed one at a time to avoid rate limiting from aws-knowledge-mcp-server. Slower but reliable.

5. **Cross-cutting actions are optional** — Network disruption, API fault injection, and EC2 actions can affect almost any service indirectly. They are included only when relevant, and explicitly marked as optional in the output.

6. **Scenario Library cross-reference dedup** — If a FIS action already appears as a sub-action in a Scenario Library composite scenario, it is annotated in the per-service table (e.g., "Also sub-action of AZ Power Interruption") rather than listed redundantly. If all FIS actions for a service are covered by Scenario Library scenarios, the per-service FIS Native sub-section is replaced with a note pointing to the Scenario Library section.

7. **Language follows user** — All output matches the language of the user's conversation (English, Chinese, etc.).

## Limitations

- Depends on aws-knowledge-mcp-server availability; if the MCP server is not configured, documentation research cannot run (FIS CLI queries still work).
- Sequential documentation gathering takes ~30-60 seconds for 5-6 queries + 3-5 page reads.
- Scenario Library content reflects documentation state at read time; newly added scenarios require re-reading the docs.
- The skill generates testing recommendations and report only — it does not execute FIS experiments or create experiment templates automatically.
- Cross-cutting action relevance depends on context; the skill uses heuristics (VPC-based, EC2-based, PrivateLink) to decide inclusion.
