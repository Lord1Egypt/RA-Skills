## Description:

Helps an agent set up and check Everpod cloud computers and prepare a move to an always-on OpenClaw pod at its owner's request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[everpod](https://clawhub.ai/user/everpod)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use this skill to start or check an Everpod pod for their agents, or to prepare an existing agent for migration to a pod. The owner creates the access key and completes payment and account setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A migration bundle can expose private agent and workspace context if transferred without review.

Mitigation: Show the owner the exact files and data categories before packaging; remove unnecessary private or regulated content, and exclude passwords, API keys, and configuration. Revoke the old Everpod key after migration if it is no longer needed.

## Reference(s):

- [Everpod API documentation](https://everpod.ai/docs/api)
- [Everpod skill listing](https://clawhub.ai/everpod/skills/everpod)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline commands and pod links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare a migration ZIP containing workspace context, skills, and scheduled-job details at the owner's request.]

## Skill Version(s):

1.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
