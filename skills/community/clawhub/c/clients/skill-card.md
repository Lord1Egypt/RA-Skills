## Description:

Manages client relationships end to end for freelancers, consultants, and agencies: qualifying leads, scoping, onboarding, scope creep, getting paid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, consultants, and agencies use this skill to manage the commercial client lifecycle from lead qualification through proposals, onboarding, delivery, payment collection, retention, and offboarding. It helps draft client-facing messages and maintain local client records while leaving sending, signing, pricing commitments, and acceptance decisions to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains long-lived local client records and may read, write, or delete business-sensitive information.

Mitigation: Install only when automatic local client-record maintenance is desired; review announced writes and deletions and keep backups of Clawic data folders.

Risk: User-derived names and references can influence paths for clients, projects, contacts, artifacts, and configuration files.

Mitigation: Use safe generated slugs or validated relative paths before creating, updating, or deleting records.

Risk: Client work often involves credentials or access details that should not be stored in local notes.

Mitigation: Store credential pointers only, such as password-manager, keychain, or environment-variable references, and avoid writing secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/clients)
- [Clawic Clients homepage](https://clawic.com/skills/clients)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown guidance, client-facing drafts, checklists, local record updates, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, update, or delete local Clawic client, contact, project, receivable, and artifact records under configured local data folders.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
