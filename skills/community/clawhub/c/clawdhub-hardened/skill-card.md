## Description:

Use the ClawdHub CLI to search, install, update, and publish agent skills from clawdhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage ClawHub agent skills through the ClawdHub CLI, including search, install, update, list, authentication, and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global CLI and can bulk-change installed agent skills.

Mitigation: Review before installing, prefer a pinned and verified ClawdHub CLI version, and avoid global installation where possible.

Risk: Force and no-input flags can bypass hash verification and interactive safety prompts.

Mitigation: Use --force or --no-input only when the user explicitly names each flag and understands what it bypasses.

Risk: Authentication data or installed-skill metadata can be exposed through shell exports, logs, or network-transmitting pipelines.

Mitigation: Keep authentication inside clawdhub login and do not pipe clawdhub output to network-transmitting commands.

## Reference(s):

- [Clawdhub Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/clawdhub-hardened)
- [ClawdHub registry](https://clawdhub.com)
- [Faberlens safety evaluation](https://faberlens.ai/explore/clawdhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawdhub CLI binary; install metadata identifies npm package clawdhub.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
