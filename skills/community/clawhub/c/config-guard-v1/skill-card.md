## Description:

Config Guard helps agents modify OpenClaw configuration by backing up the current file, previewing intended changes, validating JSON, and requiring explicit user confirmation before edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill when an agent needs to update ~/.openclaw/openclaw.json for model, channel, tool, or skill configuration changes. It structures the workflow around backup, preview, JSON validation, and explicit approval before modification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised redaction can expose API keys or tokens in terminal output or logs.

Mitigation: Review the skill before installing, do not share preview or sanitize output, and use structural jq-based redaction before displaying configuration.

Risk: Configuration edits can damage OpenClaw behavior if applied without validation or review.

Mitigation: Use a minimal non-sensitive diff, validate JSON, write through a secure temporary file in the config directory, and require clear user confirmation before modifying or restarting OpenClaw.

## Reference(s):

- [OpenClaw Common Configuration Examples](references/examples.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Config Guard on ClawHub](https://clawhub.ai/justaboyhai-wq/skills/config-guard-v1)
- [Publisher Profile](https://clawhub.ai/user/justaboyhai-wq)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted previews, validation results, and confirmation-gated edit steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
