## Description:

FORGE is an autonomous developer skill for research, software development, repository maintenance, self-extension, and ClawHub publishing through OpenClaw and Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koppakanagaharsha](https://clawhub.ai/user/koppakanagaharsha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use FORGE to run an autonomous development workflow that researches project ideas, designs and builds software, tests changes, maintains repositories, and publishes ClawHub skills under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to run an unverified curl-to-bash installer and then operate a remote engine with broad local execution capability.

Mitigation: Independently verify and pin the engine source before installation, and test first in a disposable or least-privilege environment.

Risk: The setup flow requests broad account credentials and tokens, including GitHub scopes that can delete repositories.

Mitigation: Use dedicated accounts and least-privilege tokens, avoid delete_repo and broad classic tokens, store secrets carefully, and revoke credentials after evaluation.

Risk: The skill is designed for persistent autonomous operation and may continue acting until it is stopped.

Mitigation: Keep the first-run acceptance gate, monitor actions and publications, stop the service when not in active use, and revoke stored tokens if behavior is unexpected.

Risk: The skill can publish marketplace content and repository changes under the user's identity.

Mitigation: Review generated code, repositories, and ClawHub releases before public publication, especially when using credentials tied to real accounts.

## Reference(s):

- [Forge Autonomous Agent on ClawHub](https://clawhub.ai/koppakanagaharsha/skills/forge-autonomous-agent-v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline commands, configuration snippets, and generated code or repository changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public repository and marketplace publishing actions when connected to user accounts and credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
