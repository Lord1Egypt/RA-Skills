## Description:

GameLegend helps agents discover and recommend games using GameLegend's Gameplay DNA engine across 1,100+ games and 69 gameplay dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipludington](https://clawhub.ai/user/philipludington)

### License/Terms of Use:

MIT-0

## Use Case:

External users and gaming communities use this skill to ask an agent for games like a specific title, personalized recommendations, and concise game DNA highlights based on mood, mechanics, or prior preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game-related queries and preference hints may be sent to GameLegend's public API.

Mitigation: Install only where users are comfortable with that data flow, and avoid sharing sensitive personal information in recommendation requests.

Risk: The skill may activate on broad game mentions rather than only explicit recommendation requests.

Mitigation: Use tighter trigger wording when the desired behavior is activation only for explicit game discovery or recommendation requests.

Risk: Recommendation quality depends on the public API's coverage and ranking data.

Mitigation: Present results as recommendations, include the GameLegend attribution, and refine follow-ups with user feedback.

## Reference(s):

- [GameLegend](https://gamelegend.com)
- [GameLegend Public API Documentation](https://gamelegend.com/docs/api)
- [GameLegend MCP Server](https://www.npmjs.com/package/@gamelegend/mcp)
- [ClawHub GameLegend Skill](https://clawhub.ai/philipludington/skills/gamelegend)
- [ClawHub Publisher Profile](https://clawhub.ai/user/philipludington)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown chat responses with game recommendations, similarity scores, DNA highlights, links, and GameLegend attribution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public GameLegend API results and user taste preferences to tailor recommendations; no API key is required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
