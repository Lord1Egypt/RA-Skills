## Description:

Helps agents manage and optimize OpenClaw configuration, including model selection, skill management, tool setup, and system tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junsheng428](https://clawhub.ai/user/junsheng428)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review, adjust, and troubleshoot OpenClaw assistant settings for models, skills, tools, channels, and runtime performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration examples can change live OpenClaw settings or restart services.

Mitigation: Review every configuration patch and restart command before execution, apply one change at a time, test after each change, and keep backups.

Risk: API-key examples can lead to credential exposure if real secrets are written directly into commands or files.

Mitigation: Use environment variables or a secrets manager for real credentials and avoid storing raw tokens in shared configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junsheng428/skills/assistant-configurator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces configuration reports, model comparison guidance, configuration patch examples, restart/status commands, and API-key setup examples.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
