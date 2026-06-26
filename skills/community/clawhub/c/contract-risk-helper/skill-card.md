## Description: <br>
Contract risk helper. Input Chinese or English contract text; identify common risky clauses, classify severity, and suggest negotiation or revision points. Boundary: preliminary risk spotting only, not a lawyer and not formal legal advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to screen Chinese or English contract text for common risky clauses, grouped by severity with negotiation or revision suggestions. It supports preliminary risk spotting only and is not a substitute for advice from a qualified lawyer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake preliminary pattern-based risk spotting for formal legal advice. <br>
Mitigation: Keep the legal boundary visible and require qualified legal review for important contracts, jurisdiction-specific questions, or final negotiation decisions. <br>
Risk: Contract text can contain private business, customer, billing, or credential information. <br>
Mitigation: Redact unnecessary sensitive information before use and avoid sharing full transcripts or private exports unless explicitly needed. <br>
Risk: Pattern matching can miss uncommon clauses or produce incomplete context for complex agreements. <br>
Mitigation: Use the output as a triage aid and review the full agreement manually, especially for high-value, regulated, or cross-border contracts. <br>


## Reference(s): <br>
- [Common Contract Risk Patterns](artifact/references/common-risks.md) <br>
- [Contract Risk Helper on ClawHub](https://clawhub.ai/harrylabsj/contract-risk-helper) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, text] <br>
**Output Format:** [Markdown-style bilingual risk report with severity sections and summary statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports matched clause categories, severity levels, short descriptions, and suggested negotiation or revision points.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
