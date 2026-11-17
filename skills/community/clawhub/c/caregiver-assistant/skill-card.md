## Description:

护工助手 generates a single-file interactive HTML caregiving dashboard for patient records, care logs, medication, vital signs, diet, family reports, emergency handling, multi-patient management, and shift handoff workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT

## Use Case:

External caregiving teams, elder-care facilities, and home-care coordinators use this skill to produce a browser-based dashboard for tracking patient care, medication status, vital signs, reports, emergency procedures, and team handoffs. It is appropriate for lightweight local coordination, but should not be used as a regulated medical record or operational care system without additional privacy, access-control, validation, audit, and storage protections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive patient and caregiving information using weak local browser storage.

Mitigation: Avoid real patient information unless the deployment adds privacy controls, protected storage, access control, audit logging, and a clear data-retention process.

Risk: Exported JSON backups may contain sensitive patient information.

Mitigation: Protect exported files, limit sharing, and treat backups as confidential healthcare-adjacent data.

Risk: Importing untrusted backup files can introduce unsafe or misleading data into the dashboard.

Mitigation: Import only trusted backups and review imported records before using them for care coordination.

Risk: The dashboard includes healthcare workflow prompts and emergency guidance but is not validated as a regulated care system.

Mitigation: Do not rely on it for regulated healthcare records or operational care decisions without clinical, legal, security, and compliance review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/caregiver-assistant)
- [Publisher profile](https://clawhub.ai/user/bettermen)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Caregiver HTML app](assets/caregiver.html)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance that points to a single-file HTML caregiving dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated dashboard stores data in browser localStorage and supports JSON import and export backups.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
