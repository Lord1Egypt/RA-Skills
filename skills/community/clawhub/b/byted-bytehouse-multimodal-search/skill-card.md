## Description:

Provides ByteHouse multimodal search guidance and Python helpers for vectorizing and retrieving text, image, and video content with ByteHouse and Volcengine Ark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure ByteHouse and Volcengine Ark embeddings for multimodal vector storage and hybrid retrieval across text, images, and video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can build database SQL from caller-controlled inputs without safe validation or clear scoping.

Mitigation: Use least-privileged ByteHouse credentials and validate or allowlist table names and filter conditions before execution.

Risk: The skill may send text or media to Ark and store derived data in ByteHouse.

Mitigation: Avoid sensitive or regulated content unless organizational policy approves that data flow.

Risk: The security guidance calls for dependency review before production use.

Mitigation: Pin and review Python dependencies in an isolated environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-bytehouse-multimodal-search)
- [ByteHouse vector search SQL documentation](https://www.volcengine.com/docs/6464/1208707)
- [Volcengine multimodal embeddings API documentation](https://www.volcengine.com/docs/82379/1409291)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment-variable setup guidance and Python helper usage examples; no fixed token cap is specified.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
