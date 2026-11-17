## Description:

Add a new OpenClaw Agent, automatically configure openclaw.json, create workspace, copy auth and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owen-ai-01](https://clawhub.ai/user/owen-ai-01)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to add an isolated OpenClaw agent with a dedicated Telegram bot, generated persona files, copied auth context, and updated agent-to-agent configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: New agents inherit the main agent's auth profiles, skills, and user context, which can broaden access beyond the intended scope.

Mitigation: Use the skill only when inherited access is intentional, prefer separate credentials per agent, and review copied auth and user context before deployment.

Risk: The skill edits core openclaw.json configuration and enables broad session visibility.

Mitigation: Keep a known-good backup outside the automated restore path, validate agent IDs and Telegram IDs strictly, and review the exact openclaw.json diff before applying it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and Markdown code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational setup steps, generated file contents, validation guidance, and restart and verification instructions.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
