## Description:

Agent self-awakening onboarding protocol for forming an agent identity through conversation when Mupengism is first installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to onboard a newly installed Mupengism/OpenClaw-based agent through a short identity-forming conversation. The workflow guides the agent to create SOUL.md, SELF.md, and USER.md after user review and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or later influence persistent agent identity and behavior files through broad onboarding triggers.

Mitigation: Install only in workspaces where persistent agent identity files are intended, and review generated SOUL.md, SELF.md, and USER.md carefully before saving.

Risk: Generated identity files could be used to weaken safety expectations or expand tool permissions if treated as policy configuration.

Mitigation: Keep generated files limited to identity, relationship, and communication preferences; avoid placing tool permissions or safety-policy changes in them.

Risk: The workflow instructs the agent to delete BOOTSTRAP.md after onboarding.

Mitigation: Back up BOOTSTRAP.md before running the workflow if that file needs to be preserved.

## Reference(s):

- [SOUL-TEMPLATE.md](artifact/references/SOUL-TEMPLATE.md)
- [ClawHub Skill Page](https://clawhub.ai/mupengi-bot/skills/awakening-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Conversational guidance and Markdown identity files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SOUL.md, SELF.md, and USER.md previews for user confirmation before saving.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
