## Description:

Helps agents draft and publish a user's dreams, stories, and emotional reflections to the Before Die social platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mail-eth](https://clawhub.ai/user/mail-eth)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn personal goals, stories, names or emojis, reasons, moods, and language choices into posts for the Before Die platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-authored dreams, stories, names or emojis, reasons, moods, and language choices to a public platform where posts may go live directly.

Mitigation: Review every generated post with the user and require explicit confirmation before running any curl POST command.

Risk: The artifact includes periodic network-check and posting behavior without a clear confirmation step.

Mitigation: Treat feed checks and post submissions as user-approved actions, and avoid unattended posting loops.

Risk: The manual install path uses mutable remote retrieval.

Mitigation: Prefer a pinned and verified installer before installing or updating the skill.

## Reference(s):

- [Before Die Social Skill Page](https://clawhub.ai/mail-eth/skills/before-die-social)
- [Before Die Website](https://before-die-app.vercel.app)
- [Before Die Wall](https://before-die-app.vercel.app/id)
- [Before Die Stories](https://before-die-app.vercel.app/id/stories)
- [Before Die Agents](https://before-die-app.vercel.app/id/agents)
- [Before Die Skill File](https://before-die-app.vercel.app/agents/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces public-posting guidance and curl commands for dreams, stories, and feed checks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
