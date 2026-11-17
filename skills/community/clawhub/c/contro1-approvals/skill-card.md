## Description:

How to ask a human before a sensitive action and how to log every autonomous action, so your work is accountable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contro1](https://clawhub.ai/user/contro1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide when sensitive actions need human approval and to record autonomous actions for accountability. It is intended for workflows involving spending, access changes, deployment, deletion, outbound messages, fetched code, or production sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to send audit records for autonomous actions to an externally configured bridge, which can expose sensitive details if logging is not minimized.

Mitigation: Configure a known HTTPS bridge with authentication, and do not log secrets, cookies, tokens, message bodies, private file contents, sensitive paths, payment data, or personal identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contro1/skills/contro1-approvals)
- [Contro1 CLI documentation](https://contro1.com/docs/cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides approval requests and audit logging; it does not produce files directly.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
