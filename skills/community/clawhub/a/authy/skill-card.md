## Description:

Inject secrets into subprocesses via environment variables without exposing secret values to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric8810](https://clawhub.ai/user/eric8810)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to run trusted local commands, tests, deployment scripts, and services with scoped secrets injected as environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets are injected into subprocess environments, so an untrusted command or destination could expose credentials.

Mitigation: Review each authy run command before execution, run only trusted scripts or clients, and use the narrowest available scope.

Risk: Printed, logged, redirected, or persisted environment variables could leak sensitive values.

Mitigation: Do not echo, print, log, redirect, or write secret-bearing environment variables to disk.

## Reference(s):

- [Authy Command Reference](artifact/references/commands.md)
- [Authy Homepage](https://github.com/eric8810/authy)
- [ClawHub Authy Skill Page](https://clawhub.ai/eric8810/skills/authy)
- [ClawHub Publisher Profile](https://clawhub.ai/user/eric8810)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require authy on PATH, AUTHY_TOKEN, and AUTHY_KEYFILE.]

## Skill Version(s):

0.3.0 (source: release evidence and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
