## Description:

Automatically switches to backup models when token usage is exhausted or API rate limits are encountered, and notifies the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei-wei-zhao](https://clawhub.ai/user/wei-wei-zhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor token usage and rate-limit conditions, then switch model routing to a configured backup model when thresholds are reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change active model routing through an OpenClaw gateway token.

Mitigation: Review configured fallback models, costs, data-handling expectations, and heartbeat behavior before enabling automatic switching.

Risk: The gateway token may be sent over unencrypted HTTP if the gateway URL is configured that way.

Mitigation: Use a local-only gateway or HTTPS gateway, protect OPENCLAW_GATEWAY_TOKEN, and rotate the token if exposed.

Risk: Automatic fallback models may have different compliance, cost, or quality characteristics than the primary model.

Mitigation: Approve each fallback model in config.yaml before deployment and monitor switch status and history after activation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wei-wei-zhao/skills/auto-model-switch)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, status text, and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local model-switch state and switch-history files when run.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
