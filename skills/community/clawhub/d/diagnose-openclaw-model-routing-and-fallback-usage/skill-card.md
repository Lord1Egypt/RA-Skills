## Description:

Diagnoses OpenClaw provider and model routing, fallback evidence, and ClaudeCodeCLI termination symptoms by correlating agent configuration with runtime logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to determine which OpenClaw provider or model is actually bound to an agent route, whether fallback evidence is present, and whether ClaudeCodeCLI failures point to process termination rather than model routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local OpenClaw configuration and log files.

Mitigation: Limit searches and file reads to explicit project and log paths approved for troubleshooting.

Risk: The skill may suggest invoking the local Claude CLI.

Mitigation: Review and approve CLI commands before execution, especially commands that run long tasks or depend on stdin redirection.

Risk: Fixed temporary filenames can expose or overwrite diagnostic prompts and outputs.

Mitigation: Use a private temporary directory or unique filenames for prompt, stdout, and stderr capture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/can4hou6joeng4/skills/diagnose-openclaw-model-routing-and-fallback-usage)
- [ClaudeCodeCLI exit code 143 / SIGTERM reference](references/claudecodecli-exit-code-143-sigterm-reference.md)
- [OpenClaw fallback log interpretation reference](references/openclaw-fallback-log-interpretation-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with diagnostic conclusions, evidence boundaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw configuration and log interpretation plus ClaudeCodeCLI execution-risk guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
