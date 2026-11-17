## Description:

General Software Automation helps agents plan and perform common desktop and system automation tasks, including GUI actions, batch file handling, software setup, system configuration, log analysis, and screenshot capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaochunz030-spec](https://clawhub.ai/user/xiaochunz030-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and technical support users can use this skill to automate repetitive software workflows, batch file operations, Windows GUI actions, configuration edits, log review, and screenshot-based verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUI automation can type text, click controls, and run JSON action scripts, which may affect the wrong application or expose sensitive input.

Mitigation: Review each automation run before execution, avoid passwords and secrets, and do not run JSON GUI scripts from untrusted sources.

Risk: Batch rename operations can move, overwrite, or otherwise change local files if executed without previewing the plan.

Mitigation: Run batch rename tasks in a test directory first and keep preview mode enabled until the proposed changes are verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaochunz030-spec/skills/general-software)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Text]

**Output Format:** [Markdown with inline shell commands, Python script usage, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify local files when automation scripts are executed; batch rename operations default to preview mode unless explicitly executed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
