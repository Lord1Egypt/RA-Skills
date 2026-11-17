## Description:

Moderate text, images, and video using Vettly's content moderation API via MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[code-with-brian](https://clawhub.ai/user/code-with-brian)

### License/Terms of Use:


## Use Case:

Developers and content operations teams use this skill to moderate user-generated text, image, and video content against Vettly policies, validate policy YAML, audit recent moderation decisions, and monitor usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moderated content is sent to an external Vettly service.

Mitigation: Use the skill only for content approved for Vettly processing, and avoid passing secrets or regulated data unless that processing is authorized.

Risk: The MCP setup runs an unpinned npm package.

Mitigation: Confirm trust in @vettly/mcp before installation and pin a reviewed package version where possible.

Risk: Recent moderation decisions may contain sensitive moderation data.

Mitigation: Limit access to decision-review outputs and handle them as potentially sensitive operational records.

Risk: The integration requires a Vettly API key.

Mitigation: Use a dedicated, revocable API key and rotate it if the skill configuration or environment is exposed.

## Reference(s):

- [Vettly](https://vettly.dev)
- [ClawHub Content Moderation](https://clawhub.ai/code-with-brian/skills/content-moderation)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON configuration snippets and tool-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include moderation assessments, policy validation results, usage summaries, and recent decision reviews.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
