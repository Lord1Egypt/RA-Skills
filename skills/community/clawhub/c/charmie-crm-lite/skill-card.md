## Description:

Lightweight CRM with SQLite - manage contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[businessbrainsolutions](https://clawhub.ai/user/businessbrainsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage a local SQLite contact list by adding, searching, updating, and deleting contact records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact records are stored locally in a plaintext SQLite database.

Mitigation: Use the skill only for low-sensitivity contact lists and keep the installation directory private.

Risk: Contact records can be updated or deleted by name without built-in confirmation.

Mitigation: Manually confirm the exact contact before asking an agent to update or delete records.

Risk: Dependency installation may introduce third-party package risk.

Mitigation: Review dependency versions before running npm install.

## Reference(s):

- [Charmie CRM Lite on ClawHub](https://clawhub.ai/businessbrainsolutions/skills/charmie-crm-lite)
- [Publisher profile](https://clawhub.ai/user/businessbrainsolutions)
- [Product homepage](https://BusinessBrainSolutions.WealthDaoinc.com)
- [Professional upgrade information](https://BusinessBrainSolutions.WealthDaoinc.com/pro)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands]

**Output Format:** [Text responses and JSON-serialized contact records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores contacts in a local SQLite database.]

## Skill Version(s):

3.0.3 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
