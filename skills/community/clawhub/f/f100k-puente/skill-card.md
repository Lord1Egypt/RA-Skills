## Description:

Bridge guidance for running Formula 100K skills in an OpenClaw agent by mapping Claude Code and Mac-specific instructions to server-safe tools, workspace paths, Telegram delivery, and approval rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill before running Formula 100K skills in OpenClaw so the agent follows the user's workspace context, uses available server integrations, avoids logged-in social browsing, and asks for approval before spending credits or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private F100K workspace context and may use connected third-party services.

Mitigation: Install only when that workspace access and those service connections are acceptable for the deployment.

Risk: Research, scraping, media generation, deployment, and delivery steps can involve paid or external services.

Mitigation: Review previews and require approval before paid actions, public posting, or outbound delivery.

Risk: Gemini image generation can send prompts and selected photos to Google.

Mitigation: Avoid sending sensitive photos or prompts unless the user has approved that external processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/f100k-puente)
- [Formula 100K publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing operational bridge instructions; no standalone generated artifact is required.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
