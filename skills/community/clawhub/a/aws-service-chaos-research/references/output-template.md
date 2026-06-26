# Output Template

Use this structure when generating the chaos testing report. Replace `{SERVICE}`,
`{REGION}`, and other placeholders with actual values.

**Language**: All table headers, descriptions, and text must be in the same language as
the user's conversation. The template below uses English as an example — translate
all content (including section titles, column headers, and descriptions) if the
conversation is in another language (e.g., Chinese).

---

## {SERVICE} HA Chaos Testing Report — {REGION} Region

### 1. Executive Summary

Provide a 3-5 sentence overview covering:
- Target service, its HA architecture (Multi-AZ, cluster mode, replication topology, etc.)
- Target region and FIS native support status (how many FIS actions available)
- Which FIS Scenario Library composite scenarios are relevant
- Key testing recommendation

If the report covers **multiple services**, use a summary table:

| Service | Resource Name | HA Architecture | FIS Native Support |
|---|---|---|---|
| **{SERVICE_1}** | `{RESOURCE_ID}` | {HA_DESCRIPTION} | {N} FIS actions |
| **{SERVICE_2}** | `{RESOURCE_ID}` | {HA_DESCRIPTION} | 0 FIS actions |

Followed by a brief paragraph highlighting key findings across all services.

---

### 2. FIS Scenario Library Composite Scenarios

**This section comes BEFORE per-service sections** because Scenario Library composite
scenarios have the highest priority — they represent AWS's own curated resilience
testing recommendations and simulate realistic multi-service failure patterns.

Present an overview table of all relevant Scenario Library scenarios, then provide
detail sub-sections for each.

#### Overview Table

| # | Scenario | Scope | {SERVICE_1} | {SERVICE_2} | ... | Default Duration |
|---|---|---|---|---|---|---|
| 1 | **AZ Availability: Power Interruption** | Full AZ power failure | Direct | Direct | ... | 30min + 30min recovery |
| 2 | **AZ: Application Slowdown** | Intra-AZ latency injection | Direct | Indirect | ... | 30min |

Use "Direct" when the scenario includes sub-actions that explicitly target the service,
"Indirect" when it affects infrastructure the service depends on.

#### 2.x {Scenario Name} Detail

For each relevant Scenario Library scenario, create a detail sub-section containing:

**Sub-Actions Table:**

| Sub-Action | FIS Action | Affected Service | Resource Tag |
|---|---|---|---|
| {sub-action name} | `{action}` | {service} | `{TagKey}: {TagValue}` |

List only the sub-actions that are relevant to the user's environment.

**Required Resource Tags** (if applicable):

| Resource Type | Tag Key | Tag Value | Description |
|---|---|---|---|
| {resource type} | `AzImpairmentPower` | `{value}` | {description} |

**Why This Scenario Matters:** Brief paragraph on why this composite scenario matters.

**Default Duration:** Interruption + recovery phases.

#### Cross-Cutting Actions — Optional

> Cross-cutting actions are optional supplementary scenarios for testing infrastructure-level
> fault impact on services indirectly.

| Test Scenario | FIS Action | Applicable Services |
|---|---|---|
| {scenario} | `{action}` | {which services are affected} |

Cross-cutting actions to include when relevant:
- `aws:network:disrupt-connectivity` — any VPC-based service (simulates AZ network failure)
- `aws:network:disrupt-vpc-endpoint` — PrivateLink services
- `aws:fis:inject-api-internal-error` — AWS API failures (any AWS service control plane)
- `aws:fis:inject-api-throttle-error` — API throttling (any AWS service API calls)
- `aws:fis:inject-api-unavailable-error` — graceful degradation (any AWS service control plane)
- `aws:ec2:stop-instances` / `terminate-instances` — EC2-based services
- `aws:network:route-table-disrupt-cross-region-connectivity` — cross-region DR
- `aws:ssm:send-command` — custom fault injection scripts

**When to include**: only when the user's service runs on EC2, uses VPC networking,
or the user explicitly requests infrastructure-level failure testing. **Skip** when
the user is focused only on service-native failures.

---

### 3-N. Per-Service Sections

For **each service**, create a numbered section (Section 3, 4, 5, ...) with the
following sub-sections. If only one service is being tested, use Section 3 only.

**RED FLAG — Common mistake to avoid:**
Do NOT use `| # | ...` numbered rows as the test plan. The ONLY table with test
identifiers in each per-service section is the "Recommended Testing Scenario Matrix"
at the end, which uses `Test ID` column with `{SVC}-1` format. All other tables
(FIS Native, Built-in, Testing Methods) are reference lists — they do NOT have
numbered `#` columns.

#### {N}. {SERVICE} — {RESOURCE_ID}

##### FIS Native Fault Injection Scenarios

Use this sub-section when FIS has native actions for the service.
This is a **reference list** of available FIS actions — NOT the test plan.

**IMPORTANT — Scenario Library deduplication:** Before building this table, check
each FIS action against the Scenario Library composite scenarios in Section 2.
If an action already appears as a sub-action there (e.g., `aws:rds:failover-db-cluster`
is a sub-action of AZ Power Interruption), you MUST append a note to the
"HA Verification Purpose" cell:

> "(Also sub-action of AZ Power Interruption — see Scenario Library section)"

**All actions covered:** If EVERY FIS action for this service is a Scenario Library
sub-action (e.g., ElastiCache has only `replicationgroup-interrupt-az-power` which
is covered by AZ Power Interruption), OMIT this entire sub-section and replace with:

> All FIS native actions for {SERVICE} are covered by Scenario Library composite
> scenarios. See Section 2 for details.

**Otherwise**, list the actions in this table (NO `#` column — this is a reference list):

| FIS Action | Description | HA Verification Purpose |
|---|---|---|
| `aws:{service}:{action}` | {what the action does} | {what resilience property it validates} |

Group scenarios by failure domain when there are many:
1. **Instance/Task Level** — individual resource failure
2. **Storage Level** — disk/volume failure or degradation
3. **Network Level** — connectivity disruption
4. **AZ Level** — availability zone failure simulation

##### Service Built-in Fault Injection

Use this sub-section for service-native fault injection methods (not FIS).
This is a **reference list** — NOT the test plan.

| Method | Command/API | What It Simulates |
|---|---|---|
| {method name} | `{CLI command or API call}` | {what it simulates} |

Known built-in capabilities to check:
- **Aurora MySQL/PostgreSQL**: `ALTER SYSTEM CRASH`, `ALTER SYSTEM SIMULATE READ REPLICA FAILURE`
- **RDS Multi-AZ**: `reboot-db-instance --force-failover`
- **ElastiCache**: `test-failover` API
- **DynamoDB**: On-demand backup/restore testing

##### Testing Methods (No Native FIS Actions)

Use this sub-section instead of "FIS Native Fault Injection Scenarios" when the service
has **no native FIS actions**. Include a note explaining this.

> **Note:** AWS FIS does not currently have dedicated actions for {SERVICE} in {REGION}.
> The following approaches use indirect FIS actions, AWS APIs, and manual methods.

###### Indirect FIS Fault Injection

| Test Scenario | Method | What It Validates |
|---|---|---|
| {scenario} | `{FIS action or method}` | {what it validates} |

###### AWS API / Console Methods

| Test Scenario | Method | What It Validates |
|---|---|---|
| {scenario} | `{CLI/API/Console method}` | {what it validates} |

##### Recommended Testing Scenario Matrix (REQUIRED)

**IMPORTANT — This sub-section is MANDATORY for every service.** It is the single
authoritative test plan for this service. All other sub-sections above (FIS Native,
Built-in, Testing Methods) are reference information only — they list available
capabilities, NOT the test plan.

This matrix combines FIS native actions, service built-in methods, Scenario Library
references, and indirect methods into ONE prioritized table with unique Test IDs.

**Test ID format:** Use `{SERVICE_SHORT}-{NUMBER}` as the FIRST column. The service
short name MUST be a 3-letter (or short) abbreviation. Numbers are sequential starting
from 1:
- EKS → `EKS-1`, `EKS-2`, `EKS-3`, ...
- ElastiCache Redis → `RDS-1`, `RDS-2`, ... (use `RDS` for Redis to keep 3 chars; or `RED` if RDS MySQL also present)
- RDS MySQL → `RDS-1`, `RDS-2`, ...
- MSK → `MSK-1`, `MSK-2`, ...
- DynamoDB → `DDB-1`, `DDB-2`, ...
- When both ElastiCache Redis and RDS MySQL are in the same report, use distinct prefixes:
  ElastiCache → `ECR-1` or `RED-1`, RDS → `RDS-1`

**Table format (use exactly these columns):**

| Test ID | Test Scenario | Method | Verification Target | Priority |
|---|---|---|---|---|
| EKS-1 | {scenario name} | {FIS action / API / Scenario Library ref} | {what it validates} | P0 |
| EKS-2 | {scenario name} | {method} | {what it validates} | P1 |

When referencing a Scenario Library composite scenario, use the format:
"Scenario Library: {Scenario Name}" in the Method column.

##### Environment Observations

Brief bullet-point notes about the actual resource configuration discovered during
research. Include:
- Key configuration details (engine, instance type, topology)
- Important observations or warnings
- Architecture notes that affect testing strategy

##### Stop Conditions for {SERVICE}

| Metric | Source | Recommended Threshold |
|---|---|---|
| `{CloudWatch metric}` | {source} | {threshold} |

---

### {N+1}. Recommended Test Priority (Consolidated)

This section consolidates all per-service test scenarios into a single priority-ranked
table. **You MUST reference the Test IDs** (e.g., `EKS-1`, `RDS-3`, `MSK-2`) from the
per-service "Recommended Testing Scenario Matrix" tables. Do NOT invent new scenario
names or repeat full descriptions — use the Test ID as the primary reference.

| Priority | Test ID | Scenario (brief) | Target Service | FIS Experiment Hint | Reason |
|---|---|---|---|---|---|
| **P0 Must Test** | EKS-1 | {brief name from matrix} | EKS | {one-line: FIS action/method + target placeholders} | {why it's critical} |
| **P0 Must Test** | RDS-1 | {brief name from matrix} | RDS MySQL | {one-line: FIS action/method + target placeholders} | {why it's critical} |
| **P1 High** | MSK-3 | {brief name from matrix} | MSK | {one-line: FIS action/method + target placeholders} | {why it's important} |

**FIS Experiment Hint format:** A one-line description specifying the FIS action (or
method) and target resource, using `{PLACEHOLDER}` for resource identifiers the customer
needs to fill in. This helps customers quickly create the corresponding FIS experiment.

Examples:
- FIS native action: `` `aws:rds:failover-db-cluster` targeting cluster `{DB_CLUSTER_ID}` ``
- FIS native action: `` `aws:lambda:invocation-add-delay` targeting function `{FUNCTION_ARN}`, startupDelayMilliseconds=`{DELAY_MS}` ``
- FIS native action: `` `aws:eks:pod-network-latency` targeting cluster `{EKS_CLUSTER}` namespace `{NAMESPACE}` ``
- Scenario Library: `` Scenario Library "AZ Power Interruption" — tag resources with `AzImpairmentPower: {AZ_ID}` ``
- Service built-in: `` `aws rds reboot-db-instance --db-instance-identifier {DB_INSTANCE_ID} --force-failover` ``
- Cross-cutting: `` `aws:network:disrupt-connectivity` targeting subnet `{SUBNET_ID}` in `{AZ}` ``
- No FIS action: `` No native FIS action — use `aws:ssm:send-command` with custom script on `{INSTANCE_ID}` ``

Priority guidelines:
- **P0**: FIS Scenario Library composite scenarios directly affecting the service; failover / primary failure (impacts RTO)
- **P1**: AZ-level failure, network isolation (multi-AZ resilience); service-specific critical tests
- **P2**: Performance degradation, replica failure (read availability)
- **P3**: API throttling, cross-region DR, cross-cutting actions (advanced scenarios)

**Dedup with Scenario Library:** Do NOT list a FIS action as a separate priority item
if it is already covered as a sub-action of a Scenario Library composite scenario
listed in this same table. For example, if "AZ Power Interruption" is listed as P0
and it already includes `aws:rds:failover-db-cluster` as a sub-action, do NOT add
a separate P0 row for `aws:rds:failover-db-cluster`. The Scenario Library composite
scenario entry already covers it.

---

### {N+2}. Implementation Best Practices

#### Steady State Definition

- **{SERVICE}**: {metrics that define normal operation}

#### DNS / Connection Handling

- **{SERVICE}**: {service-specific reconnection considerations}

#### Blast Radius Control

1. {guidance on starting small}
2. {guidance on progressive escalation}
3. {guidance on AZ isolation}

---

### {N+3}. Reference Materials

| # | Type | Title | Link |
|---|---|---|---|
| 1 | {Docs/Blog/Well-Architected} | {title} | {URL} |

Only include URLs from actual search results or documentation pages read.
Never fabricate links.

---

### {N+4}. Next Steps

Suggest 3-4 actionable next steps tailored to the service(s), for example:
1. Generate a complete FIS experiment template (JSON) for {scenario}
2. Design CloudWatch alarms to use as FIS experiment Stop Conditions
3. Verify {service-specific config} configuration
4. Start execution with the simplest P0 scenario

---

## Formatting Rules

1. **Section ordering**: Executive Summary → Scenario Library & Cross-Cutting → Per-Service sections → Consolidated Priority → Best Practices → References → Next Steps
2. **Test ID is the ONLY numbered identifier in per-service sections**: The `Test ID` column (`EKS-1`, `RDS-2`, `MSK-1`, etc.) in the "Recommended Testing Scenario Matrix" is the ONLY place where rows are numbered/identified. All other tables (FIS Native, Built-in, Testing Methods, Cross-Cutting) are reference lists and do NOT have a `#` column. If you find yourself writing `| # | ...` in a per-service table, STOP — that column belongs only in the Scenario Matrix.
3. **Consolidated priority table references Test IDs**: The consolidated priority table MUST have a `Test ID` column that references IDs from per-service matrices (e.g., `EKS-1`, `RDS-3`). Do NOT write scenario names without IDs.
4. **Per-service sections** each get their own numbered section with service name and resource ID
5. **Table consistency**: All tables within the same sub-section type use identical column headers
6. **FIS Action IDs** always in backtick code format: `aws:service:action`
7. **CLI commands** in backtick code format
8. **Service names** in bold when used as labels
9. **Priority labels** in bold: **P0 Must Test**, **P1 High**, **P2 Medium**, **P3 Optional**
10. **Environment observations** use bullet points, keep concise
11. **Scenario Library section comes BEFORE per-service sections**: Scenario Library composite scenarios are the primary content with highest priority
12. **Language**: Follow the same language as the conversation throughout
