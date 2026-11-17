## Description:

Routes Telegram group @mentions for a design-framework generation suite to the appropriate companion skill based on current task state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[807209066](https://clawhub.ai/user/807209066)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this OpenClaw skill as the Telegram-facing router for a four-skill design generation workflow. It listens for configured group mentions, checks workflow state, and routes work to builder, confirmation, or image generation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads stored OpenRouter and Telegram credentials.

Mitigation: Install only in a trusted environment, restrict access to the OpenClaw configuration file, limit bot permissions, and rotate credentials after testing or suspected exposure.

Risk: The skill sends text, generated prompts, and images to external OpenRouter and Telegram services.

Mitigation: Avoid processing sensitive source material, confirm recipients before enabling automation, and document the external services involved for users.

Risk: Helper scripts can forward local file contents or images to caller-supplied Telegram targets.

Mitigation: Restrict accepted file paths and destination IDs, run the skill with least privilege, and review outbound messages before use on shared systems.

Risk: Evidence.security flags unsafe shell/Python handling.

Mitigation: Fix quoting and input validation issues, replace shell interpolation with structured argument passing where possible, and re-scan before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/807209066/skills/design-framework-sender)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Telegram messages, generated image files, local state files, and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on OpenClaw Telegram and OpenRouter configuration plus companion design-framework skills.]

## Skill Version(s):

2.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
