# GDPR and AI Intersection in HR Context

## Overview

AI systems in HR must comply with both the EU AI Act and GDPR. This document explains where these regulations intersect and what HR professionals need to know.

---

## Key Principles

### GDPR Principles (Article 5)

| Principle | AI Implication |
|-----------|----------------|
| **Lawfulness, fairness, transparency** | AI decisions must be lawful, fair, and explainable |
| **Purpose limitation** | AI can only process data for specified, explicit purposes |
| **Data minimisation** | AI systems should only use necessary data |
| **Accuracy** | AI outputs must be accurate and kept up to date |
| **Storage limitation** | AI training data retention must be justified |
| **Integrity and confidentiality** | AI systems must have appropriate security |
| **Accountability** | Controllers must demonstrate compliance |

---

## Article 22: Automated Individual Decision-Making

### ⚠️ EU vs UK Divergence (Updated July 2026)

The EU and UK now have **different frameworks** for automated decision-making. For UK/Ireland cross-border work, assess under both.

#### EU GDPR Article 22 (Ireland)

GDPR Article 22 provides specific protections against automated decision-making:

> "The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her."

**Model:** Restrictive — solely automated decisions with legal/significant effects are generally prohibited unless an exception applies.

Article 22 applies when:

1. **Decision is solely automated** — No meaningful human involvement
2. **Decision produces legal effects** — Hiring, firing, promotion
3. **Decision similarly significantly affects** — Rejecting job applications

Rights under Article 22:
1. **Obtain human intervention** — Request human review
2. **Express their point of view** — Contest the decision
3. **Contest the decision** — Challenge the outcome

Lawful basis for automated decisions (EU):
1. **Necessary for contract performance** — Limited to contract preparation
2. **Authorised by EU/Member State law** — Limited scope
3. **Based on explicit consent** — Must be freely given

**Important**: Rights under Article 22(1) cannot be waived by consent for decisions based solely on automated processing.

#### UK Articles 22A–22D (DUAA 2025, effective 5 February 2026)

The UK replaced GDPR Article 22 with a new framework under the Data (Use and Access) Act 2025:

**Model:** Permissive + safeguards — automated decisions are **allowed** provided appropriate safeguards are in place.

| Aspect | EU GDPR Art. 22 | UK DUAA 22A–22D |
|--------|-----------------|-------------------|
| **Approach** | Restrictive (prohibition model) | Permissive (regulated activity model) |
| **Lawful basis** | Explicit consent, contract, law | Consent OR legitimate interests (broader) |
| **Safeguards** | Human intervention, express view, contest | Notice, ability to object, human review |
| **Effective** | Since 2018 | 5 February 2026 |

**Key implication for Irish employers:** If you process data of UK data subjects or operate in the UK, you may be able to use automated decisions under the UK framework that would not be permitted under EU GDPR. However, for operations in Ireland, EU GDPR Article 22 applies.

**For cross-border HR AI:** Document which framework applies to which data subjects. Do not assume one size fits both.

---

## Data Minimisation for AI Training Data

### GDPR Requirements

- Collect only data necessary for the specified purpose
- Do not retain data longer than necessary
- Do not use data for purposes incompatible with original collection

### AI Training Data Considerations

| Question | Compliance Consideration |
|----------|-------------------------|
| Is the data necessary for the AI's purpose? | Must justify each data element |
| Is the data accurate? | Training data quality affects AI accuracy |
| How long is training data retained? | Must justify retention period |
| Is training data properly anonymised? | Anonymisation must be effective |
| Are data subjects informed? | Privacy notice must cover AI training |

### Training Data Best Practices

1. **Document data sources** — Where did training data come from?
2. **Limit data categories** — Only collect what's needed
3. **Anonymise where possible** — Reduce privacy risk
4. **Set retention limits** — Delete training data when no longer needed
5. **Conduct DPIA** — Data Protection Impact Assessment required for high-risk processing

---

## Data Protection Impact Assessment (DPIA)

### When Required

A DPIA is **required** when:

- Processing is likely to result in high risk to rights and freedoms
- Using new technologies (AI qualifies)
- Systematic evaluation of personal aspects
- Processing on a large scale
- Automated decision-making with legal effects

### DPIA for AI Systems

A DPIA for AI must cover:

1. **Systematic description of processing**
   - What the AI does
   - What data it processes
   - Who it affects

2. **Necessity and proportionality**
   - Why AI is necessary
   - Could the purpose be achieved another way
   - Is processing proportionate to purpose

3. **Assessment of risks**
   - Risks to data subjects
   - Bias and discrimination risks
   - Accuracy risks
   - Security risks

4. **Measures to address risks**
   - Technical measures
   - Organisational measures
   - Human oversight measures

5. **Consultation with DPO**
   - Data Protection Officer must be consulted
   - Document their opinion

---

## Irish DPC Guidance

### Relevant Publications

1. **Guidance on Automated Decision-Making and Profiling** (2018)
   - Available at: https://www.dataprotection.ie/sites/default/files/2018-05/Guidance%20on%20Automated%20Decision-Making%20and%20Profiling%20v1.pdf

2. **Guidance on AI and Data Protection** (2024)
   - Available at: https://www.dataprotection.ie/

3. **DPIA Template and Guidance**
   - Available at: https://www.dataprotection.ie/

### Key Points from Irish DPC

1. **Transparency is essential** — Data subjects must know when AI is being used
2. **Human oversight is required** — Purely automated decisions are rarely lawful in HR
3. **DPIA is mandatory** — For AI processing in HR context
4. **Record processing activities** — Article 30 records must include AI systems
5. **International transfers** — Ensure appropriate safeguards for data transfers

---

## Practical Checklist

### Before Deploying AI in HR

- [ ] Conduct Data Protection Impact Assessment
- [ ] Identify lawful basis for processing
- [ ] Ensure transparency in privacy notices
- [ ] Implement human oversight mechanisms
- [ ] Establish data retention periods
- [ ] Document training data sources
- [ ] Test for bias and discrimination
- [ ] Consult with Data Protection Officer
- [ ] Establish procedures for subject access requests
- [ ] Create appeals process for AI-affected decisions

### During AI Operation

- [ ] Monitor for accuracy and bias
- [ ] Log all AI decisions
- [ ] Retain human oversight
- [ ] Respond to data subject requests
- [ ] Review and update DPIA
- [ ] Conduct regular audits

### After AI Changes

- [ ] Update DPIA if processing changes significantly
- [ ] Re-test for bias
- [ ] Update documentation
- [ ] Notify affected individuals if required

---

## Key GDPR Articles for AI in HR

| Article | Title | AI Relevance |
|---------|-------|--------------|
| 5(1) | Principles | Fairness, transparency, accuracy requirements |
| 13-14 | Information provision | Transparency about AI processing |
| 22 (EU) | Automated decision-making | Rights for AI-affected individuals (restrictive model) |
| 22A–22D (UK) | Automated decision-making (DUAA 2025) | Permissive + safeguards model (effective 5 Feb 2026) |
| 35 | DPIA | Assessment for high-risk processing |
| 37 | DPO designation | Requirement to consult DPO |
| 30 | Records of processing | Documentation of AI processing |

---

## EU AI Act and GDPR Relationship

| Aspect | GDPR | EU AI Act | Interaction |
|--------|------|-----------|-------------|
| **Scope** | All personal data processing | High-risk AI systems | Both apply to HR AI |
| **Risk approach** | Risk-based approach | Risk categories (high/medium/minimal) | Complementary |
| **Transparency** | Article 13-14 rights | Article 13 transparency requirements | Reinforce each other |
| **Human oversight** | Article 22 intervention | Article 14 oversight | Overlap for high-risk systems |
| **Accountability** | Article 5(2) | Articles 9-15 requirements | Documentation obligations |

---

## References

- **GDPR**: Regulation (EU) 2016/679
- **EU AI Act**: Regulation (EU) 2024/1689
- **Irish DPC Guidance**: https://www.dataprotection.ie/
- **EDPB Guidelines on Automated Decision-Making**: https://edpb.europa.eu/
- **Article 29 Working Party Opinion on AI**: WP251

---

*Last updated: July 2026 | Updated for UK DUAA 2025 (Articles 22A–22D) and Digital Omnibus package*  
*Author: Enda Rochford*  
*For informational purposes only — not legal advice*