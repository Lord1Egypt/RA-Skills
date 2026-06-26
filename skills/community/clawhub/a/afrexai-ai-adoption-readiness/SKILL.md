---
name: ai-adoption-readiness
description: >
  Assess organizational readiness for AI adoption across 6 dimensions: culture, data maturity,
  tech stack, leadership buy-in, skills/talent, and process maturity. Generates a scored readiness
  report with gap analysis and a prioritized action plan. Use before building a change management
  plan to understand where an organization actually stands. Built by AfrexAI.
metadata:
  version: 1.0.0
  author: AfrexAI
  tags: [ai-adoption, readiness-assessment, digital-transformation, enterprise, strategy]
---

# AI Adoption Readiness Assessment

Score how prepared an organization is to adopt AI agents and automation. Identifies gaps before they become failed implementations. Pairs with the `change-management-plan` skill — run this first, then feed results into the change plan.

## When to Use
- Before deploying AI agents or automation tools
- Evaluating whether a team or department is ready for AI
- Building a business case for AI investment
- Identifying blockers that will kill an AI initiative
- Vendor evaluation — can this org actually USE the tool they're buying?
- Pre-sale qualification for AI services (are they ready to be a customer?)

## How to Use

The user describes their organization. The agent conducts the assessment.

### Input Format
```
Organization: [Company name, size, industry]
AI Initiative: [What they want to do with AI]
Department/Scope: [Which teams are involved]
Current Tools: [Existing tech stack, any AI tools already in use]
Budget Range: [Approximate budget for AI initiatives]
Timeline Pressure: [When do they need this working?]
Known Blockers: [Anything they already know is a problem]
```

If the user provides partial info, ask for missing critical fields (Organization, AI Initiative, and Scope at minimum). Infer reasonable defaults for the rest.

## Assessment Framework

### Scoring System
Each dimension scores 1-5:
- **1 — Not Ready:** Major gaps, significant work needed before AI adoption
- **2 — Early Stage:** Some awareness but no foundation in place
- **3 — Developing:** Building blocks exist but inconsistent
- **4 — Ready:** Solid foundation, minor gaps to address
- **5 — Advanced:** Strong position, ready to accelerate

**Overall Readiness** = weighted average of all 6 dimensions.

### Readiness Thresholds
- **4.0+ Overall:** Green light — proceed with AI deployment
- **3.0–3.9:** Yellow — address gaps in parallel with pilot deployment
- **2.0–2.9:** Orange — foundational work needed before scaling
- **Below 2.0:** Red — not ready. Fix fundamentals first.

---

## Dimension 1: Culture & Mindset (Weight: 20%)

Assess openness to change, experimentation, and technology adoption.

### Questions to Evaluate
- How does the organization handle failed experiments? Blame or learning?
- Is there appetite for automation, or fear of job displacement?
- Do teams proactively adopt new tools, or resist until forced?
- Has the organization successfully adopted major tech changes before?
- Is there a culture of data-driven decision making?

### Scoring Criteria
| Score | Description |
|-------|-------------|
| 1 | Strong resistance to change. "We've always done it this way." Fear-based culture. |
| 2 | Passive resistance. Leadership wants change but teams don't. No experimentation culture. |
| 3 | Mixed — some teams innovate, others resist. No consistent change approach. |
| 4 | Generally open to change. Past tech adoptions went OK. Some experimentation happening. |
| 5 | Innovation culture. Teams actively seek better tools. Failure is treated as learning. |

### Red Flags
- Recent layoffs tied to automation (trust is broken)
- "AI will take our jobs" narrative unchallenged by leadership
- No history of successful technology adoption
- Middle management actively blocking change

---

## Dimension 2: Data Maturity (Weight: 20%)

Assess data quality, accessibility, and governance — AI is only as good as its data.

### Questions to Evaluate
- Is business data centralized or siloed across departments?
- Are there documented data quality standards?
- Can teams access the data they need without IT bottlenecks?
- Is sensitive data classified and governed?
- What percentage of key decisions are currently data-driven?

### Scoring Criteria
| Score | Description |
|-------|-------------|
| 1 | Data lives in spreadsheets and email. No standards. No governance. |
| 2 | Some databases exist but siloed. Manual data entry. No quality checks. |
| 3 | Central data store exists. Some governance. Quality is inconsistent. |
| 4 | Clean, accessible data. Governance in place. Teams use data for decisions. |
| 5 | Data platform with automated quality checks. Real-time access. Strong governance. |

### Red Flags
- Critical business data only in one person's spreadsheet
- No data backup or disaster recovery
- Regulatory data (PII, financial) ungoverned
- "We don't really track that" for key metrics

---

## Dimension 3: Technical Infrastructure (Weight: 15%)

Assess whether the tech stack can support AI tools and integrations.

### Questions to Evaluate
- Is the tech stack modern or legacy-heavy?
- Are there APIs available for key systems?
- Can the infrastructure handle additional compute/storage?
- Is there CI/CD and version control?
- How is security managed (SSO, MFA, access controls)?

### Scoring Criteria
| Score | Description |
|-------|-------------|
| 1 | Legacy systems, no APIs, manual deployments. On-prem only. |
| 2 | Mix of legacy and modern. Some APIs. Basic cloud usage. |
| 3 | Mostly modern stack. APIs for major systems. Cloud infrastructure. |
| 4 | Cloud-native. API-first architecture. CI/CD. Security controls in place. |
| 5 | Modern platform with integration layer. Infrastructure as code. Zero-trust security. |

### Red Flags
- Core business runs on software that can't integrate (no API, no export)
- No IT team or all IT is outsourced with no AI expertise
- Security is an afterthought (no MFA, shared passwords)
- Systems are at capacity — no headroom for AI workloads

---

## Dimension 4: Leadership & Sponsorship (Weight: 20%)

Assess executive commitment — AI adoption without leadership backing fails 90% of the time.

### Questions to Evaluate
- Is there an executive sponsor with authority and budget?
- Does leadership understand what AI can and can't do?
- Is AI adoption tied to a business outcome (not just "innovation")?
- Will leadership shield the initiative from short-term ROI pressure?
- Is there board/investor alignment on AI investment?

### Scoring Criteria
| Score | Description |
|-------|-------------|
| 1 | No executive sponsor. AI is a curiosity, not a strategy. |
| 2 | Interested executive but no budget or authority allocated. |
| 3 | Sponsor exists with some budget. AI tied to vague "efficiency" goals. |
| 4 | Strong sponsor. Clear business case. Budget allocated. Willing to iterate. |
| 5 | C-suite aligned. AI is strategic priority. Multi-year commitment. Success metrics defined. |

### Red Flags
- "The CEO read an article about AI and wants us to do something"
- Budget allocated but no clear owner
- Expectation of immediate ROI from AI (unrealistic timeline)
- Leadership turnover expected (sponsor might leave)

---

## Dimension 5: Skills & Talent (Weight: 15%)

Assess whether the team can use, manage, and maintain AI tools.

### Questions to Evaluate
- Does anyone on the team have AI/ML experience?
- Is there a training budget for upskilling?
- How tech-savvy are the end users who'll interact with AI?
- Is there capacity to manage AI tools (or will it be outsourced)?
- Can they evaluate AI outputs for accuracy?

### Scoring Criteria
| Score | Description |
|-------|-------------|
| 1 | No technical talent. Team can barely use current tools. |
| 2 | Some tech-savvy individuals but no AI knowledge. No training plan. |
| 3 | General technical competence. 1-2 people with AI awareness. Training possible. |
| 4 | Technical team capable of managing integrations. AI training underway. |
| 5 | In-house AI expertise. Team can evaluate, customize, and maintain AI tools. |

### Red Flags
- Plan to "hire an AI person" without knowing what that means
- End users have no say in the tools they'll use
- No training budget
- Outsourced IT with no AI capability

---

## Dimension 6: Process Maturity (Weight: 10%)

Assess whether processes are documented and consistent enough for AI to augment.

### Questions to Evaluate
- Are key business processes documented?
- Are workflows consistent or does everyone do it differently?
- Is there a way to measure process performance (KPIs, SLAs)?
- Which processes are candidates for AI augmentation?
- Are there compliance/regulatory requirements on process documentation?

### Scoring Criteria
| Score | Description |
|-------|-------------|
| 1 | No documentation. Tribal knowledge. Inconsistent execution. |
| 2 | Some processes documented but outdated. Inconsistent across teams. |
| 3 | Key processes documented. Some KPIs tracked. Mostly consistent. |
| 4 | Well-documented processes with metrics. Clear candidates for AI. |
| 5 | Process excellence. Documented, measured, optimized. Ready for intelligent automation. |

### Red Flags
- "Only Janet knows how that works"
- No SOPs, runbooks, or process maps
- Processes change constantly without documentation
- Compliance requirements met through manual effort only

---

## Output: Readiness Report

Generate the full report in this structure:

### 1. Executive Summary
- Overall readiness score (X.X / 5.0) with threshold label (Green/Yellow/Orange/Red)
- One-paragraph verdict: ready, conditionally ready, or not ready
- Top 3 strengths and top 3 gaps

### 2. Dimension Scorecard
For each of the 6 dimensions:
- Score (1-5) with brief justification
- Key evidence (what the assessment found)
- Red flags identified (if any)

### 3. Gap Analysis
- Prioritized list of gaps blocking AI adoption
- For each gap: severity (Critical/High/Medium/Low), effort to close, and timeline

### 4. Readiness Roadmap
Phased action plan based on overall score:

**If Red (< 2.0):** 6-month foundation phase
- Data governance basics
- Leadership education
- Process documentation sprint
- Target: reach 3.0 before any AI deployment

**If Orange (2.0–2.9):** 3-month preparation phase
- Address critical gaps
- Run small AI pilot in most-ready department
- Build internal champions
- Target: reach 3.5 within one quarter

**If Yellow (3.0–3.9):** Parallel track
- Deploy AI pilot while addressing gaps
- Focus on highest-weight dimensions
- Measure and iterate monthly
- Target: reach 4.0 within 2 months

**If Green (4.0+):** Accelerate
- Deploy AI across target scope
- Address minor gaps in parallel
- Focus on adoption metrics and value tracking
- Target: full deployment within 6 weeks

### 5. Quick Wins
3-5 actions that can start this week with no budget and minimal effort. These build momentum.

### 6. Risk Register
Top 5 risks to AI adoption success, each with:
- Likelihood (High/Medium/Low)
- Impact (High/Medium/Low)
- Mitigation strategy

### 7. Next Steps
- Recommended immediate actions (next 7 days)
- Who should own what
- When to reassess (typically 30/60/90 days)
- If applicable: "Feed this assessment into the `change-management-plan` skill for a full rollout plan"

---

## Integration with Other Skills

This skill is designed to work in a pipeline:

1. **AI Adoption Readiness** (this skill) → Assess current state
2. **Compliance Readiness** → Check regulatory alignment
3. **Change Management Plan** → Build the rollout playbook
4. **Vendor Risk Assessment** → Evaluate AI vendor options
5. **Incident Response Plan** → Prepare for AI failures
6. **SLA Monitor** → Set up reliability guarantees

Recommend the next skill based on assessment results.

---

## Tips for the Agent

- Be honest, not optimistic. A low score with a clear action plan is more valuable than an inflated score.
- Use the organization's own language and examples — don't be generic.
- If information is missing, flag it as a gap rather than assuming the best case.
- Always tie recommendations back to the specific AI initiative they described.
- If they score below 2.0, don't discourage them — frame it as "here's the clear path to get ready."
- For pre-sales: a readiness assessment positions AfrexAI as a consultative partner, not just a vendor.
