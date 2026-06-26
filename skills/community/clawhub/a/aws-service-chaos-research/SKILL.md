---
name: aws-service-chaos-research
description: >
  Use when the user asks about chaos engineering, fault injection, resilience testing,
  or HA verification for a SPECIFIC AWS service (e.g., RDS, EKS, MSK, ElastiCache,
  DynamoDB, S3, Lambda, OpenSearch, etc.). Triggers on "chaos testing on [service]",
  "fault injection for [service]", "how to test HA of [service]",
  "FIS scenarios/actions for [service]", "[service] failover testing",
  "[service] resilience testing", "[service] 混沌测试", "[service] 故障注入",
  "[service] 高可用验证", "对 [service] 做混沌实验", "test my [service]",
  "verify my [service] is resilient". Use this skill even when the user phrases
  it casually like "test my RDS" or "how resilient is my MSK cluster".
---

# AWS Service-Specific Chaos & HA Testing Research

Generate comprehensive chaos engineering and high availability testing scenarios for a
specific AWS service. Uses a **Scenario-Library-first** approach: read the latest FIS
Scenario Library documentation for pre-built composite scenarios first, then query
individual FIS actions via `list-actions`, and finally supplement with deep documentation
research.

## Output Language Rule

Detect the language of the user's conversation and use the **same language** for all output.
- Chinese input -> Chinese output
- English input -> English output
- Mixed -> follow the dominant language

## Prerequisites

Required tools (at least one of each group):

**FIS Scenario Library (Group A — documentation-based, always available):**
- `aws___read_documentation` — read FIS Scenario Library pages directly (scenarios are
  console-only and cannot be queried via CLI, so reading the latest docs is the only way
  to discover them)

**FIS Actions Discovery (Group B — use in order of preference):**
1. **AWS CLI** `aws fis list-actions` — definitive, real-time list of FIS actions from user's region
2. **aws___search_documentation** — FIS actions reference page as fallback when CLI is unavailable

**Documentation Research (Group C):**
- `aws___search_documentation` — search AWS official docs
- `aws___read_documentation` — read full doc pages
- `aws___recommend` — discover related pages

All documentation research uses **only** the AWS Knowledge MCP tools above.
Do NOT use SearXNG or other web search tools for documentation research.

## Workflow

**CRITICAL — Sequential execution of all AWS Knowledge MCP calls:**
All calls to `aws___search_documentation`, `aws___read_documentation`, and
`aws___recommend` MUST be executed **one at a time, sequentially**. NEVER send
multiple MCP requests in parallel — the aws-knowledge-mcp-server has strict rate
limits and will reject concurrent requests with "Too many requests" errors.
Wait for each request to return a complete response before sending the next one.
This applies to ALL steps below (Step 2, 4b, 4c, 5a, 5b).

**Retry on failure:** If any MCP call (especially `aws___read_documentation`) returns
a rate limit error ("Too many requests") or any other transient error, **retry up to
10 times** with a 5-second wait between retries. Only skip the request after all 10
retries have failed.

**Multi-service requests:** When the user asks about multiple services (e.g.,
"EKS, RDS, MSK, and ElastiCache"), process them **one service at a time**. Complete
all research steps (Steps 2-5) for one service before starting the next. Do NOT
launch parallel research for multiple services — this will trigger rate limiting.
The Scenario Library fetch (Step 2) only needs to run once since it covers all
services; the per-service steps (3-5) must be repeated sequentially for each service.

### Step 1: Identify Target Service

Extract the target AWS service from the user's message and determine the target region.

#### Region Detection

FIS actions can differ across AWS regions — some actions may be available in
`us-east-1` but not yet in `ap-southeast-1`. Always determine the target region first,
because service keyword resolution depends on it.

**Detection order (use the first one that applies):**

1. **User explicitly specifies** — e.g., "us-west-2", "东京区域", "ap-northeast-1"
2. **Infer from context** — resource ARNs, previous conversation mentioning a region
3. **Check AWS CLI default** — run `aws configure get region` to get the configured default
4. **Ask the user** — if none of the above yields a region, ask:
   "Which AWS region are you targeting? FIS actions and scenarios may vary by region."

Store the resolved region as `TARGET_REGION` for use in subsequent steps.

#### Service Keyword Resolution

FIS action IDs follow the pattern `aws:<service>:<action>`. To map the user's input
to the correct FIS service keyword, use dynamic discovery from the live FIS action list:

```bash
aws fis list-actions --region TARGET_REGION | jq '.actions[].id' | awk -F':' '{print $2}' | sort -u
```

This returns the definitive list of FIS-supported service keywords in that region
(e.g., `ebs`, `ec2`, `ecs`, `eks`, `elasticache`, `fis`, `network`, `rds`, `s3`, `ssm`...).
Match the user's service name against this list. For example, if the user says
"Aurora", match it to `rds`; if "Kubernetes", match to `eks`.

If the AWS CLI is not available, derive the keyword by lowercasing the AWS service name
and removing spaces/hyphens (e.g., "ElastiCache" -> `elasticache`).

If the service is ambiguous, ask the user to clarify (e.g., "RDS MySQL or Aurora MySQL?").

Also determine the deployment architecture if the user mentions it:
- Multi-AZ, Multi-Region, Single-AZ
- Read replicas, Global Tables, Cross-region replication
- This affects which scenarios are relevant

### Step 2: Fetch FIS Scenario Library (Scenario-Library-First)

**This step has the highest priority.** The FIS Scenario Library provides AWS-curated
composite scenarios that orchestrate multiple fault injection actions into realistic
failure simulations. These are the most valuable starting point because they represent
AWS's own recommendations for how to test resilience.

Scenario Library scenarios are **console-only** — they cannot be listed or queried via
AWS CLI or API. The only way to discover them is by reading the latest documentation.

Fetch the Scenario Library pages listed in `references/search-queries.md` under
"FIS Scenario Library Pages (Always Fetch)". Read both the overview and detailed scenario
pages relevant to the target service. **Read pages one at a time, sequentially** —
wait for each `aws___read_documentation` call to complete before starting the next one.

#### From the scenario documentation, extract for each relevant scenario:

- **Scenario name and description**
- Which **sub-actions** the scenario orchestrates
- Which sub-actions are **relevant to the target service**
- What **resource tags** are required to target specific resources
- The **default durations** (interruption + recovery phases)
- Any **prerequisites or limitations**
- **Stop condition** recommendations

#### Decision: Which scenarios apply?

After reading the documentation, classify each scenario's relevance:

| Relevance | Criteria |
|---|---|
| **Directly relevant** | Scenario includes sub-actions that explicitly target the service (e.g., "Failover RDS" in AZ Power Interruption) |
| **Indirectly relevant** | Scenario affects infrastructure the service depends on (e.g., network disruption affects any VPC-based service) |
| **Not relevant** | Scenario has no meaningful impact on the target service |

Include both directly and indirectly relevant scenarios in the output.

### Step 3: Query FIS Actions

After the Scenario Library research, query individual FIS actions to discover
service-specific fault injection capabilities that may not be covered by composite
scenarios.

#### Path A: AWS CLI Available (Preferred)

**Step 3a: Fetch ALL FIS actions in the target region:**

```bash
aws fis list-actions --region TARGET_REGION --query 'actions[].{id:id, description:description}' --output json
```

Replace `TARGET_REGION` with the region resolved in Step 1 (e.g., `us-east-1`).
If no region was determined, omit `--region` to use the CLI default, but **warn
the user** that results reflect their default region and may differ in other regions.

**Step 3b: Filter for target service** — from the full list, find actions whose `id`
contains the search keyword(s) from Step 1:

```bash
aws fis list-actions --region TARGET_REGION --query 'actions[?starts_with(id, `aws:KEYWORD:`)].{id:id, description:description}' --output json
```

Also scan the description field for the service name, because some actions may
reference a service in their description even if the action prefix is different.

**Step 3c (Optional): Collect cross-cutting actions** — these affect services
indirectly. Include them if the user's service would benefit from network, API, or
infrastructure-level fault injection testing:

```bash
aws fis list-actions --region TARGET_REGION --query 'actions[?starts_with(id, `aws:network:`) || starts_with(id, `aws:fis:inject`) || starts_with(id, `aws:ssm:`) || starts_with(id, `aws:ec2:stop`) || starts_with(id, `aws:ec2:terminate`)].{id:id, description:description}' --output json
```

Cross-cutting actions and when they're useful:
- `aws:network:disrupt-connectivity` — useful for any VPC-based service
- `aws:network:disrupt-vpc-endpoint` — useful for services accessed via PrivateLink
- `aws:fis:inject-api-internal-error` — useful to test app handling of AWS API failures
- `aws:fis:inject-api-throttle-error` — useful to test backoff/retry logic
- `aws:fis:inject-api-unavailable-error` — useful to test graceful degradation
- `aws:ec2:stop-instances` / `terminate-instances` — useful for services running on EC2
- `aws:ssm:send-command` / `start-automation-execution` — useful for custom fault scripts

Whether to include cross-cutting actions depends on context:
- **Include** when the service runs on EC2, uses VPC networking, or the user is
  interested in infrastructure-level failure testing
- **Skip** when the user is focused only on service-native failures, or the service
  is fully managed with no user-accessible infrastructure layer

#### Path B: AWS CLI Not Available

Search the FIS actions reference documentation:
```
aws___search_documentation(
  search_phrase="AWS FIS actions [SERVICE_NAME] fault injection",
  topics=["reference_documentation"],
  limit=10
)
```

Then read the FIS actions reference page:
```
aws___read_documentation(
  url="https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html",
  max_length=10000
)
```

#### Decision Point: FIS Actions Found?

Count the number of **service-specific** actions found (exclude cross-cutting actions).

- **YES (1+ service-specific actions found)** -> Continue to Step 4 (FIS-Enriched Path)
- **NO (zero service-specific actions)** -> Jump to Step 5 (Documentation-Only Path)

### Step 4: FIS-Enriched Path

When FIS has native actions for the target service, combine Scenario Library findings
with FIS-action-specific details.

#### 4a: Organize FIS Actions into Testing Scenarios

Map each FIS action to a testing scenario. Use the "FIS Native Fault Injection
Scenarios" table format from `references/output-template.md`.

**IMPORTANT — Scenario Library deduplication (must apply before building the table):**
Before listing any FIS action in the per-service table, check whether that exact
action ID appeared as a sub-action in any Scenario Library composite scenario
discovered in Step 2. Common examples of overlap:
- `aws:rds:failover-db-cluster` — sub-action of AZ Power Interruption
- `aws:elasticache:replicationgroup-interrupt-az-power` — sub-action of AZ Power Interruption
- `aws:eks:pod-network-latency` — sub-action of AZ Application Slowdown
- `aws:eks:pod-network-packet-loss` — sub-action of Cross-AZ Traffic Slowdown
- `aws:ec2:stop-instances` — sub-action of AZ Power Interruption

Rules:
1. If an action **is** a Scenario Library sub-action, **still list it** in the
   per-service table but append to the "HA Verification Purpose" column:
   "(Also sub-action of {Scenario Name} — see Scenario Library section)".
2. If **all** service-specific FIS actions are Scenario Library sub-actions (e.g.,
   ElastiCache has only `replicationgroup-interrupt-az-power` which is covered by
   AZ Power Interruption), **omit** the "FIS Native Fault Injection Scenarios"
   sub-section entirely and replace with:
   > All FIS native actions for {SERVICE} are covered by Scenario Library composite
   > scenarios. See the Scenario Library and Cross-Cutting section for details.

Group scenarios by failure domain:
1. **Instance/Task Level** — individual resource failure
2. **Storage Level** — disk/volume failure or degradation
3. **Network Level** — connectivity disruption
4. **AZ Level** — availability zone failure simulation
5. **Region Level** — cross-region failover
6. **API/Control Plane** — AWS API errors

**Scenario Library cross-reference:** For each FIS action, check whether it also
appears as a sub-action in any Scenario Library composite scenario discovered in
Step 2. If it does, append a note in the "HA Verification Purpose" column (e.g.,
"Also a sub-action of AZ Power Interruption — see Scenario Library section"). If
**all** service-specific FIS actions are sub-actions of Scenario Library scenarios,
omit the "FIS Native Fault Injection Scenarios" sub-section entirely and replace
it with a note: "All FIS native actions for this service are covered by Scenario
Library composite scenarios — see the Scenario Library and Cross-Cutting section."

#### 4b: Enrich with Service-Specific Capabilities

Some services have **built-in fault injection** beyond FIS. Search for these
(**sequentially** — wait for the search to complete before reading any result pages):

```
aws___search_documentation(
  search_phrase="[SERVICE_NAME] fault injection testing failover simulation",
  topics=["general", "reference_documentation"],
  limit=10
)
```

If found, add a "Service Built-in Fault Injection" section using the table format from
`references/output-template.md`.

#### 4c: Deep Documentation Research

Use the search queries from `references/search-queries.md` under "FIS-Enriched Path".
Run all 5 queries **sequentially** (one at a time). After searches, read the top 3-5
most relevant pages **one at a time** and use `aws___recommend` on the most relevant
page for discovery. Never send multiple read or recommend requests in parallel.

### Step 5: Documentation-Only Path (No FIS Actions)

When FIS has no native actions for the target service, fall back to comprehensive
documentation research. Note that Scenario Library findings from Step 2 still apply.

#### 5a: Deep Documentation Search

Use the search queries from `references/search-queries.md` under "Documentation-Only Path".
Run all 6 queries **sequentially** (one at a time, wait for each to complete).

#### 5b: Read Key Pages and Discover Related Content

From the combined search results, read the **top 5 most relevant pages** following the
priority order in `references/search-queries.md`. Read pages **one at a time** — wait
for each `aws___read_documentation` call to complete before the next. Then use
`aws___recommend` on the service's main documentation page to discover related content.

Extract from all pages:
- **Failure modes** the service can experience
- **Built-in HA mechanisms** (automatic failover, replication, etc.)
- **Testing approaches** documented in official guides
- **Monitoring/metrics** to watch during tests

#### 5c: Compile Alternative Testing Approaches

Use the "Testing Methods (No Native FIS Actions)" section format from `references/output-template.md`,
including both indirect FIS actions and AWS API/Console methods.

### Step 6: Compile Output and Save to Local File

**Write the report directly to a local markdown file** instead of outputting the full
content to the terminal. Use the following file naming convention:

```bash
TIMESTAMP=$(TZ=Asia/Shanghai date +%Y-%m-%d-%H-%M-%S)
SERVICE_SLUG=$(echo "{SERVICE_NAME}" | tr '[:upper:]' '[:lower:]' | tr ' :/' '-')
# File name: ${TIMESTAMP}-${SERVICE_SLUG}-chaos-research.md
```

For multi-service requests, generate **one file per service**:
- `${TIMESTAMP}-rds-chaos-research.md`
- `${TIMESTAMP}-eks-chaos-research.md`
- etc.

Compile the report content using the exact format defined in `references/output-template.md`
and save it to the file. The report must include all sections in this order:

1. **Executive Summary** — overview with region, FIS support status, key recommendation
2. **Scenario Library and Cross-Cutting** — Scenario Library composite scenarios (highest priority), cross-cutting actions as optional supplement. **This section comes BEFORE per-service sections.**
3. **Per-service sections** — each with: FIS scenarios (using `{SVC}-#` test IDs, e.g., `EKS-1`, `Redis-1`), built-in methods, recommended testing scenario matrix, environment observations, and stop conditions
4. **Recommended Test Priority (Consolidated)** — references test IDs from per-service sections; do NOT duplicate full descriptions; do NOT list a FIS action separately if already covered by a Scenario Library scenario in the same table
5. **Implementation Best Practices** — steady state, DNS/connection, blast radius
6. **Reference Materials** — only URLs from actual search results or pages read
7. **Next Steps** — 3-4 actionable next steps

After saving, print a brief summary to the terminal listing only:
- The file path(s) of the generated report(s)
- Target service(s) and region
- Number of FIS actions found (service-specific + cross-cutting)
- Number of Scenario Library scenarios identified
- Top 3 recommended test priorities

## Important Guidelines

- **Scenario Library first, always.** The FIS Scenario Library represents AWS's own
  curated resilience testing scenarios. Always read the latest Scenario Library
  documentation before anything else. These are documentation-based (console-only),
  not CLI-queryable.
- **Region matters.** Always resolve the target region before querying FIS actions.
  FIS action availability varies by region. Always pass `--region` to the AWS CLI and
  clearly state the region in the output.
- **Don't fabricate FIS actions.** If an action doesn't exist, say so clearly. The
  fallback path exists precisely for services FIS doesn't cover.
- **Don't fabricate links.** Only include URLs from actual search results or known
  documentation pages you've read.
- **Be specific about the service.** Every recommendation should reference the specific
  service, its HA mechanisms, and its specific metrics.
- **Cross-cutting actions are optional context.** Include them when they add value,
  but focus on service-specific actions and Scenario Library scenarios first.
- **AWS Knowledge MCP only for docs research.** Do NOT use SearXNG or other web search.
  Use `aws___search_documentation`, `aws___read_documentation`, and `aws___recommend`.
- **Search across multiple topics.** Use different `topics` values (`general`,
  `reference_documentation`, `troubleshooting`) sequentially.
- **Use aws___recommend for discovery.** After reading a key page, call `aws___recommend`
  to find related content that keyword search may miss.
- **NEVER send MCP requests in parallel.** All calls to `aws___search_documentation`,
  `aws___read_documentation`, and `aws___recommend` MUST be executed one at a time.
  Wait for each response before sending the next request. Parallel calls will trigger
  "Too many requests" errors from the aws-knowledge-mcp-server. This is the single
  most common cause of failures — enforce strictly in every step.
- **Retry on failure — up to 10 times.** If any MCP call fails with a rate limit or
  transient error, wait 5 seconds and retry. Repeat up to 10 times before skipping.
- **Respect language.** Output in the same language as the user's conversation.
