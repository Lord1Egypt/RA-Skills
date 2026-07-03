# B2B Product Backlog & Version Planning Template

## I. Backlog Management

### 1.1 Backlog Excel Field Standards

Use the `xlsx` skill to generate a backlog Excel file with the following fields:

| Field | Type | Description |
|------|------|------|
| Requirement ID | REQ-YYYY-Seq | Unique identifier, e.g. REQ-2026-0001 |
| Requirement Title | Text | One-sentence description |
| Requirement Source | Enum | Customer Feedback / Sales Feedback / Internal Planning / Competitive Benchmarking / User Research / Strategic Requirement |
| Source Details | Text | Specific customer/person/scenario of origin |
| Customer Importance | Enum | KA Strategic / High Value / Medium / Standard |
| Involved Roles | Multi-select | Target roles using this feature |
| Requirement Type | Enum | New Feature / Feature Optimization / Bug Fix / Technical Optimization / UX Optimization |
| Requirement Stage | Enum | Raw / Clarified / Solution Design / Pending Review / Scheduled / In Development / Go Live |
| KANO Classification | Enum | Basic / Performance / Excitement / Indifferent |
| Priority | P0/P1/P2/P3 | P0=Must Do (This Version), P1=Should Do (Next Version), P2=Could Do (Future), P3=Won't Do |
| Priority Score | 0-100 | Auto-calculated via weighted scoring |
| Related Feature Module | Enum | e.g. Procurement Management / Approval Workflow / Permission Management |
| Estimated Effort | Person-Days | Rough estimate |
| Requirement Submitted Date | Date | |
| Expected Go Live Date | Date | Customer expectation (if any) |
| Committed Customer | Text | Customer committed to delivery (if any), blank = not committed |
| Review Conclusion | Text | Approved / Rejected / Pending Confirmation |
| Notes | Text | Supplementary information |

### 1.2 Backlog Maintenance Rules

```
1. Requirements must be entered into the backlog within 24 hours of submission
2. Sync backlog status to product and dev teams every Monday
3. Monthly cleanup of long-stalled requirements (mark as P3 or close)
4. Customer-committed requirements must be flagged, must not be lost
5. Requirement IDs, once assigned, are never reused
```

---

## II. Version Planning

### 2.1 Version Planning Template

```
Version: [Product Name] V[Version Number]
Codename: [Optional, internal codename for the version]
Target Release Date: YYYY-MM-DD

## Version Goal
[One sentence describing the core goal of this version, no more than 20 words]

## Version Key Metrics
| Metric | Current Value | Target Value |
|------|--------|--------|
| | | |

## Requirement Scope

### P0 - Must Deliver (Core of This Version)
| Req ID | Title | Owner | Effort | Status | Risk |
|--------|---------|--------|--------|------|------|
| | | | | | |

### P1 - Should Deliver (If Bandwidth Allows)
| Req ID | Title | Owner | Effort | Status |
|--------|---------|--------|--------|------|
| | | | | |

### P2 - Next Version (Explicitly Excluded from This Version)
| Req ID | Title | Reason |
|--------|---------|------|
| | | |

## Version Cadence
| Phase | Start | End | Description |
|------|------|------|------|
| Requirement Freeze | | | After this, requirements only shrink, never grow |
| Development Start | | | |
| Code Freeze | | | After this, only bug fixes |
| QA Complete | | | |
| Go Live Release | | | |

## Risks & Blockers
| Risk | Likelihood | Impact | Response |
|------|--------|------|------|
| | | | |
```

### 2.2 Product Roadmap (Now-Next-Later Framework)

```
Now (This Quarter):
├── [Core Feature 1] — Solves [Problem], Targets [Metric]
├── [Core Feature 2] — Solves [Problem], Targets [Metric]
└── [UX Optimization]   — Solves [Problem], Targets [Metric]

Next (Next Quarter):
├── [Feature 3]
├── [Feature 4]
└── [Feature 5]

Later (Long-Term):
├── [Feature 6] — Depends on [Condition]
├── [Feature 7] — Pending Market Verification
└── [Feature 8] — Pending Tech Research
```

---

## III. Priority Score Calculator

### Weighted Scoring Method

| Dimension | Weight | Scoring Criteria |
|------|------|---------|
| Customer Willingness to Pay | 25% | 10=Customer explicitly willing to pay extra; 5=Indirectly influences deal; 0=No payment connection |
| Strategic Alignment | 20% | 10=Directly supports strategic goals; 5=Indirectly related; 0=Unrelated |
| NRR Contribution | 15% | 10=Significantly improves NRR; 5=Some contribution; 0=No contribution |
| Technical Feasibility | 15% | 10=Mature tech, low effort; 5=Needs tech verification; 0=Extremely high tech risk |
| Competitive Coverage | 10% | 10=All competitors have it, customers always compare; 5=Competitors have it but not critical; 0=Competitors don't have it |
| Implementation Complexity | 10% | 10=Very easy (1 person-week); 5=Medium (2-4 person-weeks); 0=High complexity (>8 person-weeks) |
| NDR Contribution | 5% | 10=Directly prevents churn; 5=Has retention effect; 0=No retention impact |

### Quick Prioritization (MoSCoW Method)

- **Must Have**: Product unusable without this (Basic requirements)
- **Should Have**: Important but can be temporarily solved with workarounds (Performance requirements)
- **Could Have**: Nice to have, acceptable without (Excitement requirements)
- **Won't Have**: Explicitly excluded (everything not in this release goes here)

---

## IV. Version Release Checklist

```
Must Complete Before Go Live:
□ PRD reviewed and approved
□ Technical proposal reviewed
□ UI design mockups confirmed
□ Test cases reviewed
□ All P0 test cases passed
□ All P0 bugs fixed
□ Data migration scripts prepared (if applicable)
□ Rollback plan prepared
□ Help documentation updated
□ Release announcement prepared
□ Customer notification sent (if involving existing customers)
□ Monitoring alerts configured
□ Canary release plan determined (if applicable)
```


---

## v1.1.0 Added: PLG Priority Ranking

### PLG Backlog Priority Matrix
| Priority | Type | Example | Expected Impact |
|--------|------|------|---------|
| P0 | Activation Blocker | Registration flow stuck, core feature unavailable | Directly impacts activation rate |
| P0 | Payment Blocker | Cannot upgrade, payment failure | Directly impacts revenue |
| P1 | Activation Optimization | Onboarding guidance, first-time experience | Boost activation rate 20% |
| P1 | Viral Distribution | Sharing features, collaboration invites | Boost viral coefficient |
| P2 | Retention Improvement | Usage reminders, weekly reports | Boost retention rate |
| P2 | Conversion Optimization | Pricing page optimization, PQL scoring | Boost conversion rate |
| P3 | UX Optimization | UI polish, performance optimization | Long-term competitiveness |

### PLG Sprint Planning
| Sprint | Theme | Core Goal | Key Metric |
|--------|------|---------|---------|
| Sprint 1-2 | Activation Optimization | Registration → First Experience < 5 min | Activation Rate > 40% |
| Sprint 3-4 | Viral Distribution | Sharing feature go live | Viral Coefficient > 0.5 |
| Sprint 5-6 | Paid Conversion | Self-serve upgrade flow | Free → Paid > 3% |
| Sprint 7-8 | Retention Improvement | Usage reminders + weekly reports | M1 Retention > 40% |