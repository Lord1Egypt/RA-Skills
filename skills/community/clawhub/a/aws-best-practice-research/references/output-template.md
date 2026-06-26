# Output Template

This template covers **two output modes** depending on whether a live target resource is provided:

| Mode | When to Use | Output File |
|------|-------------|-------------|
| **Checklist Mode** | No target resource provided | `{SERVICE}-best-practice-checklist.md` |
| **Assessment Mode** | Target resource provided | `{RESOURCE_ID}-assessment-report.md` |

**Language**: All content must be in the same language as the user's conversation.

---

# Mode 1: Checklist Only (No Target Resource)

Use this format when the user does NOT provide a live resource to assess.

**File naming**: `YYYY-mm-dd-HH-MM-SS-{SERVICE}-best-practice-checklist.md`
- `{SERVICE}` = lowercase, hyphen-separated service name (e.g., `elasticache-redis`, `amazon-eks`)

---

## {SERVICE} Best Practice Checklist (HA/DR/Security)

### Category 1: High Availability Architecture

| # | Check Item | Description | Source | Priority |
|---|------------|-------------|--------|----------|
| HA-01-hi | **Item name** | What to check, specific thresholds, conditions | Source tag | High |
| HA-02-md | ... | ... | ... | Medium |

### Category 2: Disaster Recovery

| # | Check Item | Description | Source | Priority |
|---|------------|-------------|--------|----------|
| DR-01-hi | **Item name** | What to check, specific thresholds, conditions | Source tag | High |

### Category 3: Failover Planning

| # | Check Item | Description | Source | Priority |
|---|------------|-------------|--------|----------|
| FP-01-hi | **Item name** | What to check, specific thresholds, conditions | Source tag | High |

### Category 4: Security Configuration

| # | Check Item | Description | Source | Priority |
|---|------------|-------------|--------|----------|
| SEC-01-hi | **Item name** | What to check, specific thresholds, conditions | Source tag | High |

### Category 5: Others

| # | Check Item | Description | Source | Priority |
|---|------------|-------------|--------|----------|
| OT-01-md | **Item name** | What to check, specific thresholds, conditions | Source tag | Medium |

*(Include Source Annotations, Key Reference Links, and Scope Notice sections from the Common Sections below)*

---

# Mode 2: Assessment Report (With Target Resource)

Use this format when the user provides credentials, region, and resource identifiers.
**This is the ONLY output** — do NOT also generate a separate checklist file.

**File naming**: `YYYY-mm-dd-HH-MM-SS-{RESOURCE_ID}-assessment-report.md`
- `{RESOURCE_ID}` = actual resource identifier, lowercase, hyphens for separators

---

## {SERVICE} Best Practice Assessment: `{RESOURCE_ID}` ({REGION})

### Resource Summary

| Property | Value |
|----------|-------|
| Resource ID | `{RESOURCE_ID}` |
| Engine / Service | {ENGINE} {VERSION} |
| Node Type / Instance Class | {NODE_TYPE} |
| Topology | {TOPOLOGY_DESCRIPTION} |
| Multi-AZ | {ENABLED/DISABLED} |
| Auto Failover | {ENABLED/DISABLED} |
| Encryption At Rest | {ENABLED/DISABLED} |
| Encryption In Transit | {ENABLED/DISABLED} |
| Authentication | {AUTH_METHOD or NONE} |

Add service-specific properties as needed.

---

### Category N: {Category Name}

| # | Check Item | Description | Source | Priority | Status | Finding |
|---|------------|-------------|--------|----------|--------|---------|
| XX-01-hi | **Item name** | What to check, thresholds | Source tag | High | 🟢 PASS | Actual value observed |
| XX-02-md | **Item name** | What to check, conditions | Source tag | Medium | 🔴 FAIL | Value observed, issue |
| XX-03-lo | **Item name** | What to check | Source tag | Low | 🟡 WARN | Cannot verify from API |
| XX-04-md | **Item name** | What to check | Source tag | Medium | ⚪ N/A | Does not apply (reason) |

Repeat for all 5 categories (High Availability, Disaster Recovery, Failover Planning,
Security Configuration, Others).

---

### Assessment Summary

| Category | Pass | Fail | Warn | N/A |
|----------|------|------|------|-----|
| HA Architecture | n | n | n | n |
| Disaster Recovery | n | n | n | n |
| Failover Planning | n | n | n | n |
| Security Configuration | n | n | n | n |
| Others | n | n | n | n |
| **Total** | **n** | **n** | **n** | **n** |

---

### Critical Issues (Must Fix)

List all FAIL items where Priority = High:

1. **{CHECK_ID}: {Check Item Name}** — {Description of issue and observed value}.
   **Remediation**: {Specific action, note if requires resource recreation}.

---

### Recommendations

**Immediate** (can fix in-place, no downtime):
- Item 1...

**Short-term** (may require maintenance window or resource recreation):
- Item 1...

**Medium-term** (optimization, monitoring improvements):
- Item 1...

*(Include Source Annotations and Key Reference Links sections from the Common Sections below)*

---

# Common Sections (Include in Both Modes)

### Source Annotations

| Abbreviation | Source |
|--------------|--------|
| WA-REL | Well-Architected Lens - Reliability Pillar |
| WA-SEC | Well-Architected Lens - Security Pillar |
| WA-PE | Well-Architected Lens - Performance Efficiency Pillar |
| WA-OE | Well-Architected Lens - Operational Excellence Pillar |
| WA-CO | Well-Architected Lens - Cost Optimization Pillar |
| Security Hub [{Service}.N] | AWS Security Hub CSPM control |
| re:Post | AWS re:Post knowledge center article |
| Official Docs | Service user guide |
| AWS Blog | AWS official blog post |
| Whitepaper | AWS whitepaper |

### Key Reference Links

- [Link 1 title](URL)
- [Link 2 title](URL)
- ...

List the 5-10 most important documentation pages used.

### Scope Notice (Container/Orchestration Platforms Only)

**Include only for EKS, ECS, Fargate, App Runner, Elastic Beanstalk — omit for other services.**

> **Scope**: This checklist/assessment covers **AWS infrastructure-level** best practices only —
> items verifiable through AWS APIs (`aws eks`, `aws ecs`, `aws ec2`).
>
> **Workload-level items not covered** (require `kubectl` / in-cluster access):
> - Pod Disruption Budgets (PDB) and replica counts
> - Topology Spread Constraints and pod anti-affinity
> - Liveness / readiness / startup probes
> - Container resource requests and limits
> - Pod security context (runAsNonRoot, capabilities)
> - Network Policies (Kubernetes resource level)
> - Pod graceful termination settings
>
> For workload-level assessment, use a dedicated **container workload assessment skill**.

---

# Formatting Rules

## Check Items
1. **Check item names** should be bold and concise
2. **Descriptions** should include specific values/thresholds when available
3. **Source tags** use abbreviations from the table above; multiple sources separated by " / "
4. **Priority assignment**:
   - **High**: Data loss risk, no encryption, no authentication, no backup, no HA
   - **Medium**: Non-optimal configuration, missing DR, missing monitoring
   - **Low**: Performance optimization, cost tags, non-latest instance types
5. Each category: minimum 3 items, typically 5-15 items
6. Total checklist: 30-50 items for well-documented services

## Assessment Status (Mode 2 Only)
1. **Status badges**:
   - `🟢 PASS` — meets recommendation
   - `🔴 FAIL` — does not meet recommendation
   - `🟡 WARN` — cannot fully verify or partially meets
   - `⚪ N/A` — check does not apply
2. **Findings**: Always include actual observed value
   - Good: "`SnapshotRetentionLimit: 0` — automatic backups disabled"
   - Bad: "Backups not configured"
3. **Critical issues**: Only FAIL items with Priority=High
4. **Recommendations**: Be specific about in-place fixes vs. resource recreation
