## Description:

Felo Mindmap creates shareable mindmaps from prompts using the Felo Mindmap API, with supported layouts and optional LiveDoc integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in Claude Code to turn a topic, question, meeting notes, or project outline into a Felo-hosted mindmap. It is intended for mindmap generation tasks and supports layout selection plus optional LiveDoc attachment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's mindmap prompt and FELO_API_KEY-backed request to Felo's API.

Mitigation: Avoid sending secrets, regulated data, or confidential notes unless the user is comfortable sharing them with Felo.

Risk: Security evidence reports an undocumented FELO_API_BASE endpoint override that can redirect the API key and mindmap prompt to another server.

Mitigation: Use the skill only where FELO_API_BASE is unset or tightly controlled, and prefer removing or validating the endpoint override before release.

## Reference(s):

- [Felo Mindmap API](https://openapi.felo.ai/docs/api-reference/v2/mindmap.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/felo-mindmap)
- [Project homepage](https://github.com/Felo-Inc/felo-skills)
- [Project support](https://github.com/Felo-Inc/felo-skills/issues)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown result with optional JSON fields from the Felo API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a mindmap_url on success and structured error guidance on failure.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
