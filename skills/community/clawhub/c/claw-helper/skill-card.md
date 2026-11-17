## Description:

claw-helper helps agents answer OpenClaw usage, configuration, and troubleshooting questions, including CLI-based diagnostics and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thincher](https://clawhub.ai/user/thincher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to troubleshoot gateway, channel, configuration, and model issues, consult the local OpenClaw documentation index, and draft CLI-based remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose OpenClaw CLI configuration changes that alter local state.

Mitigation: Review proposed commands and configuration changes before execution, and confirm they match the intended OpenClaw environment.

Risk: Troubleshooting notes or documentation index updates could accidentally store sensitive logs, tokens, private account details, or incorrect guidance.

Mitigation: Keep secrets and private logs out of notes, and review file edits against authoritative OpenClaw documentation before saving them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thincher/skills/claw-helper)
- [Problem-solving experience notes](references/experience.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw CLI diagnostics, configuration changes, and local troubleshooting notes; contains no executable payload.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
