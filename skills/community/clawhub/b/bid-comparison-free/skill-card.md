## Description:

Compares multiple bidders' quotation line items locally, aligning item names, identifying missing or extra items, and ranking bidder totals without payment, registration, API keys, or network use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, bid review, and evaluation-support users use this skill to compare quotation details across at least two bidders, spot missing or extra line items, and review totals sorted from low to high. It is a mechanical comparison aid and does not decide award outcomes, assess price reasonableness, or make legal findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The comparison output may be mistaken for a procurement decision or full audit.

Mitigation: Treat it as a mechanical comparison aid; human reviewers should verify items and totals and make procurement decisions through the applicable evaluation process.

Risk: Documentation and trigger wording may cause the skill to run during general procurement discussion or overstate the exact columns produced.

Mitigation: Invoke it only when bid quotation data should be analyzed, and verify the produced fields against the supplied source data.

Risk: The free version omits checks such as outlier pricing, arithmetic validation, quantity mismatch review, and maximum-price comparison.

Mitigation: Use separate review steps for omitted checks and do not treat an absence of findings as proof that no issues exist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenqg618/skills/bid-comparison-free)
- [Publisher Profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-style console text or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; requires at least two bidders and withholds conclusions when input is insufficient.]

## Skill Version(s):

1.0.47 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
