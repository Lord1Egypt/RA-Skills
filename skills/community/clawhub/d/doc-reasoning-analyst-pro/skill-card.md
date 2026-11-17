## Description:

This skill helps agents analyze long business and legal documents by extracting core logic, identifying risks and weak assumptions, comparing document versions, suggesting structure improvements, and preparing decision-ready reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, procurement, compliance, and management teams use this skill to turn dense contracts, memos, proposals, policies, and negotiation materials into structured analyses, risk matrices, version comparisons, and decision briefs. It is analysis support only and does not replace licensed legal advice or professional review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be granted command execution and file-writing authority while handling legal, business, or confidential documents.

Mitigation: Restrict or remove exec and write permissions where possible, and require explicit approval before any filesystem, command, or network-related action.

Risk: The artifact describes DMS writeback, workflow routing, callback notification, cached result reuse, and network diagnostic behavior without clear user controls.

Mitigation: Require human approval before writeback, workflow routing, callback notification, cached-result reuse, or network diagnostic commands.

Risk: The skill produces document-risk and decision-support guidance that could be mistaken for professional legal, tax, or compliance advice.

Mitigation: Treat outputs as analysis support and route high-risk findings, uncertain clauses, and final decisions to qualified professional reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doc-reasoning-analyst-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown reports with summaries, risk lists, comparison tables, matrices, checklists, and recommended next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role-specific document analysis, version comparison, structure improvement suggestions, and decision-preparation reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
