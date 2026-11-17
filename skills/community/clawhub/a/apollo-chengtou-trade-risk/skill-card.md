## Description:

Apollo Chengtou Trade Risk helps agents review Chinese local-government financing platform trade contracts, counterparty risk, and state-owned asset supervision issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and enterprise risk teams use this skill to screen trade contracts, assess counterparties, interpret regulatory red lines, and draft concise risk-control reports before business decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests retention of customer feedback, new risk patterns, regulatory updates, and ambiguous cases after each task.

Mitigation: Install with a policy that requires explicit user consent, redaction, and human review before storing contract text, company details, feedback, or case material.

Risk: The skill supports contract and compliance risk screening but does not provide legal advice and may rely on stale business, judicial, or regulatory data.

Mitigation: Use outputs as preliminary risk-control guidance only; require legal review and current source verification before major contract, counterparty, or regulatory decisions.

Risk: The recorded evaluation report shows 0 of 8 test cases passing.

Mitigation: Run fresh evaluations in the target agent environment and resolve failed coverage before using the skill in decision-support workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-chengtou-trade-risk)
- [Contract review report template](references/合同审查报告模板.md)
- [Real-case examples](references/真实案例.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown risk reports with optional Python scanner output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include risk levels, issue tables, due-diligence checklists, policy mapping, and remediation guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter and README state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
