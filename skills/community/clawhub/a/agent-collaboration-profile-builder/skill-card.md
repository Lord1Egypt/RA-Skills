## Description:

Helps an agent guide users through a questionnaire and synthesize cognitive style, output preferences, value orientation, and collaboration protocol into reusable Markdown profile files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lakendocean](https://clawhub.ai/user/lakendocean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn repeated prompting preferences or messy self-descriptions into an agent-readable collaboration profile for OpenClaw or other agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated profiles may carry personal work preferences, values, and collaboration rules into future agent sessions.

Mitigation: Review the profile before reuse and avoid including private details that should not be carried across AI sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lakendocean/skills/agent-collaboration-profile-builder)
- [Questionnaire v1](references/questionnaire-v1.md)
- [Inference Rules](references/inference-rules.md)
- [Output Schema](references/output-schema.md)
- [Templates](references/templates.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown profile files, usually AI_USER_PROFILE.md with optional USER.md, WORKSTYLE.md, and COLLAB_PROTOCOL.md variants]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include partial profiles with Known Unknowns when the questionnaire is incomplete.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
