# Stakeholder Analysis Template

## Document Information

| Field | Content |
|------|------|
| Project/Change Name | [Name] |
| Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |

---

## 1. Stakeholder Landscape

### 1.1 Stakeholder Spectrum

```
┌─────────────────────────────────────────┐
│ Decision Layer: Who Approves?              │
│ Management Layer: Who is evaluated? Most impacted? │
│ Execution Layer: Who actually operates?    │
│ Impact Layer: Who is indirectly affected?  │
│ External Layer: Customers/Suppliers/Regulators? │
└─────────────────────────────────────────┘
```

### 1.2 Stakeholder Directory

| ID | Name | Title | Role Type | Layer | Contact |
|----|------|------|---------|---------|---------|
| SH-01 | | | Sponsor | Decision | |
| SH-02 | | | Business Owner | Management | |
| SH-03 | | | Core User | Execution | |

---

## 2. Power-Interest Analysis

### 2.1 Power-Interest Matrix

| ID | Name | Power (1-5) | Interest (1-5) | Quadrant | Management Strategy |
|----|------|----------|----------|------|---------|
| SH-01 | | 5 | 5 | Manage Closely | 1-on-1 weekly reports + decision participation |
| SH-02 | | 4 | 5 | Manage Closely | Weekly meetings + instant communication |
| SH-03 | | 2 | 4 | Keep Informed | Monthly reports + feedback collection |
| SH-04 | | 4 | 2 | Keep Satisfied | Milestone notifications |
| SH-05 | | 1 | 2 | Minimal Effort | Public announcements |

### 2.2 Management Strategy Details

```
Manage Closely (High Power + High Interest):
- Frequency: At least 1 one-on-one per week
- Content: Progress + Risks + Decision requests
- Goal: Become their strategic partner, not just a demand-side contact

Keep Satisfied (High Power + Low Interest):
- Frequency: Monthly or per milestone
- Content: Concise one-page summary
- Goal: Avoid them being "surprised" by issues

Keep Informed (Low Power + High Interest):
- Frequency: Every two weeks
- Content: Progress + Participation opportunities
- Goal: Convert them into allies who help drive change

Minimal Effort (Low Power + Low Interest):
- Frequency: As needed
- Content: Public channel notifications
- Goal: Don't let them become future blockers
```

---

## 3. Attitude-Influence Analysis

| ID | Name | Current Attitude | Influence | Conversion Target | Conversion Strategy |
|----|------|---------|--------|---------|---------|
| SH-01 | | Supportive | High | Champion | Empower + Public recognition |
| SH-02 | | Neutral | High | Ally | Demonstrate personal benefits |
| SH-03 | | Opposed | Medium | Neutral | Understand concerns + Prove with small wins |
| SH-04 | | Unknown | Medium | Supportive | Schedule 1-on-1 to gauge stance ASAP |

### 3.1 Strategy for Opponents

```
Root Cause Analysis for Opponents:
├── Interests harmed → Seek compensation solutions
├── Don't understand the value → More precise communication
├── Past negative experiences → Prove with small wins + Commit to improvements
├── Overlooked / Loss of face → Invite them to participate, value their contributions
├── Style / Culture clash → Find someone they trust as an intermediary
└── Pure resistance to change → If a key person, seek support from their superior

Principle: Don't try to "eliminate" opponents; try to "convert" them.
```

---

## 4. Key Role Deep-Dive Analysis

### 4.1 [Decision-Maker / Sponsor]

| Dimension | Analysis |
|------|------|
| KPI/OKR | |
| Personal Goals/Ambitions | |
| Risk Appetite | |
| Decision-Making Style | Data-driven / Intuitive / Consensus / Autocratic |
| Information Preference | Detailed / Summary / Verbal / Written |
| Trusted People/Advisors | |
| Attitude in Past Similar Projects | |
| Our Influence Strategy | |

### 4.2 [Business Owner]

(Same structure as above)

### 4.3 [Core Opponent]

(Same structure as above)---

## 5. Communication Plan

| Stakeholder | Communication Goal | Core Message | Channel | Frequency | Owner | Measurement (How to know it's effective) |
|-----------|---------|---------|------|------|--------|------------------|
| | | | | | | |

### 5.1 Key Communication Milestones

| Milestone | Timing | Communication Content | Participants | Expected Outcome |
|------|------|---------|--------|---------|
| Project Kickoff | | Vision/Objectives/Plan/Roles | All key stakeholders | Understanding + Engagement |
| Milestone 1 | | | | |
| Go/No-Go | | Full business case | Decision-makers | Approval |
| Go Live | | Readiness + Contingency plan | All stakeholders | Confidence + Support |

---

## 6. RACI Matrix

| Activity/Decision | SH-01 | SH-02 | SH-03 | SH-04 | SH-05 |
|----------|-------|-------|-------|-------|-------|
| Approve Budget | A | R | I | I | - |
| Confirm Requirements | I | A | R | C | I |
| Solution Design | - | C | R | A | - |
| Implementation | - | I | C | R | R |
| Acceptance | I | A | R | C | - |
| Go Live Decision | A | R | C | I | - |

R=Responsible (Executes) A=Accountable (Answerable) C=Consulted (Advised) I=Informed (Notified)

---

## 7. Risks & Responses

| Risk | Stakeholders Involved | Trigger Signal | Response Plan |
|------|----------------|---------|---------|
| Sponsor departure/rotation | SH-01 | | Cultivate Backup Sponsor + Prepare handover package |
| Core user collective resistance | SH-03 | | Early participation + Prove with small wins + Build alliances |
| Opponent's influence growing | SH-04 | | Regularly monitor attitude changes |


---

## v1.1.0 Added: BABOK Agile Extension — Stakeholder Collaboration Patterns

### Stakeholder Management in Agile Environments
| Traditional BA | Agile BA | Key Difference |
|--------|--------|---------|
| Identify all stakeholders fully upfront | Iterative identification, adjust each Sprint | Dynamic management |
| Formal sign-off confirmation | Continuous collaboration + instant feedback | Reduced formalism |
| Standalone requirements documents | Shared Product Backlog | Transparency |

### Stakeholder Engagement Cadence (Scrum Framework)
| Role | Sprint Planning | Daily Scrum | Sprint Review | Retrospective |
|------|---------------|-------------|---------------|---------------|
| Product Owner | Leads | Optional | Leads | Participates |
| Business Sponsor | As needed | No | Participates | No |
| End Users | No | No | Participates (Feedback) | No |
| Development Team | Participates | Leads | Participates | Leads |
| BA | Supports PO | Optional | Observes + Records | Participates |