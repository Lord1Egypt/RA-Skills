## Description:

Helps users troubleshoot gateway configuration changes that are lost after restart, including safer file-writing checks and validation of model IDs before persisting multi-model configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2070super](https://clawhub.ai/user/2070super)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when gateway configuration files revert after restart or when multi-model configuration needs to be written and validated against API model IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to overwrite gateway configuration files without enough safeguards.

Mitigation: Require explicit user confirmation, back up the existing configuration, use a scoped real path, and keep a rollback plan before restart.

Risk: Invalid model IDs or configuration syntax can cause the gateway to reject changes and restore previous configuration.

Mitigation: Validate model IDs against the API and check configuration syntax before writing or restarting the gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2070super/skills/configure-file-write-and-recovery)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language troubleshooting guidance for persistent gateway configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
