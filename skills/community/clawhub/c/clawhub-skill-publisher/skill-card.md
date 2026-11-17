## Description:

Publishes and syncs local bot skills to ClawHub using non-browser login, preflight safety checks, and automated release scripts for single or batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

MIT

## Use Case:

Developers, OpenClaw operators, and agent teams use this skill to publish one local skill or sync a local skills directory to ClawHub with repeatable CLI-driven release steps and preflight checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A ClawHub token could be exposed through misuse of token or registry handling.

Mitigation: Use a short-lived, low-scope token, avoid untrusted registry values, and rotate the token if authentication behavior is unexpected.

Risk: Publishing or syncing the wrong directory could upload unintended skill content.

Mitigation: Review the exact skill directory or sync root before upload and run with --dry-run to inspect the command before publishing.

Risk: The default CJK policy may block legitimate multilingual skill content.

Mitigation: Use --allow-cjk only after confirming the registry policy and intended language coverage.

## Reference(s):

- [ClawHub Skill Publisher listing](https://clawhub.ai/wanng-ide/skills/clawhub-skill-publisher)
- [ClawHub registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide ClawHub publish or sync actions and may include dry-run shell commands before upload.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
