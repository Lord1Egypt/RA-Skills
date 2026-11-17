## Description:

Generate AI Music helps agents create vocal or instrumental AI-generated songs and audio tracks through MakeBestMusic and check generation status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sthk-mbm](https://clawhub.ai/user/sthk-mbm)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, musicians, and agents use this skill to turn song descriptions into vocal or instrumental AI-generated tracks and retrieve completion links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can send the user's API key and prompts to a non-official endpoint if MBM_API_BASE is set or inherited from an untrusted environment.

Mitigation: Run the skill only where MBM_API_BASE is unset or trusted, avoid confidential prompt text, and rotate the MakeBestMusic key if it was used with a non-official endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sthk-mbm/skills/generate-ai-music)
- [MakeBestMusic website](https://makebestmusic.com/?pid=PIDcLjhgCXUQ)
- [MakeBestMusic API endpoint](https://api.makebestmusic.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation requests return music IDs first, then status checks return pending, completed, or failed results with links when available.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
