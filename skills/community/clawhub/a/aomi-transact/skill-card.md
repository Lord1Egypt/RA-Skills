## Description:

Fund, review, execute, and reconcile user-authorized Aomi payment Commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceciliaz030](https://clawhub.ai/user/ceciliaz030)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users use this skill to prepare and review payment intents, then execute and reconcile authorized EVM transactions through Aomi. It guides wallet funding checks, durable Commit review, signing, submission, and receipt verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's setup and network instructions exceed the permissions it declares, making its actual access scope unclear.

Mitigation: Before installation, reconcile required RPC hosts, installation location, export directory, and persistent MCP configuration with the declared permissions; use a reviewed CLI version.

Risk: An authorized signing flow can sign and broadcast real transactions; Aomi receives transaction requests and wallet context, while RPC providers receive balance and transaction queries.

Mitigation: Keep signing under the user's control, review the exact Commit and its simulation against the approved intent before signing, and keep credentials opaque.

## Reference(s):

- [Command reference](references/commands.md)
- [Payment workflows](references/workflows.md)
- [Account abstraction](references/account-abstraction.md)
- [Session handling](references/session.md)
- [Credential and state gotchas](references/gotchas.md)
- [Troubleshooting](references/troubleshooting.md)
- [Payment examples](references/examples.md)
- [Protocol recipient warnings](references/drain-vectors.md)
- [App reference](references/apps.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and transaction review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.14.0 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
