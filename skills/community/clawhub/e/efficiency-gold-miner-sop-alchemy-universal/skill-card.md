## Description:

This skill helps employees review authorized work traces from calendars, tasks, documents, sheets, approvals, mail, and messages to identify repeated workflow friction and produce automation SOPs, skill requirement cards, daily report drafts, and next-day tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nopedijah](https://clawhub.ai/user/nopedijah)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to turn authorized work traces into repeat-work analysis, automation opportunity cards, daily report drafts, and confirmed follow-up tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized work connectors can expose customer, financial, contract, or HR information.

Mitigation: Summarize sensitive content, avoid exposing raw sensitive text, and review drafts carefully before confirming document, table, task, or message actions.

Risk: Confirmed write actions can create or update documents, tables, tasks, or reminder drafts.

Mitigation: Show the target resource, draft content, recipients when relevant, and the reason for action before requiring explicit user confirmation.

Risk: Incorrect or fabricated resource identifiers could direct work to the wrong document, table, task, approval, or conversation.

Mitigation: Use only identifiers returned by upstream tools, selected by the user, or extracted from valid user-provided links; ask for a target when evidence is missing.

Risk: Too little work-trace evidence can make automation recommendations overconfident.

Mitigation: Use light review mode when fewer than three valid evidence items are available and disclose that the sample is insufficient for strong Top 3 conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nopedijah/skills/efficiency-gold-miner-sop-alchemy-universal)
- [Workflow](references/workflow.md)
- [DWS Products](references/dws-products.md)
- [Ecosystem Adapters](references/ecosystem-adapters.md)
- [Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, task lists, priority scores, evidence chains, and optional JSON-oriented shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authorized connectors and keeps write actions pending until explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
