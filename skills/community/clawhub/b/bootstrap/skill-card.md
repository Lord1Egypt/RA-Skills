## Description:

Generate a personalized SOUL.md through a warm, adaptive onboarding conversation for setting up or updating an AI partner's identity and behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanz](https://clawhub.ai/user/huanz)

### License/Terms of Use:


## Use Case:

External users use this skill to run a guided onboarding conversation that captures personal context, communication preferences, boundaries, and desired AI-partner behavior. After confirmation, the agent produces a concise personalized SOUL.md for local use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a local SOUL.md containing personal preferences, identity details, boundaries, and behavioral instructions.

Mitigation: Review the generated SOUL.md before saving, remove sensitive details that are not needed, and keep the local memory file only in workspaces where that profile should persist.

Risk: The generated profile may encourage future conversations, personal follow-up questions, and increasing assistant autonomy beyond the user's comfort level.

Mitigation: Edit the Growth and behavior sections before confirmation so autonomy, follow-up, and learning instructions match the user's intended boundaries.

## Reference(s):

- [Bootstrap Skill Page](https://clawhub.ai/huanz/skills/bootstrap)
- [Conversation Guide](artifact/references/conversation-guide.md)
- [SOUL.md Template](artifact/templates/SOUL.template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational text with a generated Markdown SOUL.md and local save instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated SOUL.md is intended to stay under 300 words and is saved only after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
