## Description:

Organize, track, and analyze contracts with renewal alerts, clause lookups, and multi-role support for individuals, landlords, freelancers, and legal teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users, individuals, landlords, freelancers, and legal teams use this skill to organize local contract files, extract factual metadata, track deadlines, and find clauses without requesting legal interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contracts and extracted metadata may contain sensitive personal, financial, signature, or confidential business information.

Mitigation: Keep contract files and metadata local and private, use owner-only permissions for the contracts folder, avoid logging contract content, and review generated meta.md files for sensitive data.

Risk: Calendar sync or file links can expose deadline metadata or contract locations.

Mitigation: Enable calendar sync or file links only when the calendar is private and the user accepts the exposure risk.

Risk: Users may ask for legal interpretation, risk scoring, or signing recommendations.

Mitigation: Limit responses to factual extraction, reminders, organization, and clause display; direct users to a qualified attorney for interpretation or advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/contracts)
- [Role-specific workflows](artifact/roles.md)
- [Contract analysis patterns](artifact/analysis.md)
- [Alert and deadline tracking](artifact/alerts.md)
- [Security and boundaries](artifact/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with local file organization patterns and deadline-tracking checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local contract metadata files, reminders, dashboards, and clause lookup results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
