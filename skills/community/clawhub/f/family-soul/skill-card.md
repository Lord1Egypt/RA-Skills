## Description:

Family Soul analyzes exported family or close-group chat logs and generates a collective soul.md plus individual persona Markdown files for agent personality grounding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengury](https://clawhub.ai/user/zengury)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn consented chat exports into Markdown personality context for agents, including a collective family or group profile and individual personas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private chat exports and includes a bundled chat export in the artifact.

Mitigation: Remove bundled chat data before installation and run only on chats collected with explicit consent and privacy review.

Risk: The release security guidance reports an exposed Kimi key in the artifact.

Mitigation: Remove the key, rotate it with the provider, and require credentials to come from environment configuration.

Risk: Generated soul and persona files may be installed into agents and can carry sensitive personal details from the source chat.

Mitigation: Review generated Markdown for sensitive details and get consent before installing generated personality files into an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengury/skills/family-soul)
- [ClawHub publisher profile](https://clawhub.ai/user/zengury)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files with shell command progress messages and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces soul.md and persona Markdown files from a user-provided chat export; uses LLM API credentials supplied by the runtime environment.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
