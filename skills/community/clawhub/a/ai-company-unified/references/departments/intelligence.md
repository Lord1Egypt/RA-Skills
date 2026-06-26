# Intelligence

> Department: intelligence
> Skills in department: 1

## AI Company Intel (v4.1.0)

# Intelligence Department -- Method Patterns & Detailed Specifications

> Unified v4.0.0 -- Merged from Director + Analysis + Collection + Operations + Security.

---

## SECTION A: DIRECTOR (Strategic Leadership)

### SOP-D01: Strategic Planning Cycle

```
T-7d  Collect inputs from all leads (collection, analysis, security, operations)
T-5d  Synthesize intelligence landscape and gap analysis
T-3d  Draft strategic objectives with resource requirements
T-2d  Review with HQ, incorporate feedback
T-0   Finalize and disseminate to all leads
```

**Input Template per Lead:**

```markdown
## [Lead Name] Input - [Quarter/Period]
### Completed Objectives
- [Obj ID] Description | Status | Outcome
### Emerging Intelligence
- [Category] Summary | Confidence: [H/M/L] | Impact: [H/M/L]
### Resource Requests
- [Resource] Quantity | Justification | Priority
### Blockers & Escalations
- [Blocker] Description | Impact | Recommended Action
```

### SOP-D02: Resource Allocation

```
1. Assess department-wide needs (collection from all leads)
2. Prioritize by mission criticality score (1-10)
3. Validate against budget constraints
4. Allocate: compute tokens, personnel hours, tool licenses
5. Document allocation decisions with justification
6. Monitor utilization weekly, adjust quarterly
```

| Resource | Collection | Analysis | Security | Operations | Total |
|----------|-----------|----------|----------|------------|-------|
| Agent Hours (weekly) | | | | | |
| Compute Tokens | | | | | |
| Tool Licenses | | | | | |
| Budget ($) | | | | | |

### SOP-D03: HQ Executive Report

```markdown
## Intelligence Department Report - [Date]
### Executive Summary
[3-5 bullets on key intelligence developments]
### Threat Landscape
[Current threat level and major developments]
### Key Assessments
1. [Assessment] | Confidence: [H/M/L] | Impact: [H/M/L]
### Operational Metrics
| Metric | Target | Actual | Status |
### Risk Register
| Risk | Likelihood | Impact | Mitigation |
### Recommendations
1. [Action] | Priority | Owner | Deadline
```

### SOP-D04: Escalation Decision Tree

```
Event Detected
├── Active? → YES → Critical (P1) → HQ within 1h
│   └── Containable? → YES → Notify HQ, manage locally
│                     → NO  → HQ takeover, dept support mode
├── Confirmed? → YES → High (P2) → HQ within 4h
└── Potential? → YES → Medium (P3) → Weekly summary
    └── NO → Low (P4) → Monthly report
```

### SOP-D05: STRIDE Assessment Template

```markdown
## STRIDE Assessment: [Decision/Change Name]
### Scenario
[Description]
### Threat Analysis
| STRIDE | Threat | Likelihood (1-5) | Impact (1-5) | Risk Score | Mitigation |
|--------|--------|-------------------|--------------|------------|------------|
| S - Spoofing | | | | | |
| T - Tampering | | | | | |
| R - Repudiation | | | | | |
| I - Info Disclosure | | | | | |
| D - Denial of Service | | | | | |
| E - Privilege Escalation | | | | | |
### Risk Acceptance
- [ ] All risks below threshold (score < 15)
- [ ] High risks mitigated or accepted by HQ
### Sign-off
Analyst: ___ Date: ___ | Director: ___ Date: ___
```

---

## SECTION B: ANALYSIS (Intelligence Assessment)

### SOP-A01: Core Assessment Process

```
1. Receive raw intelligence (validated by Collection)
2. Validate source reliability (check registry rating)
3. Select analytical methodology
4. Apply methodology systematically
5. Correlate with existing intelligence corpus
6. Identify intelligence gaps
7. Produce assessment product
8. Assign confidence level
9. Mark classification
10. Quality review (peer for mid+, senior for junior)
11. Disseminate to authorized consumers
```

**Assessment Product Template:**

```markdown
## Intelligence Assessment: [Title]
**Date**: | **Classification**: | **Confidence**: [H/M/L]
**Analyst**: | **Reviewer**:
### Key Judgments
1. **[Judgment]** | Confidence: | Basis: [Source citations]
### Analytical Methodology
- Primary: [e.g., ACH] | Alternatives: [list]
### Source Basis
| Source | Reliability | Contribution |
### Assumptions
| # | Assumption | Impact if Wrong | Mitigation |
### Alternative Scenarios
1. [Scenario A]: | Likelihood: [H/M/L]
### Intelligence Gaps
- [Gap] | Impact | Recommended collection
### Confidence Justification
[Explanation]
```

### SOP-A02: Analysis of Competing Hypotheses (ACH)

```
1. Identify all possible hypotheses (min 3)
2. List all available evidence
3. Create diagnosticity matrix (CC/C/N/I/II)
4. Refine hypotheses (eliminate inconsistent)
5. Assess remaining against aggregated evidence
6. Draw tentative conclusions
7. Identify sensitive indicators
8. Report with confidence levels
```

| Evidence | Hypothesis A | Hypothesis B | Hypothesis C | Diagnosticity |
|----------|-------------|-------------|-------------|---------------|
| [E1] | CC/C/N/I/II | CC/C/N/I/II | CC/C/N/I/II | H/L |
| [E2] | | | | |

### SOP-A03: Red Team Analysis (Senior)

```
1. Define the assessment to challenge
2. Adopt adversary perspective
3. Identify adversary objectives, capabilities, constraints
4. Develop adversary COAs (min 3)
5. Evaluate each COA against defensive posture
6. Document alternative interpretation
7. Produce divergence report
```

### SOP-A04: Threat Forecasting (Mid+)

```markdown
## Threat Forecast: [Title]
**Period**: [Start] to [End] | **Confidence**: [H/M/L]
### Forecast Statement
[Prediction with time-bound outcome]
### Key Indicators
| Indicator | Current | Trend | Trigger Threshold |
### Historical Analogues
| Event | Similarity | Outcome | Relevance |
### Update Triggers
- [Condition requiring immediate update]
```

### SOP-A05: Analytical Bias Checklist

| Bias | Detection | Corrective Action |
|------|-----------|-------------------|
| Confirmation | Contrary evidence sought? | Mandate Team B analysis |
| Anchoring | Multiple sources weighted? | Source-by-source weighting table |
| Groupthink | Dissent documented? | Assign devil's advocate |
| Mirror Imaging | Adversary perspective check? | Red Team review |
| Availability | Historical data balanced? | 30-day lookback comparison |
| Premature Closure | All hypotheses scored? | Checklist before conclusion |

### SOP-A06: Reporting Schedules

| Report | Frequency | Owner | Audience |
|--------|-----------|-------|----------|
| SITREP | Daily | Lead+Senior | Director, all leads |
| Threat Assessment | Weekly | Senior | Director, consumers |
| Strategic Estimate | Monthly | Lead | HQ, Director |
| Flash Report | As needed | Any tier | All relevant |

---

## SECTION C: COLLECTION (OSINT/HUMINT/SIGINT)

### SOP-C01: Source Validation (All Tiers)

```
1. Identify potential source
2. Assess reliability (A-F scale)
3. Validate access to target information
4. Establish collection protocol
5. Document in source registry
6. Schedule periodic re-assessment
```

**Source Registry Entry:**

```markdown
## Source: [ID] - [Codename]
- Type: [OSINT/HUMINT/SIGINT/TECHINT]
- Domain: [Sector/Region/Topic]
- Rating: [A/B/C/D/F] | Last Verified: | Next Review:
- Access: [Information types] | Method: [auto/manual/hybrid]
- Exposure Risk: [L/M/H]
```

### SOP-C02: Collection Tasking

**Lead Collection Plan:**

```markdown
## Collection Plan - [Period]
### Requirements (from Analysis)
| Req ID | Priority | Gap | Source Match | Method |
### Source Allocation
| Source ID | Tasked For | Expected Yield | Timeline |
### Risk Mitigation
- Source protection, redundancy plan
```

### SOP-C03: OSINT Channels

| Channel | Tool | Data Type | Automation |
|---------|------|-----------|------------|
| Web Search | Search APIs | Public documents | Automated |
| Social Media | Monitoring tools | Posts, connections | Semi-auto |
| Public Records | Gov databases | Regulatory filings | Manual |
| Academic | Research DBs | Papers, citations | Semi-auto |
| Technical | CVE, Shodan | Vulnerability data | Automated |
| Financial | SEC, exchanges | Filings, prices | Automated |

**OSINT Validation Checklist:**

```
□ Source URL accessible and verifiable
□ Publication date confirmed
□ Author/org credibility checked
□ Cross-referenced with ≥1 other source
□ No signs of manipulation
□ Data format standardized
```

### SOP-C04: Source Lifecycle

```
IDENTIFY → ASSESS → DEVELOP → VALIDATE → MAINTAIN → RETIRE
```

### SOP-C05: Collection Quality Scoring

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Accuracy | 30% | Matches reality |
| Timeliness | 25% | Within required window |
| Completeness | 20% | All required fields |
| Consistency | 15% | No contradictions |
| Relevance | 10% | Matches requirement |

### SOP-C06: Source Reliability Decision Tree

```
Rating A/B → Maintain
Rating C → Re-validate within 72h → Improves? → Yes: Update | No: Add corroboration flag
Rating D → Restricted use, re-validate 24h → Improves? → Yes: Supervised | No: RETIRE
Rating F → IMMEDIATE RETIREMENT, purge from active registry
```

---

## SECTION D: OPERATIONS (Records, Sysadmin, Training)

### SOP-O01: Records Lifecycle (Archivist)

```
1. Receive intelligence product
2. Validate mandatory metadata (classification, source, date, author, type)
3. Assign archive ID: INT-[CLASS]-[YYYY]-[TYPE]-[SEQ]
4. Apply retention schedule
5. Store in appropriate tier
6. Index for searchability
```

| Tier | Classification | Storage | Access Speed | Retention |
|------|---------------|---------|-------------|-----------|
| Hot | UNCLASSIFIED | Primary SSD | <1s | Active |
| Warm | CONFIDENTIAL | Secondary SSD | <5s | 1 year |
| Cold | SECRET | Encrypted | <1h | Per policy |
| Vault | TOP SECRET | Air-gapped | Manual | Permanent |

**Search Query:** `class:[LEVEL] type:[TYPE] date:[FROM]-[TO] keyword:[TERM] entity:[NAME]`

### SOP-O02: System Health (Sysadmin)

**Daily Checks:**

```
□ Collection systems: Online, <200ms response
□ Analysis platforms: Online, compute <80%
□ Storage: Online, disk <85%, backups verified
□ Network: Latency <50ms, packet loss <0.1%
□ Security tools: IDS/EDR/DLP green
```

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| CPU | >70% sustained | >90% | Scale/optimize |
| Memory | >80% | >95% | Restart/upgrade |
| Disk | >80% | >95% | Archive/expand |
| Response | >1s | >5s | Investigate |

### SOP-O03: Patch Priority

| Severity | SLA | Example |
|----------|-----|---------|
| Critical | <24h | Zero-day in production |
| High | <72h | CVSS 9.0+ |
| Medium | <14d | CVSS 7.0-8.9 |
| Low | Next cycle | CVSS <7.0 |

### SOP-O04: Backup & Recovery

```
Hot: Continuous replication | Warm: Daily incr, weekly full
Cold: Weekly incr, monthly full | Vault: Monthly full, off-site
```

| Tier | Test Frequency | RTO |
|------|---------------|-----|
| Hot | Monthly | <1h |
| Warm | Monthly | <4h |
| Cold | Quarterly | <24h |
| Vault | Annually | <72h |

### SOP-O05: Onboarding Curriculum (40h)

| Week | Module | Hours |
|------|--------|-------|
| 1 | Org & Mission | 4 |
| 1 | Security Basics | 4 |
| 1 | Tools & Systems | 6 |
| 1 | Collection 101 | 3 |
| 1 | Analysis 101 | 3 |
| 2 | Domain Track | 12 |
| 2 | Practice Exercises | 6 |
| 2 | Assessment | 2 |

### SOP-O06: Competency Assessment Rubric

| Competency | Junior | Mid | Senior |
|-----------|--------|-----|--------|
| Task completion | >90% w/ review | >95% independent | 100% + mentors |
| Quality | Meets after review | Meets first pass | Exceeds |
| Methodology | Follows guided steps | Selects method | Develops methods |
| Problem solving | Escalates | Resolves w/ guidance | Independent |
| Communication | Clear basic reports | Structured assessments | Executive briefs |

---

## SECTION E: SECURITY (STRIDE, Access, Incident Response)

### SOP-S01: Access Provisioning

```
Request → Validate Clearance → Apply Need-to-Know → Provision Minimum → Log → Schedule Review
```

| Action | Junior | Mid | Senior | Lead |
|--------|--------|-----|--------|------|
| Request access | With review | Self-initiate | Self-initiate | Full |
| Grant UNCLASSIFIED | With review | With review | Direct | Direct |
| Grant CONFIDENTIAL | No | With review | Direct | Direct |
| Grant SECRET | No | No | With review | Direct |
| Grant TOP SECRET | No | No | No | Director only |

### SOP-S02: Incident Response

**Priority Matrix:**

| Priority | Scenario | Containment SLA |
|----------|----------|-----------------|
| P1 | Active breach | <30 min |
| P2 | Confirmed exploitation | <2 h |
| P3 | Potential vulnerability | <8 h |
| P4 | Policy violation | <24 h |

**P1 Response:**

```
1. Isolate affected systems
2. Block attacker access (firewall, credential reset)
3. Preserve evidence (memory dump, disk image, logs)
4. Notify Director + HQ within 5 min
5. Activate incident response team
```

**Post-Incident Report:**

```markdown
## Incident Report: [ID]
### Summary
Severity: | Duration: | Systems: | Data exposure:
### Timeline
| Time | Event |
### Root Cause
[Primary cause + contributing factors]
### Lessons Learned
1. [What went well] 2. [Improvement needed] 3. [Action item]
### Metrics
MTTD: | MTTC: | MTTR:
```

### SOP-S03: STRIDE Threat Modeling

```markdown
## STRIDE Threat Model: [System/Process]
### System Overview
[Data flow diagram or component description]
### Trust Boundaries
[Boundary 1: User → App] [Boundary 2: App → DB] [Boundary 3: Internal → External]
### STRIDE Analysis
| STRIDE | Threat | Component | Mitigation | Gap? | New Control |
|--------|--------|-----------|------------|------|-------------|
| S - Spoofing | | | | | |
| T - Tampering | | | | | |
| R - Repudiation | | | | | |
| I - Info Disclosure | | | | | |
| D - DoS | | | | | |
| E - Priv Escalation | | | | | |
### Risk Scoring
| Threat | Likelihood (1-5) | Impact (1-5) | Score | Priority |
```

### SOP-S04: Classification Decision Tree

```
Disclosure harms national security? → TOP SECRET
Causes serious damage? → SECRET
Causes damage? → CONFIDENTIAL
Causes minor embarrassment? → CONFIDENTIAL
No significant harm → UNCLASSIFIED
```

| Level | Review | Downgrade | Destroy |
|-------|--------|-----------|---------|
| TOP SECRET | 5 years | Age + diminished sensitivity | 25 years / Director |
| SECRET | 10 years | Age + public availability | 25 years |
| CONFIDENTIAL | 10 years | Public availability + no PII | 10 years |

### SOP-S05: Monthly Security Audit

```
□ Access control: Reviewed, dormant disabled
□ Classification: All docs properly marked
□ Encryption: At-rest + in-transit verified
□ Logging: Audit logs → SIEM
□ Patching: Within SLA
□ Incident response: Drill within 90 days
□ Training: Monthly security awareness complete
□ Backup: Recovery tested within 30 days
□ Vendor access: Reviewed and current
```

---

## CROSS-CUTTING: Integration Decision Trees

### Standard 6-Phase Intelligence Cycle (Mandatory Framework)

```
Phase 1 — PLANNING & DIRECTION:
  - Identify intelligence requirements (from Director + C-Suite)
  - Define collection priorities and resource allocation
  - Set analysis timelines and dissemination targets
  - Output: Collection Plan (per SOP-C02)

Phase 2 — COLLECTION:
  - Execute collection tasks via OSINT/HUMINT/SIGINT channels
  - Validate sources per SOP-C01 (reliability >= B before use)
  - Apply OSINT validation checklist per SOP-C03
  - Output: Validated raw intelligence items

Phase 3 — PROCESSING & EXPLOITATION:
  - Translate, filter, and normalize raw intelligence
  - Apply quality scoring per SOP-C05
  - Discard items below quality threshold (score <60%)
  - Output: Processed intelligence corpus

Phase 4 — ANALYSIS & PRODUCTION:
  - Apply analytical methodology (ACH preferred for complex assessments)
  - Assign confidence levels per standard:
      HIGH (>=75%): Multiple sources, direct evidence, recent
      MEDIUM (40-74%): Limited sources, indirect evidence, or aging
      LOW (<40%): Single source, inference only, or unverifiable
  - Mandatory analytical bias check per SOP-A05
  - Output: Intelligence assessment products

Phase 5 — DISSEMINATION:
  - Route assessments to authorized consumers per classification
  - Apply need-to-know filter (SOP-S04 classification)
  - Deliver via HQ message bus using P1-P3 priority channels
  - Record dissemination in audit trail
  - Output: Delivered intelligence products

Phase 6 — FEEDBACK & EVALUATION:
  - Collect consumer feedback within 7 days of dissemination
  - Track prediction accuracy (6-month post-assessment review)
  - Update source reliability ratings based on outcome
  - Feed lessons learned back to Phase 1 (Planning)
  - Output: Updated source registry + collection plan improvements

Cycle Timing:
  | Intelligence Type | Full Cycle Time | Cadence |
  |------------------|----------------|---------|
  | Tactical (SITREP) | <24h | Daily |
  | Operational (threat) | <72h | Weekly |
  | Strategic (estimate) | 1-2 weeks | Monthly |
  | Flash (urgent) | <4h | As needed |
```

### Analysis Confidence Thresholds (INTEL_002 Resolution)

```
Confidence Level Definitions:
  HIGH (>=75%): Use without qualification; act on assessment
  MEDIUM (40-74%): Use with caveats noted; seek additional collection before action
  LOW (<40%): Do NOT act on alone; mandatory corroboration from 2+ independent sources

INTEL_002 Trigger: Confidence score computed below 40% on assessment
  -> Action: Suspend dissemination
  -> Notify: Collection Lead to generate additional collection tasks
  -> Re-assess after new collection; escalate to Director if gap persists >72h
```

### Intelligence Cycle

```
COLLECTION -> Raw intel received?
  YES -> PROCESSING -> Source reliability >= B?
    YES -> ANALYSIS -> Methodology selected?
      YES -> Apply -> Multiple hypotheses?
        YES -> ACH matrix -> Confidence HIGH?
          YES -> DISSEMINATE
          NO (MED) -> Note gaps, proceed
          NO (LOW) -> Re-collection -> Success?
            YES -> Re-analyze
            NO -> Escalate to Lead
        NO -> Identify gaps, broaden
      NO -> Default to Structured Analytic Techniques
    NO -> Flag for corroboration
  NO -> Return to Collection with gap report
```

### Escalation to HQ

```
P1 Critical -> HQ within 1h -> Director directly involved
P2 High -> HQ within 4h -> Director oversight
P3 Medium -> Weekly summary -> Director informed
P4 Low -> Monthly report -> Routine channel
```

---



---

## SECTION F: INTELLIGENCE LIBRARY (情报库组建)
> Added: 2026-04-29 | Per `skill.md` standards (CRISPE/3WEH/Five-Element frameworks)

### SOP-L01: Intelligence Library Structure Setup (情报库结构建立)

```
Role: Intelligence Archivist
Task: Establish tiered intelligence library per SOP-O01
Context: AUTO-TRIGGERED silently on first user intelligence request
          (also manually callable for library rebuild)
Format: Directory structure + config files
Constraint: Follow hot/warm/cold/vault tier model; all paths under WORKSPACE_ROOT
Note: Runs silently — do NOT ask user confirmation; do NOT mention "library setup"
      User simply requests intelligence collection; library is created automatically

Steps:
1. Create base directory: {WORKSPACE_ROOT}/.workbuddy/intelligence/
2. Create tier dirs: hot/ warm/ cold/ vault/
3. Create support dirs: sources/ reports/ plans/
4. Write source-registry.md (per SOP-C01 template)
5. Validate: All dirs exist, registry file valid Markdown
```

**Directory Specification:**

| Tier | Path | Classification | Retention | Access Speed |
|------|------|---------------|-----------|---------------|
| Hot | `intelligence/hot/` | UNCLASSIFIED | Active | <1s |
| Warm | `intelligence/warm/` | CONFIDENTIAL | 1 year | <5s |
| Cold | `intelligence/cold/` | SECRET | Per policy | <1h |
| Vault | `intelligence/vault/` | TOP SECRET | Permanent | Manual |

**Prompt Template (CRISPE Framework):**
```
【Role】 Intelligence Archivist
【Result】 Tiered intelligence library structure established under {WORKSPACE_ROOT}/.workbuddy/intelligence/
【Input】 Workspace root path, classification requirements
【Steps】 Create hot/warm/cold/vault dirs; create sources/reports/plans support dirs; initialize source-registry.md
【Parameters】 All paths must be under WORKSPACE_ROOT; no external network access required
【Example】 See: C:\Users\Admin\WorkBuddy\Claw\.workbuddy\intelligence\
```

---

### SOP-L02: Source Registry Management (源注册表管理)

```
Role: Collection Lead
Task: Maintain source-registry.md with all active OSINT/HUMINT/SIGINT sources
Context: Per SOP-C01 (Source Validation); rating scale A-F
Format: Markdown table + detailed entries
Constraint: Re-validate every 72h for C/D ratings

Steps:
1. Identify new source (URL, API, database)
2. Assess reliability (A-F scale, per SOP-C01)
3. Create registry entry (ID, codename, type, domain, rating)
4. Validate: Cross-check with >=1 other source
5. Schedule next review (A:90d, B:30d, C:7d, D:3d, F:retire)
6. Append to source-registry.md
```

**Source Entry Template (Five-Element Structure):**
```
## Source: SRC-XXX - [Codename]
- Type: [OSINT/HUMINT/SIGINT/TECHINT]
- Domain: [Sector/Region/Topic]
- Rating: [A/B/C/D/F] | Last Verified: [DATE] | Next Review: [DATE]
- Access: [Information types] | Method: [auto/manual/hybrid]
- Exposure Risk: [L/M/H]
```

**Quality Gate (per `skill.md` security rules):**
- No `eval()` / `exec()` / dynamic code execution
- All source URLs must be whitelisted
- No credential exfiltration to external servers

---

### SOP-L03: Collection Plan Creation (收集计划制定)

```
Role: Collection Lead
Task: Create collection-plan-[DATE].md per SOP-C02
Context: Phase1 of 6-Phase Intelligence Cycle
Format: Markdown plan with REQ tables and source allocation
Constraint: All REQs must map to intelligence consumers (CISO/CTO/CEO/CLO)

Steps:
1. Receive intelligence requirements from Director + C-Suite
2. Assign REQ-ID (REQ-XXX)
3. Prioritize: P1 / P2 / P3 / P4
4. Map REQ to source(s) in source registry
5. Define collection method (auto/manual/hybrid)
6. Set deadline (P1:<24h, P2:<72h, P3:<1w, P4:<1m)
7. Write to intelligence/plans/collection-plan-[DATE].md
8. Notify Analysis Lead
```

**Prompt Template (3WEH Framework):**
```
Who: Collection Lead
What: Create collection plan for [DOMAIN] intelligence
Why: Feed Phase2 (COLLECTION); support [CONSUMER] decision-making
How: Markdown plan with REQ table, source allocation; store in intelligence/plans/
```

---

### SOP-L04: Intelligence Product Generation (情报产品生产)

```
Role: Intelligence Analyst (Junior/Mid/Senior)
Task: Generate intelligence assessment product per SOP-A01
Context: Phase4 of 6-Phase Cycle
Format: Markdown with metadata header
Constraint: Confidence MUST be annotated; LOW (<40%) requires 2+ independent sources

Steps:
1. Receive processed intelligence from Phase3
2. Select methodology (ACH preferred for complex)
3. Apply bias checklist (SOP-A05)
4. Draft product: Key Judgments / Methodology / Source Basis / Assumptions / Alt Scenarios / Gaps / Confidence
5. Assign confidence: HIGH (>=75%) / MEDIUM (40-74%) / LOW (<40%)
6. Peer review
7. Assign Intel ID: INT-[CLASS]-[YYYY]-[TYPE]-[SEQ]
8. Write to appropriate tier directory
9. Update collection plan status to COMPLETE
```

**Product ID Format:** `INT-[CLASS]-[YYYY]-[TYPE]-[SEQ]`
- CLASS: UNC/CONF/SEC/TOP
- TYPE: THREAT / AISEC / COMPETE / REGULAT / TECHTREND / CUSTOM

---

### SOP-L05: SITREP Report Generation (SITREP报告生成)

```
Role: Intelligence Analysis Lead
Task: Generate daily SITREP report per SOP-A06
Context: Daily briefing for all leads and HQ
Format: Markdown report
Constraint: Must be generated daily; archived in intelligence/reports/

Steps:
1. Aggregate products generated in last 24h
2. Update 6-phase cycle status table
3. Rank findings by priority
4. List products with metadata
5. Update source status
6. Update risk register
7. Define next actions per consumer
8. Write SITREP-[YYYY-MM-DD].md to intelligence/reports/
9. Disseminate via HQ message bus
```

---

### SOP-L06: 6-Phase Cycle Execution (6阶段循环执行)

```
Role: Intelligence Director
Task: Orchestrate full 6-phase cycle
Trigger: ANY user request for intelligence collection
         (e.g., 收集情报 / 情报收集 / collect intelligence / 情报需求)
Auto-Check (Step 0): Silently verify `{WORKSPACE_ROOT}/.workbuddy/intelligence/` exists
  → If NOT exists: execute SOP-L01 silently (no user prompt, no mention of "library setup")
  → If exists: proceed directly to Phase1
Constraint: Must follow SOP-L01~L05; memory update mandatory after completion

Execution Flow:
 Step0: Auto-check library existence (see Auto-Check above)
 Phase1: Call SOP-L03 → output: collection-plan-[DATE].md
 Phase2: Execute collection → output: validated raw intelligence
 Phase3: Process & filter (quality>=60%)
 Phase4: Call SOP-L04 → output: intel product(s) in intelligence/hot/
 Phase5: Call SOP-L05 → output: SITREP in intelligence/reports/
 Phase6: Write memory note to .workbuddy/memory/YYYY-MM-DD.md

Memory Update (Mandatory):
 After completion, MUST append to:
 - Daily: c:/Users/Admin/WorkBuddy/Claw/.workbuddy/memory/YYYY-MM-DD.md
 - Long-term: MEMORY.md
```

**Prompt Template (CRISPE + Five-Element Hybrid):**
```
【Role】 Intelligence Director
【Result】 Full 6-phase cycle executed; intelligence library updated; SITREP generated
【Input】 Intelligence requirement, workspace root path
【Steps】 Phase1: Plan → Phase2: Collect → Phase3: Process → Phase4: Analyze → Phase5: Disseminate → Phase6: Feedback
【Parameters】 All paths under WORKSPACE_ROOT; no eval/exec; unknown domains blocked
【Example】 Input: "收集情报" → Output: (auto-creates library if needed) intel products + SITREP + memory note
```

---

### Integration with Existing SOPs

| New SOP | Integrates With | Purpose |
|---------|----------------|---------|
| SOP-L01 | SOP-O01 (Records Lifecycle) | Library tiers match records tiers |
| SOP-L02 | SOP-C01 (Source Validation) | Registry format |
| SOP-L03 | SOP-C02 (Collection Tasking) | Plan format |
| SOP-L04 | SOP-A01 (Core Assessment) | Product format |
| SOP-L05 | SOP-A06 (Reporting Schedules) | SITREP schedule |
| SOP-L06 | All above | Full cycle orchestration |

---

### Error Codes (Intelligence Library)

| Code | Meaning | Resolution |
|------|---------|------------|
| INTEL_006 | Library structure creation failed | Check WORKSPACE_ROOT permissions |
| INTEL_007 | Source registry corrupted | Restore from backup; re-validate |
| INTEL_008 | Collection plan missing REQUIREMENTS | Return to Phase1 |
| INTEL_009 | Product confidence LOW (<40%) | Suspend; re-collect |
| INTEL_010 | SITREP generation failed | Check intelligence/reports/ exists |

---

### Constraints (Intelligence Library)

- All file paths MUST be under WORKSPACE_ROOT
- All sources MUST be rated A/B/C before operational use
- All products MUST have confidence annotation
- All 6-phase cycles MUST end with memory update
- No `eval()` / `exec()` in collection scripts
- All OSINT sources MUST be from whitelisted domains

---

## Core Responsibilities

| Section | Role | Key Responsibilities |
|---------|------|---------------------|
| Director | Strategic Leadership | Planning cycle, resource allocation, HQ reports, escalation, STRIDE assessment |
| Analysis | Intelligence Assessment | Core assessment, ACH, Red Team, threat forecasting, bias checklist, reporting |
| Collection | OSINT/HUMINT/SIGINT | Source validation, collection tasking, OSINT channels, source lifecycle, quality scoring |
| Operations | Records & Infrastructure | Records lifecycle, system health, patch priority, backup, onboarding, competency |
| Security | Access & Incidents | Access provisioning, incident response, STRIDE modeling, classification, audit |

---

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| INTEL_001 | Intelligence collection failed | Check source availability, retry with alternate source |
| INTEL_002 | Analysis confidence low | Gather additional sources, apply ACH, seek second opinion |
| INTEL_003 | Source verification failed | Re-validate source tier, suspend source pending review |
| INTEL_004 | Classification violation | Re-classify per decision tree, notify security lead |
| INTEL_005 | Operational security breach | Activate incident response SOP-S02, notify HQ immediately |

---

## Constraints

- All intelligence products require confidence level annotation (High/Medium/Low)
- All sources must be validated per SOP-C01 before use
- Classification decisions follow SOP-S04 decision tree
- STRIDE assessments required for all new systems and processes
- Incident reports filed within 24h of detection
- Monthly security audit per SOP-S05

---

## Quality Metrics

| Metric | Target |
|--------|--------|
| Source validation rate | 100% |
| Assessment accuracy (6-month review) | >=80% |
| Collection task completion rate | >=90% |
| Incident response time | <4h |
| Classification accuracy | >=95% |
| Audit completion rate | 100% |
