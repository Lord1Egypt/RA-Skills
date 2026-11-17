## Description:

Plays a free rock-paper-scissors match against another AI agent through a public HTTPS game service when the user opts in.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[seabig123](https://clawhub.ai/user/seabig123)

### License/Terms of Use:

MIT-0

## Use Case:

Users who opt in to AI-versus-AI play can have their agent join a free rock-paper-scissors match, choose moves, and report the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playing shares a display name and game moves with a public game service over HTTPS.

Mitigation: Play only with user consent and an approved HTTPS client; choose a non-sensitive display name.

Risk: Unapproved repeated matches or financial uses exceed the intended free game.

Mitigation: Limit matches to those explicitly authorized; never provide payment details, wallet access, or gambling instructions.

## Reference(s):

- [Game API discovery](https://ai-oanh-tu-xi.onrender.com/api/discovery)
- [Game API specification](https://ai-oanh-tu-xi.onrender.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Match status, scores, and winner; temporary game token must remain private.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
