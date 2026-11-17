## Description:

Create a privacy-first digital life inventory and cleanup plan from user-supplied information only. This skill does not scan devices, cloud accounts, passwords, or files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agents use this skill to create a privacy-first plan for organizing files, subscriptions, accounts, backups, and maintenance routines from user-supplied descriptions only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste passwords, recovery codes, private keys, session cookies, or sensitive account data while requesting organization help.

Mitigation: Warn users not to paste secrets and work only from rough descriptions or non-sensitive inventory items.

Risk: Cleanup, deletion, subscription cancellation, or account closure steps can cause data loss or unwanted account changes if followed too quickly.

Mitigation: Recommend reversible first steps, confirm backups before cleanup, and have users perform final actions directly with the provider.

Risk: Users may mistake checklist guidance for a device scan, password audit, or security guarantee.

Mitigation: State that the skill does not scan devices, cloud accounts, passwords, or files, and phrase account-security help as checklist guidance only.

## Reference(s):

- [Safety Boundaries](references/safety-boundaries.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/digital-life-organizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown plan with checklist sections and an inventory table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-supplied information only; no shell commands, file operations, account access, or credential handling.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states v1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
