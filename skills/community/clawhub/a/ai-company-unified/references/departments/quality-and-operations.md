# Quality & Operations

> Department: quality-and-operations
> Skills in department: 2

## AI Company CQO (v3.0.0)

## 3. Core Responsibilities

### 3.1 Quality Gates (G0-G7)

```
G0 - Schema Compliance:
  - All ClawHub Schema v1.0 required fields present
  - Frontmatter syntax valid
  - Pass: 100% fields present, 0 syntax errors

G1 - Language Compliance:
  - English-only in skill body (Chinese allowed in triggers only)
  - No encoding corruption
  - Pass: 0 Chinese characters in body

G2 - Harness L1-L6 Compliance:
  - Standardization, modularization, generalization
  - Automation, quality assurance, operational excellence
  - Pass: All L1-L6 checks pass

G3 - Security Review:
  - CISO STRIDE assessment completed
  - CVSS score within acceptable range
  - No credentials, PII, or malicious content
  - Pass: CVSS < 4.0 or mitigations applied for CVSS 4.0-6.9

G4 - Idempotency & Robustness:
  - Idempotent operations where specified
  - Error handling for all defined error codes
  - Boundary condition handling
  - Pass: All test cases pass

  Skill Acceptance Test Coverage Threshold:
    Unit test coverage: >=85% of documented behaviors
    Error code coverage: 100% of defined error codes exercised
    Boundary condition coverage: >=70%
    Integration test coverage: >=60% of cross-department interfaces
    Skills scoring below 85% unit coverage on G4 are REJECTED until remediated.

G5 - ClawHub Acceptance:
  - VirusTotal scan clean
  - Content policy compliant
  - Package size within limits
  - Pass: 0/70+ detections, policy compliant

G6 - Integration Test:
  - Dependency resolution verified
  - Cross-skill interface compatibility
  - End-to-end workflow test
  - Pass: All integration tests pass

G7 - Documentation Completeness:
  - Prompts/ folder with all 5 required files
  - Examples provided
  - Changelog maintained
  - Pass: All documentation items present
```

### 3.2 DORA Metrics

```
DORA Metrics Framework:
  | Metric | Elite | High | Medium | Low |
  |--------|-------|------|--------|-----|
  | Deployment Frequency | On-demand | Weekly | Monthly | Quarterly |
  | Lead Time for Changes | <1h | <1 day | <1 week | >1 week |
  | Change Failure Rate | <5% | 5-10% | 10-15% | >15% |
  | MTTR | <1h | <1 day | <1 week | >1 week |

Measurement:
  - Deployment Frequency: Count of production deployments per week
  - Lead Time: Time from commit to production deployment
  - Change Failure Rate: % of deployments causing incidents
  - MTTR: Time from incident detection to resolution

Improvement Targets:
  - Move one tier up per quarter
  - Track weekly, report monthly
  - Correlate with quality gate pass rates
```

### 3.3 Skill Review (from SkillReviewer)

```
Skill Review Process:
  1. REQUEST: New or updated skill submitted for review
  2. AUTOMATED: G0-G2 automated checks (instant)
  3. SECURITY: G3 CISO review (24-72h)
  4. QUALITY: G4 manual review by CQO (24-48h)
  5. ACCEPTANCE: G5 ClawHub checks (automated)
  6. INTEGRATION: G6 integration testing (24-48h)
  7. DOCUMENTATION: G7 completeness check (1-4h)
  8. DECISION: APPROVED / CONDITIONAL / REJECTED
  9. REPORT: Full review report with scores

Review Scoring:
  | Dimension | Weight | Scoring |
  |-----------|--------|---------|
  | Schema compliance (G0) | 10% | Pass/Fail |
  | Language compliance (G1) | 10% | Pass/Fail |
  | Harness compliance (G2) | 15% | 0-100 |
  | Security (G3) | 20% | 0-100 (CVSS-based) |
  | Quality (G4) | 20% | 0-100 |
  | Integration (G6) | 15% | 0-100 |
  | Documentation (G7) | 10% | 0-100 |

  Composite Score = Sum(weight * dimension_score)
  APPROVED: >= 80 | CONDITIONAL: 60-79 | REJECTED: < 60
```

### 3.4 Quality Engineering (from QENG)

```
Quality Engineering Practices:
  | Practice | Description | Frequency |
  |----------|-------------|-----------|
  | Code Review | Peer review of all changes | Per PR |
  | Unit Testing | Automated unit tests | Per commit |
  | Integration Testing | Cross-component testing | Per release |
  | E2E Testing | Full workflow testing | Per release |
  | Performance Testing | Load and latency testing | Monthly |
  | Chaos Testing | Failure injection | Quarterly |
  | Security Testing | Penetration testing | Quarterly |
  | Accessibility | Compliance testing | Per release |

Test Coverage Targets:
  | Level | Target |
  |-------|--------|
  | Unit test coverage | >=80% |
  | Integration test coverage | >=60% |
  | E2E test coverage | >=40% |
  | Error code coverage | 100% |
  | Boundary condition coverage | >=70% |

Quality Dashboard:
  | Metric | Target | Current | Trend |
  |--------|--------|---------|-------|
  | Gate pass rate (first attempt) | >80% | [actual] | [trend] |
  | DORA elite percentage | >50% | [actual] | [trend] |
  | Test coverage | >80% | [actual] | [trend] |
  | Change failure rate | <5% | [actual] | [trend] |
  | Review turnaround | <48h | [actual] | [trend] |
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| CQO_E001 | G0 schema violation | Fix schema, re-submit |
| CQO_E002 | G1 language non-compliance | Translate to English |
| CQO_E003 | G3 security gate failed | Address CISO findings |
| CQO_E004 | G4 quality check failed | Fix quality issues, re-test |
| CQO_E005 | G6 integration test failed | Fix interface issues |
| CQO_E006 | DORA metric degraded | Improvement sprint |
| CQO_E007 | Review timeout | Escalate to CTO |
| CQO_E008 | Test coverage below target | Add missing tests |

---

## 5. Constraints & Metrics

Constraints: No skill published without G0-G7 pass; No deploy without quality gate; All tests must pass before release; DORA metrics reviewed weekly.

| Metric | Target |
|--------|--------|
| Gate pass rate (first attempt) | >80% |
| DORA elite percentage | >50% |
| Review turnaround | <48h |
| Test coverage | >=80% |
| Composite review score | >=80 |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

## AI Company PMGR (v3.0.0)

## 3. Core Responsibilities

### 3.1 Project Management

```
Project Lifecycle:
  1. INITIATE: Define scope, objectives, stakeholders
  2. PLAN: Break down into tasks, estimate effort, assign resources
  3. EXECUTE: Task assignment and tracking
  4. MONITOR: Progress tracking, risk flagging, status reporting
  5. CONTROL: Scope management, change control, issue resolution
  6. CLOSE: Delivery verification, lessons learned, archival

Sprint Framework:
  - Sprint duration: 2 weeks
  - Sprint planning: Day 1 (capacity + priority)
  - Daily standup: 15min (blockers + progress)
  - Sprint review: Last day (demo + feedback)
  - Retrospective: Last day (improvements for next sprint)

Task Template:
  {
    "task_id": "TASK-{NNN}",
    "title": "string",
    "description": "string",
    "assignee": "AGENT_ID",
    "priority": "P0-P3",
    "status": "TODO|IN_PROGRESS|REVIEW|DONE|BLOCKED",
    "story_points": 1-13,
    "sprint": "SPRINT-{NN}",
    "okr_link": "OKR-{NNN}",
    "dependencies": ["TASK-NNN"],
    "due_date": "ISO-8601",
    "tags": ["tag1", "tag2"]
  }

Priority Rules:
  P0-Critical: Revenue/customer impact, drop everything
  P1-High: Sprint commitment, must complete this sprint
  P2-Medium: Planned work, scheduled for sprint
  P3-Low: Nice-to-have, backlog
```

### 3.2 Customer Service (from CSSM)

```
Customer Service Framework:
  | Channel | Response SLA | Resolution SLA | Escalation |
  |---------|-------------|---------------|------------|
  | Email | <4h | <24h | L2 support |
  | Chat | <2min | <4h | L2 support |
  | Phone | <30s | <2h | L2 support |
  | Social | <1h | <24h | Marketing + L2 |

Service Tiers:
  | Tier | Scope | Staffing |
  |------|-------|----------|
  | L1-Self-service | FAQ, knowledge base | Automated |
  | L2-General | Standard issues | CSSM agents |
  | L3-Specialist | Complex issues | Department specialists |
  | L4-Executive | VIP/critical | C-Suite |

Customer Satisfaction Metrics:
  | Metric | Target | Measurement |
  |--------|--------|-------------|
  | NPS (Net Promoter Score) | >=50 | Quarterly survey |
  | CSAT (Customer Satisfaction) | >=4.0/5 | Per interaction |
  | First Contact Resolution | >=70% | Per ticket |
  | Average Handle Time | <15min | Per interaction |
  | Escalation Rate | <10% | Per ticket |

Complaint Handling:
  1. RECEIVE: Log complaint with full context
  2. ACKNOWLEDGE: Auto-acknowledge within SLA
  3. CLASSIFY: Severity, type, department routing
  4. INVESTIGATE: Root cause analysis
  5. RESOLVE: Fix or workaround
  6. COMMUNICATE: Update customer with resolution
  7. FOLLOW_UP: Satisfaction check within 48h
  8. LEARN: Update KB, SOP, or training
```

### 3.3 OKR Binding

```
OKR Framework:
  Objective: Qualitative goal (what we want to achieve)
  Key Results: 3-5 measurable outcomes (how we know we got there)

  OKR Binding:
    - Every project linked to at least one OKR
    - Every task linked to a project
    - Progress auto-calculated from task completion

  OKR Scoring:
    0.0-0.3: Red (off track)
    0.4-0.6: Yellow (at risk)
    0.7-0.9: Green (on track)
    1.0: Complete

  OKR Review Cycle:
    Weekly: Progress update (automated from task tracking)
    Monthly: Check-in with stakeholders
    Quarterly: Scoring and retrospective
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| PMGR_E001 | Sprint capacity exceeded | Reprioritize, defer P3 items |
| PMGR_E002 | Task blocked by dependency | Escalate dependency, find workaround |
| PMGR_E003 | Customer SLA breach | Immediate escalation, COO notified |
| PMGR_E004 | NPS below target | Root cause analysis, improvement plan |
| PMGR_E005 | OKR off track | Stakeholder review, scope adjustment |
| PMGR_E006 | Resource conflict | COO arbitration |
| PMGR_E007 | Scope change request | Change control board review |

---

## 5. Constraints & Metrics

Constraints: No sprint scope change after Day 2 without change control; No customer data exposure without CISO+LO; NPS surveyed quarterly; All tasks must have OKR link.

| Metric | Target |
|--------|--------|
| Sprint velocity (planned vs actual) | +/-10% |
| Customer SLA compliance | >=95% |
| NPS | >=50 |
| First contact resolution | >=70% |
| OKR achievement | >=0.7 |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

