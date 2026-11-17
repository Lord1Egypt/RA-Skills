## Description:

Config Safe helps agents safely modify OpenClaw configuration by reading current documentation, previewing changes, validating configuration structure, and requiring explicit user confirmation before writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glfruit](https://clawhub.ai/user/glfruit)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to plan and apply configuration changes while reducing the risk of invalid settings that can prevent the Gateway from starting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed configuration changes can modify OpenClaw Gateway settings and trigger a Gateway restart.

Mitigation: Review the generated preview carefully and confirm only changes whose effects are understood.

Risk: Changes to channels, tokens, agents, or sandbox behavior can affect access, identity, or runtime behavior.

Mitigation: Validate the configuration schema and avoid confirming sensitive changes unless they are intentional.

## Reference(s):

- [Config Safe on ClawHub](https://clawhub.ai/glfruit/skills/config-safe)
- [OpenClaw Gateway configuration documentation](/opt/homebrew/lib/node_modules/openclaw/docs/gateway/configuration.md)
- [OpenClaw Gateway configuration examples](/opt/homebrew/lib/node_modules/openclaw/docs/gateway/configuration-examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires preview, validation, and explicit user confirmation before configuration writes.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-02-09T05:00:54Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
