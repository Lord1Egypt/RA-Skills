## Description:

Maintain a local, email-only CRM ledger in SQLite. Use for adding sourced email contacts, recording email lifecycle events, checking whether a contact is safe to email, and processing email suppressions or unsubscribes. This skill never discovers contacts or sends email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codereyes-1](https://clawhub.ai/user/codereyes-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a local, email-only CRM ledger, record email lifecycle events, process suppressions, and check contact readiness before an external sender acts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's tool scope is unclear, and the security review had coverage gaps.

Mitigation: Review the scripts and publishing command before installation, and verify the two references the scan could not resolve.

## Reference(s):

- [Schema contract](references/schema.md)
- [Email readiness rules](references/readiness-rules.md)
- [Project homepage](https://github.com/codereyes-1/openclaw-email-crm-skill)
- [ClawHub release page](https://clawhub.ai/codereyes-1/skills/email-crm)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; helper results are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite ledger; the skill does not send email.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
