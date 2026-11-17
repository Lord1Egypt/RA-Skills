## Description:

Analyzes tender documents and company knowledge bases to produce bid preparation checklists, budget-scaled technical proposal drafts, scoring simulations, win-probability guidance, competitive analysis, and compliance risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Bid managers, presales teams, and proposal reviewers use this skill to turn tender text, company solution knowledge, and optional competitor information into structured bid planning and strategy material. It is intended to support human proposal drafting and review, not to replace final legal, pricing, compliance, or bid-owner approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may include confidential bid documents, pricing, customer details, certifications, or internal proposal material.

Mitigation: Use sanitized excerpts or RAG snippets where possible, remove secrets and unnecessary personal or commercial data, and restrict use to approved bid materials.

Risk: Generated bid strategy, scoring estimates, and compliance notes may be incomplete or inaccurate.

Mitigation: Require human review by the proposal owner, compliance reviewer, and pricing or legal stakeholders before relying on generated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/bidding-analyzer)
- [Publisher profile](https://clawhub.ai/user/boboy-j)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce long, budget-scaled proposal drafts; source evidence sets max_tokens to 80000 and streaming to true.]

## Skill Version(s):

1.2.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
