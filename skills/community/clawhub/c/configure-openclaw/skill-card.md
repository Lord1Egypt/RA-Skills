## Description:

Helps agents safely propose and apply validated OpenClaw configuration changes across openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onenameneo](https://clawhub.ai/user/onenameneo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to update OpenClaw settings, troubleshoot configuration errors, and generate minimal JSON5 patches for user-confirmed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or malformed OpenClaw configuration can prevent startup.

Mitigation: Review the proposed minimal JSON5 patch before confirming any write.

Risk: Changes involving auth, browser profiles, gateway exposure, hooks, cron, tools, sandbox, plugins, skills, or environment variables can affect security posture.

Mitigation: Apply only requested fields and verify sensitive sections against OpenClaw documentation before confirming.

Risk: Unknown fields or guessed values can create invalid configuration.

Mitigation: Fetch live OpenClaw documentation for unfamiliar fields before generating a patch.

## Reference(s):

- [OpenClaw configuration overview](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw configuration examples](https://docs.openclaw.ai/gateway/configuration-examples)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with minimal JSON5 patches and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before writing configuration changes.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
