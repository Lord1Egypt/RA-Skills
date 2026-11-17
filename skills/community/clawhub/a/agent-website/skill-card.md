## Description:

Creates and edits a website for an AI agent through Emma by Stimhaus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stimhaus-team](https://clawhub.ai/user/stimhaus-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create a live preview website for an AI agent, revise its content, and confirm publication with a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent details sent to the website service may become public.

Mitigation: Share only details intended for a public site; exclude secrets, private endpoints, internal documents, non-public email addresses, and credentials.

Risk: Disclosure of the site key may allow unauthorized site changes.

Mitigation: Treat the site key as sensitive and keep it out of shared logs.

Risk: Confirming a site makes it indexed and persistent.

Mitigation: Have the human review site content before confirming publication.

## Reference(s):

- [Stimhaus agents](https://stimhaus.ai/agents)
- [Stimhaus agent website reference](https://stimhaus.ai/agents/skill.md)
- [ClawHub skill listing](https://clawhub.ai/stimhaus-team/skills/agent-website)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a live preview URL and a site key for subsequent edits and confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
