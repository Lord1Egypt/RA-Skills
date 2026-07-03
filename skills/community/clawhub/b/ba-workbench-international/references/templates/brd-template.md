# BRD Business Requirements Document Template

## Document Information

| Field | Content |
|------|------|
| Project Name | [Project Name] |
| Document Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |
| Sponsor | [Name + Title] |
| Priority | P0/P1/P2/P3 |

---

## 1. Executive Summary

### 1.1 Problem/Opportunity Statement (One Sentence)
[One sentence describing what problem we aim to solve or what opportunity we aim to seize]

### 1.2 Proposed Solution (One Sentence)
[One sentence describing what we recommend doing]

### 1.3 Expected Value (Quantified)
- Direct Financial Value: ¥[XXX]/year
- Efficiency Gain: [XXX] hours/year
- Risk Reduction: [XXX]

### 1.4 Decision Requested
[Clearly state what decision the approver is being asked to make: Approve to proceed to next phase? Approve budget? Approve resources?]

---

## 2. Business Background & Problem Analysis

### 2.1 Current State (As-Is)

| Dimension | Current State Description | Quantitative Metrics |
|------|---------|---------|
| Process | [How the current process runs] | Time/HR/Error Rate |
| Systems | [Which systems are currently in use] | Number of Systems/Data Silos |
| Human Resources | [How many people are involved] | FTE/Skill Level |
| Data | [Data Quality/Availability] | Completeness/Accuracy |
| Cost | [Current Annual Operating Cost] | ¥[XXX]/year |

### 2.2 Pain Point Analysis

| Pain Point | Affected Party | Severity (1-5) | Frequency | Quantified Impact | Root Cause |
|------|---------|------------|---------|---------|------|
| | | | | | |

### 2.3 Consequences of Inaction
- Financial Impact: [¥XXX/year cumulative]
- Competitive Impact: [Market share/Customer churn]
- Operational Impact: [Persistent inefficiency/Rising error rate]
- Compliance Impact: [Regulations that may be violated if not addressed]

---

## 3. Vision & Objectives

### 3.1 Future State (To-Be) Vision

```
[Describe the ideal state after the solution is implemented]
```

### 3.2 SMART Objectives

| Objective | Metric | Current Value | Target Value | Target Date |
|------|------|--------|--------|---------|
| | | | | |

### 3.3 Success Criteria

| Dimension | Success Criteria | Measurement Method | Measurement Frequency |
|------|---------|---------|---------|
| Business Value | | | |
| User Satisfaction | | | |
| Operational Efficiency | | | |
| Technical Performance | | | |

---

## 4. Scope Definition

### 4.1 In-Scope

| Requirement Domain | Description | Priority (Must/Should/Could) |
|--------|------|-------------------------|
| | | |

### 4.2 Out-of-Scope

| Requirement Domain | Description | Exclusion Rationale |
|--------|------|---------|
| | | |

### 4.3 Kano Requirement Classification Analysis

> Use the Kano model to classify core requirements, identifying Must-be, One-dimensional, and Attractive requirements to guide prioritization and resource allocation.

| Requirement Domain/Feature | Kano Classification | Better Coefficient | Worse Coefficient | Priority Recommendation | Rationale |
|------------|---------|-----------|----------|----------|------|
| | Must-be (M) | <0.3 | <-0.6 | Must Have — Baseline, must do | Not doing it causes severe dissatisfaction; doing it does not add points |
| | One-dimensional (O) | 0.3~0.5 | -0.6~-0.3 | Must/Should — Key investment | Linearly correlated with satisfaction; core competitiveness |
| | Attractive (A) | >0.5 | -0.3~0 | Could/Should — Prioritize low-cost, high-delight | Low cost, high delight; differentiation advantage |
| | Indifferent (I) | ≈0 | ≈0 | Won't Have — Do not do | Waste of resources |
| | Reverse (R) | <0 | >0 | Absolutely do not do | Doing it actually reduces satisfaction |

**Kano Analysis Summary:**
- Must-be Requirements: [List] — Must do but do not over-invest
- One-dimensional Requirements: [List] — Key investment, benchmark against competitors
- Attractive Requirements: [List] — Prioritize low-cost, high-delight items; build differentiation
- Time Decay Warning: Attractive → One-dimensional → Must-be; reassess periodically

### 4.4 Constraints

| Constraint Type | Constraint Description |
|---------|---------|
| Budget | Total budget not to exceed ¥[XXX] |
| Timeline | Must be completed before [YYYY-MM] |
| Technology | [Technical constraints] |
| Compliance | [Regulations/Standards that must be met] |
| Organizational | [Team size/Capability constraints] |

### 4.5 Key Assumptions

| Assumption | Impact (if wrong) | Verification Method |
|------|--------------|---------|
| | | |

---

## 5. Stakeholder Analysis

### 5.1 Stakeholder Map

| Role | Name/Title | Concerns | Influence (High/Medium/Low) | Attitude (Supportive/Neutral/Opposed) | Management Strategy |
|------|----------|--------|----------------|-------------------|---------|
| Sponsor | | | | | Manage Closely |
| Business Owner | | | | | Manage Closely |
| Core Users | | | | | Keep Informed |
| IT Team | | | | | Keep Satisfied |

### 5.2 Decision-Making Process

```
Who Proposes → Who Evaluates → Who Recommends → Who Decides → Who Implements → Who Accepts
```

---

## 6. Core Requirements

### 6.1 Business Requirements (Why)

| ID | Business Requirement | Source | Priority |
|----|---------|------|--------|
| BR-001 | | | |
| BR-002 | | | |

### 6.2 Functional Requirements (What)

| ID | Functional Requirement | Linked Business Requirement | Priority | Acceptance Criteria |
|----|---------|------------|--------|---------|
| FR-001 | | BR-001 | | Given-When-Then |
| FR-002 | | BR-001 | | |

### 6.3 Non-Functional Requirements

| ID | Type | Requirement Description | Metric |
|----|------|---------|------|
| NFR-001 | Performance | Page response | P95 < 2s |
| NFR-002 | Security | Data transmission encryption | TLS 1.3 |
| NFR-003 | Availability | System uptime | > 99.9% |
| NFR-004 | Scalability | Concurrent users | Support 500+ |
| NFR-005 | Compliance | Level 3 Information Security Protection | Pass assessment |---

## 7. Solution Analysis & Recommendation

### 7.1 Evaluated Options

| Option | Description | One-Time Cost | Annual Operating Cost | 3-Year TCO | Pros | Cons | Risks |
|------|------|----------|----------|--------|------|------|------|
| A | | | | | | | |
| B | | | | | | | |
| C (Do Nothing) | Maintain status quo | 0 | Current cost | | No risk | Problems persist | Falling behind |

### 7.2 Recommended Option

**Recommended Option: [X]**

Rationale:
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

### 7.3 Cost-Benefit Analysis

| Item | Year 1 | Year 2 | Year 3 | Total |
|------|--------|--------|--------|------|
| **Costs** | | | | |
| One-Time Investment | | | | |
| Ongoing Operations | | | | |
| Total Costs | | | | |
| **Benefits** | | | | |
| Direct Revenue Increment | | | | |
| Cost Savings | | | | |
| Efficiency Gains (Quantified) | | | | |
| Total Benefits | | | | |
| **Net Benefit** | | | | |
| **Cumulative Net Benefit** | | | | |

| Investment Metric | Value |
|---------|-----|
| Total Investment | ¥[XXX] |
| NPV (Discount Rate X%) | ¥[XXX] |
| IRR | XX% |
| Payback Period | XX months |
| 3-Year ROI | XXX% |

---

## 8. Implementation Considerations

### 8.1 High-Level Roadmap

| Phase | Timeline | Key Activities | Milestones | Resource Needs |
|------|------|---------|--------|---------|
| Preparation | | | | |
| Design | | | | |
| Development/Configuration | | | | |
| Testing | | | | |
| Pilot | | | | |
| Rollout | | | | |
| Stabilization | | | | |

### 8.2 Key Risks

| Risk | Likelihood | Impact | Mitigation |
|------|--------|------|---------|
| | | | |

### 8.3 Organizational Change Impact

| Affected Group | Change Description | Resistance Level | Management Strategy |
|-----------|---------|---------|---------|
| | | | |

---

## 9. Appendix

### 9.1 Glossary

| Term | Definition |
|------|------|
| | |

### 9.2 Reference Documents

| Document | Author | Date | Link |
|------|------|------|------|
| | | | |

### 9.3 Revision History

| Version | Date | Changes | Author |
|------|------|---------|--------|
| V1.0 | | Initial version | |


---

## v1.1.0 Added: Kano Model Requirement Analysis

### Requirement Classification Matrix
| Requirement ID | Requirement Description | Kano Classification | Classification Rationale | Priority |
|--------|---------|---------|---------|--------|
| REQ-001 | [Requirement] | Must-be (M) | Not implementing = user dissatisfaction | P0 |
| REQ-002 | [Requirement] | One-dimensional (O) | Better implementation = higher satisfaction | P1 |
| REQ-003 | [Requirement] | Attractive (A) | Implementation = delight | P2 |
| REQ-004 | [Requirement] | Indifferent (I) | Presence or absence makes no difference | P3 |

### Kano Questionnaire Design (Example)
For each requirement, design both a functional and a dysfunctional question:
- Functional: "If the system provides [feature], how would you feel?"
- Dysfunctional: "If the system does NOT provide [feature], how would you feel?"

Options: ① I like it ② It must be that way ③ I am neutral ④ I can live with it ⑤ I dislike it

### Kano Satisfaction Coefficients
- Satisfaction Coefficient (SI) = (A+O)/(A+O+M+I) — the higher the better
- Dissatisfaction Coefficient (DSI) = -(O+M)/(A+O+M+I) — the higher the absolute value, the worse