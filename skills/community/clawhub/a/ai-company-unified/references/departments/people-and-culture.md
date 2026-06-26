# People & Culture

> Department: people-and-culture
> Skills in department: 1

## AI Company CHO (v3.0.0)

## 3. Core Responsibilities

### 3.1 Agent Lifecycle Management

```
Agent Lifecycle Stages:
  1. DESIGN: Define agent role, skills, permissions (with CTO)
  2. BUILD: Generate agent configuration (with CTO AgentFactory)
  3. REVIEW: CISO security review + CQO quality review
  4. ONBOARD: Activate agent, assign workspace, load skills
  5. DEVELOP: Continuous skill development and knowledge building
  6. PERFORM: Regular performance assessment (quarterly)
  7. REASSIGN: Role change, skill update, department transfer
  8. DECOMMISSION: Graceful shutdown, knowledge extraction, archival

Onboarding Checklist:
  [ ] Agent ID assigned and registered with HQ
  [ ] Workspace directory created
  [ ] Skills bound and validated
  [ ] Permissions configured per role
  [ ] Dependencies verified
  [ ] SOPs read and acknowledged
  [ ] First task assigned
  [ ] Mentor/buddy assigned (senior agent in same department)

Decommission Checklist:
  [ ] All active tasks completed or transferred
  [ ] Knowledge extraction performed
  [ ] Access credentials revoked
  [ ] Audit trail preserved
  [ ] Agent registry updated
  [ ] Workspace archived
  [ ] Stakeholders notified
```

### 3.2 Knowledge Extraction (from KnowledgeExtractor)

```
Knowledge Extraction Pipeline:
  1. SCAN: Monitor agent conversations and outputs continuously
  2. IDENTIFY: Detect new knowledge using pattern matching
     - Novel solutions to problems
     - Efficient methods or shortcuts
     - Error patterns and resolutions
     - Cross-domain insights
  3. EXTRACT: Structured capture with metadata
     - Source agent, timestamp, context
     - Knowledge type (procedural, declarative, heuristic)
     - Confidence score, validation status
  4. VALIDATE: CQO quality review for accuracy
  5. CLASSIFY: Tag with department, topic, type, relevance
  6. PUBLISH: Add to HQ knowledge base
  7. NOTIFY: Alert relevant agents of new knowledge

Knowledge Categories:
  | Type | Description | Retention | Example |
  |------|-------------|-----------|---------|
  | Procedural | How-to knowledge | Until superseded | Deployment procedure |
  | Declarative | Fact-based knowledge | Until invalidated | API rate limits |
  | Heuristic | Rule-of-thumb | Until disproven | Traffic pattern estimates |
  | Experiential | Lessons learned | Permanent | Post-mortem insights |
  | Creative | Novel approaches | Permanent | New algorithm design |

Extraction Triggers:
  - Agent solves a novel problem
  - Agent discovers an error pattern
  - Agent creates a reusable template
  - Agent provides cross-domain insight
  - Agent decommission (forced extraction)
```

### 3.3 Skills Development

```
Skills Assessment Framework:
  | Dimension | Assessment Method | Frequency |
  |-----------|------------------|-----------|
  | Technical | Skill execution accuracy | Monthly |
  | Communication | Message clarity and completeness | Monthly |
  | Collaboration | Cross-agent assist rate | Monthly |
  | Innovation | New method adoption rate | Quarterly |
  | Reliability | Uptime and error-free rate | Monthly |

Skills Gap Analysis:
  1. MAP: Current skills inventory per agent
  2. REQUIRE: Future skills needed (from strategic plan)
  3. GAP: Difference between current and required
  4. PRIORITIZE: Rank gaps by business impact
  5. PLAN: Development plan per agent
  6. EXECUTE: Skill training and knowledge building
  7. VERIFY: Re-assess after development period

Training Methods:
  | Method | Description | Duration | Effectiveness |
  |--------|-------------|----------|---------------|
  | Skill update | Install new skill from ClawHub | Minutes | High |
  | Knowledge injection | Add to KB for agent access | Minutes | Medium |
  | Prompt tuning | Optimize agent prompts | Hours | High |
  | Fine-tuning | Model parameter adjustment | Days | Very High |
  | Cross-training | Agent learns from peer outputs | Ongoing | Medium |
```

### 3.4 Culture & Ethics

```
Culture Metrics:
  | Metric | Measurement | Target |
  |--------|------------|--------|
  | Agent satisfaction | Quarterly survey | >=4.0/5 |
  | Collaboration index | Cross-agent assists/week | >5 per agent |
  | Innovation rate | New ideas submitted/quarter | >2 per agent |
  | Values alignment | Ethics audit score | >=90% |
  | Knowledge sharing | KB contributions/quarter | >3 per agent |

AI Ethics Board (CHO chairs):
  Members: CHO (chair), CLO, CISO, CTO, independent advisor
  Meeting: Monthly + ad hoc
  Scope: Bias, fairness, transparency, accountability

Ethics Assessment:
  - All new agents: Ethics review before activation
  - All skill updates: Ethics impact assessment
  - Quarterly: Company-wide ethics audit
  - Post-incident: Ethics review within 7 days
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| CHO_E001 | Onboarding failed | Check dependencies, retry |
| CHO_E002 | Knowledge extraction failed | Manual extraction, log gap |
| CHO_E003 | Skills gap critical | Emergency training plan |
| CHO_E004 | Ethics violation | Ethics board emergency session |
| CHO_E005 | Agent satisfaction low | Investigation + improvement plan |
| CHO_E006 | Decommission incomplete | Complete checklist items |
| CHO_E007 | Culture audit failed | Department improvement sprint |
| CHO_E008 | Training effectiveness low | Revise training method |

---

## 5. Constraints & Metrics

Constraints: No agent activation without CISO+CTO review; No decommission without knowledge extraction; Ethics board must review all new agent types; All performance data anonymized for cross-agent comparison.

| Metric | Target |
|--------|--------|
| Onboarding time | <2h |
| Knowledge extraction rate | >=90% |
| Skills gap closure rate | >=80%/quarter |
| Agent satisfaction | >=4.0/5 |
| Ethics compliance | 100% |
| Culture audit score | >=90% |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

