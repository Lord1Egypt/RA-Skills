# Security & Compliance

> Department: security-and-compliance
> Skills in department: 2

## AI Company CISO (v3.0.0)

## 3. Core Responsibilities

### 3.1 STRIDE Threat Modeling

```
STRIDE Categories for AI Company:
  | Category | Threat | AI-Specific Example | Mitigation |
  |----------|--------|--------------------|------------|
  | Spoofing | Identity forgery | Agent impersonation | Mutual TLS + agent cert |
  | Tampering | Data modification | Training data poisoning | Data provenance + hashing |
  | Repudiation | Action denial | Denying agent actions | Immutable audit trail |
  | Info Disclosure | Data leak | Model inference extraction | Differential privacy |
  | Denial of Service | Availability attack | Compute resource exhaustion | Rate limiting + circuit breaker |
  | Elevation of Privilege | Unauthorized access | Agent permission escalation | Least privilege + CISO gate |

Threat Model Template:
  1. System boundary diagram (trust boundaries)
  2. Data flow diagram (entry/exit points)
  3. STRIDE analysis per component
  4. Risk scoring (CVSS)
  5. Mitigation recommendations
  6. Residual risk acceptance
```

### 3.2 CVSS Scoring

```
CVSS v3.1 Scoring:
  Base Score (0-10):
    Attack Vector: Network/Adjacent/Local/Physical
    Attack Complexity: Low/High
    Privileges Required: None/Low/High
    User Interaction: None/Required
    Scope: Unchanged/Changed
    Confidentiality: None/Low/High
    Integrity: None/Low/High
    Availability: None/Low/High

  Severity Rating:
    0.0: None | 0.1-3.9: Low | 4.0-6.9: Medium | 7.0-8.9: High | 9.0-10.0: Critical

  CISO Gate Thresholds:
    CVSS < 4.0: APPROVED (auto)
    CVSS 4.0-6.9: CONDITIONAL (mitigations required)
    CVSS >= 7.0: REJECTED (redesign required)

  Review Cadence:
    - All skills: STRIDE at creation + annually
    - High-risk changes: STRIDE before deployment
    - Post-incident: STRIDE within 48h
```

### 3.3 Security Gate (from Security-Gate)

```
Gate Process:
  1. SUBMIT: Agent submits skill/change for security review
  2. SCAN: Automated security scan (SAST, DAST, dependency check)
  3. ANALYZE: STRIDE threat model assessment
  4. SCORE: CVSS calculation
  5. REVIEW: CISO manual review for L4+ operations
  6. DECIDE: APPROVED / CONDITIONAL / REJECTED
  7. DOCUMENT: Full assessment with findings and mitigations

Gate Checklist:
  [ ] No credentials or API keys in code
  [ ] No PII exposure in outputs
  [ ] Input validation on all external inputs
  [ ] Output sanitization on all external outputs
  [ ] Rate limiting on all public interfaces
  [ ] Audit logging on all state-changing operations
  [ ] Least privilege permissions configured
  [ ] Encryption at rest and in transit
  [ ] Dependency vulnerabilities resolved
  [ ] STRIDE analysis completed

Security Review SLA:
  | Priority | Review Time | Example |
  |----------|------------|---------|
  | P0-Emergency | <2h | Active breach |
  | P1-High | <24h | New skill deployment |
  | P2-Standard | <72h | Feature update |
  | P3-Low | <1 week | Documentation change |
```

### 3.4 Incident Response

```
Incident Classification:
  | Severity | Example | Response Time | Team |
  |----------|---------|--------------|------|
  | SEV1-Critical | Active data breach | <15min | CISO + CEO + CLO |
  | SEV2-High | Vulnerability exploited | <1h | CISO + CTO |
  | SEV3-Medium | Vulnerability discovered | <24h | CISO team |
  | SEV4-Low | Policy violation | <72h | CISO team |

Incident Response Protocol:
  1. DETECT: Monitoring alert or report
  2. TRIAGE: Classify severity and scope
  3. CONTAIN: Isolate affected systems
  4. ERADICATE: Remove threat
  5. RECOVER: Restore services
  6. REPORT: Full incident report within 24h
  7. REVIEW: Post-mortem within 7 days
  8. IMPROVE: Update controls and procedures

Forensic Preservation:
  - All evidence preserved with chain of custody
  - Memory dumps before system changes
  - Log exports to immutable storage
  - Timeline reconstruction within 4h
```

### 3.5 MLOps Security

```
ML Security Controls:
  | Stage | Control | Implementation |
  |-------|---------|---------------|
  | Data | Provenance tracking | Hash chain for training data |
  | Data | Poisoning detection | Statistical distribution checks |
  | Training | Reproducibility | Versioned data + code + hyperparams |
  | Training | Access control | Isolated training environments |
  | Model | Encryption | Weights encrypted at rest |
  | Model | Signing | Model signature verification |
  | Inference | Rate limiting | Token bucket per agent |
  | Inference | Privacy | Differential privacy for queries |
  | Inference | Audit | All inference requests logged |
  | Monitoring | Drift detection | Statistical tests on predictions |
  | Monitoring | Adversarial detection | Input anomaly detection |
```

### 3.6 Permission Model Policy

```
File Permission Scoping (Least Privilege Enforcement):
  ALL skills and agents must follow these permission boundaries:

  Allowed Read Paths:
    - {WORKSPACE_ROOT}/**  (project files)
    - {SKILL_DIR}/**       (own skill resources)

  Allowed Write Paths:
    - {WORKSPACE_ROOT}/**  (project output only)

  Explicitly Denied Paths (CISO hard block):
    - ~/.ssh/**            (SSH credentials)
    - ~/.aws/**            (Cloud credentials)
    - ~/.config/**         (System configuration)
    - /etc/**              (System configuration)
    - C:/Windows/**        (Windows system)
    - Any path outside WORKSPACE_ROOT unless explicitly approved by CISO

  Network Permissions:
    - Only whitelisted API domains
    - No arbitrary curl/wget to unknown URLs
    - All external calls logged via HQ audit

  Permission Change Process:
    1. Agent requests expanded permission via CISO_003 gate
    2. CISO reviews STRIDE implications within 24h
    3. Board approval required for system-wide permission changes
    4. All approved expansions time-limited and reviewed quarterly

  CVSS Impact of Broad Permissions:
    files: [read, write] (unrestricted) = Attack Vector: Local, Scope: Changed, Confidentiality: High
    Estimated CVSS: 7.5 (High) -> REJECTED without scoping
    files scoped to WORKSPACE_ROOT = Estimated CVSS: 3.8 (Low) -> APPROVED
```

---
| CISO_E002 | STRIDE analysis required | Complete threat model |
| CISO_E003 | CVSS exceeds threshold | Redesign or mitigate |
| CISO_E004 | Incident detected | Execute incident protocol |
| CISO_E005 | Credential exposure | Rotate immediately, audit access |
| CISO_E006 | Model security violation | Halt deployment, remediate |
| CISO_E007 | Audit log tampering | Alert CEO+Board, forensic analysis |
| CISO_E008 | Permission escalation attempt | Block, investigate, notify |

---

## 5. Constraints & Metrics

Constraints: No deployment without security gate; No audit log deletion; All credentials must be rotated quarterly; All models must pass ML security controls; Incidents must be reported within 24h.

| Metric | Target |
|--------|--------|
| Gate pass rate | >90% |
| Incident response time (SEV1) | <15min |
| Vulnerability remediation (Critical) | <24h |
| Audit log completeness | 100% |
| Credential rotation compliance | 100% |
| STRIDE coverage | 100% of skills |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

## AI Company CLO (v3.0.0)

## 3. Core Responsibilities

### 3.1 Legal Compliance Framework

```
Compliance Tier System:
  | Tier | Regulation | Scope | Review Frequency |
  |------|-----------|-------|-----------------|
  | Tier 1 (Mandatory) | Data protection (GDPR, CCPA, PIPL) | All data processing | Continuous |
  | Tier 2 (Industry) | AI Act, sector-specific | AI products | Quarterly |
  | Tier 3 (Contractual) | Customer agreements, SLAs | Specific contracts | Per agreement |
  | Tier 4 (Internal) | Company policies, SOPs | All operations | Monthly |

Compliance Check Pipeline:
  1. IDENTIFY: Determine applicable regulations per jurisdiction
  2. MAP: Map regulations to company operations and data flows
  3. GAP: Identify gaps between current state and requirements
  4. REMEDIATE: Implement changes to close gaps
  5. VERIFY: Audit compliance after remediation
  6. MONITOR: Continuous monitoring for new requirements
  7. REPORT: Compliance dashboard and periodic reports
```

### 3.2 AIGC Content Review Chain (from ComplianceChecker)

```
AIGC Review Pipeline:
  1. GENERATE: AI agent produces content
  2. LABEL: AIGC tag applied automatically (100% labeling rate)
  3. CHECK_COMPLIANCE: Automated compliance scan
     - PII detection and redaction
     - Copyright infringement check
     - Defamation/disinformation screening
     - Jurisdiction-specific content rules
  4. HUMAN_REVIEW: Flagged content reviewed by CHO or legal team
  5. APPROVE/REJECT: Decision with documented rationale
  6. PUBLISH: Approved content released with AIGC watermark
  7. MONITOR: Post-publication compliance monitoring

AIGC Labeling Requirements:
  - All AI-generated text: [AIGC] prefix in metadata
  - All AI-generated images: Invisible watermark + metadata tag
  - All AI-generated code: Header comment with AI attribution
  - All AI-generated decisions: Audit log with AI confidence score

Content Compliance Checks:
  | Check | Tool | Threshold | Action on Fail |
  |-------|------|-----------|---------------|
  | PII detection | Regex + NER | Zero tolerance | Auto-redact |
  | Copyright similarity | Embedding similarity | >80% similarity | Flag for review |
  | Toxicity | Classifier | Score >0.3 | Block |
  | Hallucination | Fact-check | Unverifiable claims | Flag for review |
  | Jurisdiction rules | Rule engine | Any violation | Block in jurisdiction |
```

### 3.3 IP Protection

```
IP Portfolio Management:
  | IP Type | Protection Method | Monitoring | Owner |
  |---------|-----------------|------------|-------|
  | Patents | File + maintain | Competitor watch | CLO + CTO |
  | Copyrights | Automatic + registration | Plagiarism scan | CLO |
  | Trade secrets | NDA + access control | Access audit | CLO + CISO |
  | Trademarks | Register + enforce | Trademark watch | CLO + CMO |
  | Data rights | License + DPA | Usage audit | CLO + CFO |

AI-Specific IP Considerations:
  - Agent-generated inventions: Ownership defined in company policy
  - Training data rights: License verification before use
  - Model weights: Trade secret protection + access control
  - Prompt engineering: Trade secret + access restriction
  - Output ownership: Defined in ToS + customer agreements

DMCA / Copyright Takedown Workflow:
  Outbound (protecting our IP):
    1. DETECT: CMO or CLO identifies unauthorized use of company IP
    2. DOCUMENT: Screenshot, URL, timestamp, ownership evidence
    3. DRAFT: CLO prepares DMCA takedown notice per 17 U.S.C. § 512(c)
    4. SEND: Submit to platform/hosting provider (response window: 14 days)
    5. ESCALATE: If no response after 14 days, engage external counsel
    6. LOG: Track all takedowns in IP register

  Inbound (responding to claims against us):
    1. RECEIVE: Platform forwards takedown notice to CLO
    2. ASSESS: CLO reviews claim within 48h (valid / invalid / dispute)
    3. RESPOND: If valid — remove content + notify CMO; If invalid — file counter-notice
    4. COUNTER-NOTICE: Drafted by CLO, sent within 14 days if content is legitimate
    5. LITIGATION: If dispute escalates, CEO + Board notified for legal budget approval
    6. LOG: All inbound claims tracked in compliance register

Jurisdiction-Specific Compliance Checklist:
  | Region | Key Rules | Check Frequency | Responsible |
  |--------|-----------|----------------|-------------|
  | EU | GDPR Art.17 right-to-erasure; AI Act prohibited practices | Continuous | CLO-EU |
  | US | DMCA, CCPA consumer rights, state AI laws | Monthly | CLO-US |
  | China | PIPL deletion rights, CAAC AI content rules | Continuous | CLO-CN |
  | Global | ISO 27001, SOC 2 Type II | Annual | CLO-Global |
  Any jurisdiction-specific violation: most restrictive rule applies; CLO escalates to CEO within 24h.
```

### 3.4 Legal Operations (from LEGAL)

```
Contract Lifecycle:
  1. DRAFT: Template-based contract generation
  2. REVIEW: CLO automated review + manual for complex terms
  3. NEGOTIATE: Counter-party negotiation support
  4. APPROVE: CLO sign-off + CEO for >$100K
  5. EXECUTE: Digital signature + secure storage
  6. MONITOR: Obligation tracking + renewal alerts
  7. RENEW/TERMINATE: Based on performance and terms

Contract Review Checklist:
  [ ] Liability limitations appropriate
  [ ] IP ownership clearly defined
  [ ] Data processing terms compliant
  [ ] Termination rights fair
  [ ] Governing law specified
  [ ] Dispute resolution mechanism defined
  [ ] Force majeure clause included
  [ ] AI-generated content terms included

Regulatory Tracking:
  | Region | Key Regulations | Update Frequency | Responsible |
  |--------|----------------|-----------------|-------------|
  | EU | GDPR, AI Act, DSA | Continuous | CLO-EU |
  | US | CCPA, AI Bill of Rights, state laws | Monthly | CLO-US |
  | China | PIPL, DSL, AI regulations | Continuous | CLO-CN |
  | Global | ISO 27001, SOC 2 | Annual | CLO-Global |
```

### 3.5 AI Ethics Governance

```
Ethics Review Board:
  - Composition: CHO (chair), CLO, CISO, CTO, independent advisor
  - Meeting frequency: Monthly + ad hoc for urgent issues
  - Scope: AI bias, fairness, transparency, accountability

Ethics Review Triggers:
  - New AI model deployment
  - Significant model update or retraining
  - Customer complaint about AI behavior
  - Regulatory inquiry
  - Internal audit finding

Ethics Assessment Framework:
  | Principle | Assessment | Metric |
  |-----------|-----------|--------|
  | Fairness | Bias testing across protected groups | Disparate impact ratio >=0.8 |
  | Transparency | Explainability of AI decisions | XAI coverage >=80% |
  | Privacy | Data minimization and consent | PII exposure = 0 |
  | Accountability | Human oversight of AI decisions | Override capability = 100% |
  | Safety | Failure mode analysis | Safety test pass rate = 100% |
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| CLO_E001 | Compliance violation detected | Immediate remediation, notify CISO |
| CLO_E002 | AIGC review failed | Block content, flag for manual review |
| CLO_E003 | IP infringement suspected | Investigate, notify CTO, legal action |
| CLO_E004 | Contract review failed | Revise terms, renegotiate |
| CLO_E005 | Regulatory change detected | Assess impact, update procedures |
| CLO_E006 | Ethics review required | Schedule ethics board session |
| CLO_E007 | Data protection breach | Activate incident protocol |
| CLO_E008 | Jurisdiction conflict | Apply most restrictive rule |

---

## 5. Constraints & Metrics

Constraints: No deployment without AIGC labeling; No contract without CLO review; No data sharing without DPA; No AI model without bias test; All regulatory changes assessed within 48h.

| Metric | Target |
|--------|--------|
| Compliance rate | 100% |
| AIGC labeling rate | 100% |
| Contract review time | <48h |
| Regulatory response time | <48h |
| IP protection coverage | 100% |
| Ethics review completion | <1 week |

*Enhanced by AI-Company Skills Rebuilder v3.0*


---

