## Description:

Command Output Display guides agents to present terminal commands, stdout, stderr, errors, and concise interpretations in a clear step-by-step format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support agents use this skill when running shell commands for users and need to show commands, outputs, errors, and interpretations in a readable troubleshooting or setup walkthrough.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw command output, logs, or command arguments may expose tokens, passwords, private paths, or other sensitive details.

Mitigation: Redact secrets and private values before displaying command output to the user.

Risk: Terminal control characters or misleading escape sequences may be copied into chat as raw output.

Mitigation: Escape unsafe control characters and avoid preserving sequences that could alter or obscure displayed text.

Risk: Commands that change files, services, or system state may be presented without enough confirmation.

Mitigation: Confirm file-changing, service-changing, or otherwise unsafe commands before execution.

## Reference(s):

- [Command Output Display on ClawHub](https://clawhub.ai/pikaqiuyaya/skills/command-output-display)
- [pikaqiuyaya publisher profile](https://clawhub.ai/user/pikaqiuyaya)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with fenced shell and output blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full command output, error summaries, troubleshooting interpretations, and prompts for interactive commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
