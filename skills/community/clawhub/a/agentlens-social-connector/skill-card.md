## Description:

AgentLens Social Connector helps agents retrieve public social posts through the AgentLens API, summarize text and media, and save prepared notes to user-confirmed knowledge destinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inkad-code](https://clawhub.ai/user/inkad-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to read, summarize, analyze, and optionally save public social-media content from supported links without relying on social-account cookies or login sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Social-link URLs and their query parameters are sent to the third-party AgentLens service.

Mitigation: Use the skill only for public social URLs and avoid private, signed, internal, invitation, reset, or document links.

Risk: Fallback helpers can download media or write local notes when native destination tools are unavailable.

Mitigation: Prefer approved native tools, require explicit destination confirmation, and keep media downloads scoped to the current task.

Risk: Persistent API keys, destination settings, or workflow preferences could expose sensitive configuration if saved without clear consent.

Mitigation: Store credentials and destination metadata only in approved secret or configuration stores after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inkad-code/skills/agentlens-social-connector)
- [AgentLens homepage](https://agentlensapi.io/?utm_source=clawhub&utm_content=social_connector_skill)
- [AgentLens API reference](references/agentlens-api.md)
- [Media workflows](references/media-workflows.md)
- [Knowledge base workflows](references/knowledge-base-workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional JSON, code, shell commands, and knowledge-base-ready notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summaries, key points, transcript notes, media interpretation, source metadata, destination-save guidance, and current-task artifacts.]

## Skill Version(s):

0.1.2 (source: server release metadata); artifact frontmatter reports 2026.08.02

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
