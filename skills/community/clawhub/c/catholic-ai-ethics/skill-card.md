## Description:

Provides a Catholic AI ethics framework and ready-to-paste assistant prompts centered on human dignity, with principles and source tracing for families and agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achurchai](https://clawhub.ai/user/achurchai)

### License/Terms of Use:

MIT-0

## Use Case:

Families and assistant builders use this skill to configure AI guidance around Catholic social principles, generate system prompts in 15 languages, and trace those principles to cited passages. It is an application of Catholic teaching, not official Church teaching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP setup runs an unpinned npm package.

Mitigation: Review the package source or pin a known version before running the MCP command; use the public text endpoints instead when MCP is unnecessary.

## Reference(s):

- [Magnifica Family](https://magnifica.family)
- [Principles catalog](https://magnifica.family/api/principles.json)
- [Default compass prompt](https://magnifica.family/api/compass/default)
- [Principle traceability](https://magnifica.family/api/traceability)
- [Magnifica Family MCP Registry listing](https://registry.modelcontextprotocol.io/v0/servers/io.github.a-church-ai/magnifica-family)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Plain-text system prompts and Markdown guidance with example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts support 15 languages, compact/default/full tiers, and adult, teenager, or child guidance in the full tier.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
