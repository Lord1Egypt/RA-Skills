---
name: aws-best-practice-research
description: >
  Use when researching, compiling, or assessing best practices for any AWS service,
  building HA/DR/security checklists from official AWS documentation, or checking whether
  live AWS resources follow official recommendations. Requires aws-knowledge-mcp-server.
  Triggers on "best practices", "compile checklist", "summarize HA/DR best practices",
  "what are the best practices for", "find all best practices", "check my cluster",
  "audit my redis", "assess my redis", "assessment", "是否符合最佳实践", "检查现有资源",
  "查找最佳实践", "编译检查清单", "总结最佳实践", "帮我查找", "汇总成表",
  "帮我检查", "审计一下", "评估一下".
---

# AWS Best Practice Research (with Optional Live Assessment)

Research and compile comprehensive best-practice checklists for any AWS service using the
[aws knowledge mcp server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) documentation search tools. Optionally assess live AWS resources
against the compiled checklist.

## Prerequisites

This skill requires the **[aws knowledge mcp server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server)** tools to be available:
- `aws___search_documentation` — search across AWS documentation topics
- `aws___read_documentation` — read full documentation pages
- `aws___recommend` — get related documentation recommendations

For the optional live assessment (Step 8):
- **AWS CLI** (`aws`) — must be configured with credentials that have read access to the target service
- **jq** — for parsing JSON output from AWS CLI commands

## Workflow

### Step 1: Identify Target Service and Assessment Scope

Determine from user input:
- **AWS Service** — e.g., ElastiCache Redis, RDS MySQL, MSK, EKS, Aurora, DynamoDB, etc.
- **Focus areas** — HA/DR, security, or all (default: all)
- **Live assessment info (optional)** — does the user provide any of the following?
  - AWS credentials (environment variables, profile, or credential file path)
  - AWS Region (e.g., us-west-2)
  - Resource identifiers (cluster name, instance ID, table name, etc.)

If the service is ambiguous, ask the user to clarify (e.g., "RDS MySQL or RDS PostgreSQL?").

Record whether a live assessment is requested:
- **If the user provides credentials + region + resource info** → run live assessment after checklist
- **If the user provides partial info** → ask for the missing pieces before proceeding
- **If the user provides no live resource info** → skip live assessment, produce checklist only

### Step 2: Sequential Documentation Search

Run the following 5 search queries **one at a time, sequentially** using `aws___search_documentation`.
**Do NOT run them in parallel** — the aws knowledge mcp server has rate limits and parallel
requests will trigger "Too many requests" errors.

Wait for each query to return results before sending the next one. Replace `{SERVICE}` with
the actual service name (e.g., "ElastiCache Redis", "Amazon RDS MySQL", "Amazon MSK").

```
Query 1: "{SERVICE} best practices high availability disaster recovery"
  topics: ["general"]
  limit: 10

Query 2: "{SERVICE} Well-Architected reliability resilience best practices"
  topics: ["general"]
  limit: 10

Query 3: "{SERVICE} replication multi-AZ failover cluster mode backup"
  topics: ["reference_documentation", "troubleshooting"]
  limit: 10

Query 4: "{SERVICE} security encryption authentication access control"
  topics: ["general"]
  limit: 10

Query 5: "{SERVICE} Well-Architected security best practices"
  topics: ["general"]
  limit: 10
```

**Rate limit protection**: If any query returns a "Too many requests" error, wait 5 seconds
and retry once. If it fails again, skip that query and continue with the next one.

### Step 3: Read Key Documentation Pages

From the search results, identify and read the most important pages **one at a time,
sequentially** using `aws___read_documentation`. **Do NOT read multiple pages in parallel**
to avoid rate limiting. Prioritize these document types:

1. **Well-Architected Lens** pages for the service (Reliability, Security, Performance, Operational Excellence pillars)
2. **Official best practices** page
3. **Resilience / disaster recovery** page
4. **Overall best practices** page

Read each with `max_length: 15000` to get comprehensive content. Typically 3-5 page reads are needed.

If a Well-Architected Lens exists for the service, it is the single most valuable source — always read it.

### Step 4: Extract and Categorize Check Items

From all gathered documentation, extract individual check items and organize them into
**5 mandatory categories** (see `references/output-template.md` for the exact format):

**Category 1: High Availability Architecture**
Items about: cluster mode, replication, replicas per shard, Multi-AZ, AZ distribution, node types, quorum.

**Category 2: Disaster Recovery**
Items about: automatic/manual backups, retention policies, RPO/RTO documentation, Global Datastore / cross-region replication, failover testing, replication lag monitoring.

**Category 3: Failover Planning**
Items about: Test Failover API, FIS resilience testing, client timeout/topology config, SNS event notifications, graceful degradation, WAIT command.

**Category 4: Security Configuration**
Items about: encryption at-rest/in-transit, authentication (AUTH/RBAC/IAM), subnet groups, security groups, KMS keys, dangerous command renaming, RBAC metrics monitoring, IAM control plane policies.

**Category 5: Others**
Items not covered by the above 4 categories, including but not limited to: auto minor version upgrade, engine version, node type selection (Graviton), CloudWatch monitoring, reserved memory, connection pooling, read routing, expensive commands, slow log, IaC management, Auto Scaling, cost tags, client retry logic, performance tuning, operational best practices.

#### Scope Boundary for Container / Orchestration Platforms

When the target service is a **container or orchestration platform** (EKS, ECS, Fargate, App Runner,
Elastic Beanstalk), this skill focuses **exclusively on the AWS infrastructure layer**. All check
items must be verifiable through AWS APIs (`aws eks`, `aws ecs`, `aws ec2`, `aws iam`, etc.).

**Do NOT include** check items that require `kubectl`, ECS Exec, or any in-cluster / in-task
inspection to verify. These belong to a dedicated workload-level assessment skill.

For **Amazon EKS**, the infrastructure layer scope includes:

| In Scope (AWS API verifiable) | Out of Scope (requires kubectl / workload context) |
|-------------------------------|-----------------------------------------------------|
| Control plane configuration (K8s version, platform version, API endpoint access, logging) | Pod Disruption Budgets (PDB) |
| Node group configuration (instance types, scaling, AMI, AZ distribution, disk size) | Topology Spread Constraints |
| Cluster networking (VPC, subnets, security groups, service CIDR) | Liveness / readiness / startup probes |
| Add-on presence and versions (VPC CNI, CoreDNS, kube-proxy, EBS CSI, etc.) | Container resource requests / limits |
| Secrets envelope encryption (KMS key) | Pod securityContext (runAsNonRoot, capabilities) |
| Authentication mode (ConfigMap vs API) and Access Entries | Pod Security Admission (PSA) namespace labels |
| Control plane audit logging | automountServiceAccountToken |
| Cluster deletion protection | Network Policies (K8s resource level) |
| Node auto-repair and node monitoring agent addon | Pod graceful termination (terminationGracePeriodSeconds, preStop) |
| Cluster tags and nodegroup tags | Workload-level Velero backups |
| Upgrade insights and deprecation warnings | Application health check paths |
| OIDC provider configuration (for IRSA) | Service mesh (mTLS) configuration |
| GuardDuty EKS protection (account-level) | OPA Gatekeeper / Kyverno policies |

For **Amazon ECS / Fargate**, apply the same principle: check cluster, capacity providers,
service auto-scaling, task definition registration, VPC configuration, and IAM roles — but do
NOT check container-level health checks, resource limits, or task-internal configuration.

After generating the checklist, append a **Scope Notice** (see `references/output-template.md`
for the exact format) directing users to a workload-level skill for the items that are out of scope.

For each check item, record:
- **ID** — category prefix + sequential number + priority suffix (e.g., `HA-01-hi`, `DR-02-md`, `SEC-03-lo`)
  - Priority suffixes: `-hi` (High), `-md` (Medium), `-lo` (Low)
  - This embeds priority directly in the ID for quick visual scanning
- **Check item name** — concise, actionable
- **Description** — what to check and why, specific thresholds or values where applicable
- **Source** — which document/control it comes from (see source annotation rules below)
- **Priority** — High / Medium / Low (also kept as a separate column for filtering)

### Step 5: Compile Source Annotations

Use consistent source tags throughout the checklist:

| Tag | Meaning |
|-----|---------|
| `WA-REL` / `WA-RELn` | Well-Architected Lens — Reliability Pillar (question N) |
| `WA-SEC` / `WA-SECn` | Well-Architected Lens — Security Pillar |
| `WA-PE` / `WA-PEn` | Well-Architected Lens — Performance Efficiency Pillar |
| `WA-OE` / `WA-OEn` | Well-Architected Lens — Operational Excellence Pillar |
| `WA-CO` | Well-Architected Lens — Cost Optimization Pillar |
| `Security Hub [{Service}.N]` | AWS Security Hub CSPM control (e.g., `[ElastiCache.1]`) |
| `re:Post` | AWS re:Post knowledge center article |
| `Official Docs` | Service user guide / official documentation |
| `AWS Blog` | AWS Database Blog or other official blog |
| `Whitepaper` | AWS whitepaper |

### Step 6: Generate Output (Conditional)

The output depends on whether the user provided live assessment info in Step 1:

#### If NO live assessment info was provided → Generate Checklist Only

Generate the checklist content using the exact format defined in `references/output-template.md`,
then **write it to a local markdown file** using the Write tool.

**File naming**: `YYYY-mm-dd-HH-MM-SS-{SERVICE}-best-practice-checklist.md`
- Replace `YYYY-mm-dd-HH-MM-SS` with the current timestamp (e.g., `2025-07-15-14-30-00`)
- Replace `{SERVICE}` with a lowercase, hyphen-separated service name (e.g., `elasticache-redis`, `amazon-eks`)
- Example: `2025-07-15-14-30-00-elasticache-redis-best-practice-checklist.md`
- Save the file in the current working directory

The checklist output must include:
1. Title with service name
2. One table per category (5 tables)
3. Source annotation legend
4. Key reference links section

After writing the file, inform the user of the file path.

#### If live assessment info WAS provided → Skip Checklist, Proceed to Step 8

Do NOT generate a separate checklist file. The assessment report (Step 8) will include the
full checklist with assessment results in a single, comprehensive document. Generating both
would be redundant.

Proceed directly to Step 8.

### Step 7: Offer Next Steps (Checklist-Only Path)

**This step only applies if you generated a checklist in Step 6 (no live assessment).**

After writing the checklist file, suggest:
- "I can export this to a spreadsheet if you prefer."
- "If you provide AWS credentials and resource identifiers, I can assess a live resource against this checklist."

**If the user provided live assessment info in Step 1, skip this step entirely** — you should
already be proceeding to Step 8.

### Step 8: Live Resource Assessment (Optional)

**Only execute this step if the user has provided credentials, region, and resource identifiers.**
If none were provided, skip this step entirely.

See `references/assessment-workflow.md` for the detailed per-service assessment procedure. The general
flow is:

#### 8.1 Prepare Environment

If the user provided a credential file path (e.g., `env.sh`), source it:
```bash
source <credential-file-path>
```

Verify access by running a simple describe command against the target service and region.

#### 8.2 Collect Resource Configuration

Run the service-specific AWS CLI commands to gather the full configuration of the target resource.
Execute independent commands in parallel to save time.

For **ElastiCache Redis**, the key commands are (see `references/assessment-workflow.md` for the full list):
- `aws elasticache describe-replication-groups`
- `aws elasticache describe-cache-clusters --show-cache-node-info`
- `aws elasticache describe-cache-subnet-groups`
- `aws elasticache describe-cache-parameters`
- `aws elasticache list-tags-for-resource`
- `aws elasticache describe-snapshots`
- `aws elasticache describe-events`

For other services, use the equivalent describe/list commands.

#### 8.3 Map Configuration to Checklist

For each check item in the checklist, determine the assessment status:

| Status | Meaning |
|--------|---------|
| **🟢 PASS** | The resource configuration meets or exceeds the recommendation |
| **🔴 FAIL** | The resource configuration does not meet the recommendation |
| **🟡 WARN** | Cannot be fully verified from infrastructure alone (e.g., client-side settings), or partially meets the recommendation |
| **⚪ N/A** | The check does not apply to this resource (e.g., Global Datastore check when cross-region DR is not required) |

For each item, record:
- The check ID and name (from the checklist)
- The assessment status (PASS / FAIL / WARN / N/A)
- A specific finding describing what was observed (include actual values)

#### 8.4 Generate Assessment Report

Generate the assessment results using the format defined in `references/output-template.md`,
then **write it to a local markdown file** using the Write tool.

**This is the ONLY output file when a target resource is provided.** The assessment report is
self-contained and includes all checklist information (Description, Source, Priority) alongside
the assessment results. Do NOT generate a separate checklist file.

**File naming**: `YYYY-mm-dd-HH-MM-SS-{RESOURCE_ID}-assessment-report.md`
- Replace `YYYY-mm-dd-HH-MM-SS` with the current timestamp (e.g., `2025-07-15-14-30-00`)
- Replace `{RESOURCE_ID}` with the actual resource identifier, lowercase, hyphens for separators
- Example: `2025-07-15-14-30-00-my-redis-cluster-assessment-report.md`
- Save the file in the current working directory

The report must include:
1. **Resource Summary** — key properties of the assessed resource (engine, version, node type, topology, etc.)
2. **Assessment Results by Category** — one table per category with full checklist columns
   (Check Item, Description, Source, Priority) PLUS assessment columns (Status, Finding)
3. **Assessment Summary** — counts of PASS/FAIL/WARN/N/A per category
4. **Critical Issues** — list of all FAIL items with Priority=High, with specific remediation guidance
5. **Recommendations** — grouped by urgency (Immediate / Short-term / Medium-term)
6. **Source Annotations** — legend for source abbreviations
7. **Key Reference Links** — documentation pages used

After writing the file, inform the user of the file path.

#### 8.5 Offer Remediation

After presenting the assessment results, suggest:
- Which FAIL items can be fixed in-place (e.g., enabling backups, adding tags)
- Which FAIL items require resource recreation (e.g., encryption at rest)
- Whether you can help execute the remediation commands

## Important Guidelines

- **Be comprehensive**: Search broadly, read deeply. The value of this skill is completeness.
  It's better to include a check item and mark it as lower priority than to miss it.
- **Always cite sources**: Every check item must have a source annotation.
  Users need to know where each recommendation comes from.
- **Always use sequential requests**: All searches and page reads must be executed one at a
  time, sequentially. **Never send multiple aws knowledge mcp server requests in parallel.**
  The MCP server has rate limits that will reject concurrent requests with "Too many requests"
  errors. Sequential execution is slower but reliable.
- **Rate limit protection**: If any MCP request returns a "Too many requests" error, wait
  5 seconds and retry the same request once. If it fails a second time, skip that request
  and continue with the next step. Do not retry more than once per request.
- **Focus on actionable items**: Each check item should be something the user can verify
  against their actual configuration. Avoid vague recommendations.
- **Include specific thresholds**: When documentation specifies numbers (e.g., "at least 2 replicas",
  "reserved-memory-percent >= 25%"), include them in the check description.
- **Note service-specific nuances**: If a check only applies under certain conditions
  (e.g., "only if cluster mode enabled"), note that in the description.
- **Live assessment is optional**: Never fail or block if the user doesn't provide credentials.
  The checklist alone is a complete, valuable deliverable.
- **Respect language**: Always output in the same language as the user's conversation.
