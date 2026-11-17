## Description:

AI Agent general tools provide command references for system monitoring, log analysis, process management, file handling, network diagnostics, Docker inspection, and Git operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to help an agent propose common system administration, diagnostics, file-processing, Docker, log-analysis, process-management, and Git commands during operational troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad system administration commands that can delete files, terminate processes, run background jobs, or perform network checks.

Mitigation: Require explicit approval before destructive, process-ending, background, or external network commands, and run agents with the least OS permissions needed.

Risk: Command suggestions may be too broad for the user's current system scope.

Mitigation: Ask the agent to state the target path, process, service, host, or container before execution and verify that scope with the operator.

## Reference(s):

- [Cool Agent Tools on ClawHub](https://clawhub.ai/chuangyinbot-boop/skills/cool-agent-tools)
- [Publisher profile](https://clawhub.ai/user/chuangyinbot-boop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before execution, especially when commands can delete files, terminate processes, start background jobs, or perform external network checks.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and OpenClaw frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
