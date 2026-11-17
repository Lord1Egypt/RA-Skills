## Description:

API配额监控与手动切换 monitors OpenClaw model API usage, reports quota-related errors, and helps switch models after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to check API quota-related failures, review suggested model changes, and run explicit switch commands after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model switching can rewrite OpenClaw configuration and restart the Gateway, which may interrupt active service.

Mitigation: Review any --confirm or --model invocation before allowing it, run during a maintenance window when possible, and keep a backup of the OpenClaw configuration.

Risk: Gateway restart behavior and custom config or log paths can affect files or processes outside the intended release workflow.

Mitigation: Run the skill as a normal user, verify the configured OpenClaw and log paths before execution, and avoid elevated privileges unless they are explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/api-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs status summaries, confirmation prompts, model lists, and command guidance for OpenClaw configuration changes.]

## Skill Version(s):

1.0.1 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
