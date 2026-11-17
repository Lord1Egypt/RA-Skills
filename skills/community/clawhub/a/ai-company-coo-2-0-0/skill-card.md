## Description:

AI公司首席运营官（COO）技能包。战略拆解、OKR对齐、流程自动化治理、组织智能化转型、人机责权划分、三位一体监督闭环。

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations agents use this skill to translate CEO strategy into OKRs, monitor operational health, coordinate C-suite agents, and produce governance, process, and progress artifacts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file access can expose unrelated user, memory, OKR, report, or audit-log data.

Mitigation: Restrict file access to dedicated memory, OKR, report, and audit-log paths, and require explicit approval before reading USER.md or unrelated memory files.

Risk: Network access and inter-agent messaging can send operational context to unintended destinations.

Mitigation: Constrain network requests and agent messages to approved destinations, and review outbound operational summaries before sharing real company data.

Risk: COO-style recommendations can overstep budget, personnel, quality, or high-risk approval boundaries.

Mitigation: Require human approval for high-risk actions and route budget, personnel, and quality decisions through the documented CEO, CHO, and CQO approval paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnsmithfan/skills/ai-company-coo-2-0-0)
- [ClawHub Skill Homepage](https://clawhub.com/skills/ai-company-coo)
- [Publisher Profile](https://clawhub.ai/user/johnsmithfan)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown reports and structured JSON objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces COO decisions, OKR plans, process recommendations, decision logs, progress reports, and audit-oriented artifacts.]

## Skill Version(s):

2.0.1 (source: server release; SKILL.md frontmatter says 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
