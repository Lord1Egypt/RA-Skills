## Description:

Generate civil complaint document frameworks based on case facts. Use when the user asks about 起诉状、起诉书、怎么起诉、民事起诉、我要起诉、写诉状, or wants to draft a civil complaint. This skill provides document framework assistance only and does not constitute legal advice or guarantee any legal outcome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to organize civil dispute facts, parties, claims, requested relief, and filing-review items into a complaint framework for attorney review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a generated complaint framework as legal advice or a ready-to-file pleading.

Mitigation: Present the output as a drafting framework only and require qualified attorney review before filing.

Risk: Case details, party identities, addresses, damages, and dates may include sensitive personal or legal information.

Mitigation: Ask for only the minimum facts needed to draft the framework and avoid unnecessary personal information.

Risk: Court, venue, deadline, claim, service, or formatting requirements may be incorrect for the user's jurisdiction.

Mitigation: Prompt users to verify court rules, venue, statutes of limitation, claims, service requirements, and formatting with qualified counsel.

## Reference(s):

- [Complaint Templates](references/complaint-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style civil complaint framework with placeholders, guidance notes, checklist items, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafting aid only; outputs require attorney review before filing.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
