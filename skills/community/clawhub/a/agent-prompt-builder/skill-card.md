## Description:

Stop writing system prompts by hand -- let structured identity generate them automatically from beliefs and responsibilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect an agent to the Live Neon platform, manage structured beliefs and responsibilities, and fetch a generated system prompt for use with an LLM. It also provides workflows for syncing content, discovering identity signals, reviewing proposed beliefs, and tracking prompt changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Neon may receive and process agent identity data, imported content-source material, and conversation-derived observations.

Mitigation: Use the skill only with appropriate user and organization consent, review and redact payloads before upload, and avoid sending sensitive data that is not needed for prompt generation.

Risk: Generated prompt text and approved beliefs can change agent behavior after remote processing.

Mitigation: Review pending beliefs, responsibilities, and generated prompts before deployment; keep a rollback path and token-revocation plan.

Risk: Proactive observation, approve-all, consensus promotion, and scheduled heartbeat workflows can amplify unreviewed identity changes.

Mitigation: Keep those workflows disabled unless users opt in and payloads are reviewed; prefer manual approval for production agents.

## Reference(s):

- [Agent Prompt Builder on ClawHub](https://clawhub.ai/liveneon/skills/agent-prompt-builder)
- [Live Neon Persona Platform](https://persona.liveneon.ai)
- [Live Neon](https://liveneon.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, JSON, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require LIVE_NEON_TOKEN, LIVE_NEON_BASE, and an active Live Neon account to execute workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
