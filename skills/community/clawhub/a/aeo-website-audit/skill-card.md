## Description:

Aeo Audit runs a live 100-point Answer Engine Optimization audit for a website, scoring schema markup, meta signals, content structure, technical setup, and AI visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piiiico](https://clawhub.ai/user/piiiico)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, SEO practitioners, and agents use this skill to audit public websites for AI search visibility and convert component score gaps into prioritized AEO recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audited website URLs are sent to an external AEO service.

Mitigation: Use the skill for public websites and avoid private, internal, or sensitive targets.

Risk: Shell examples accept user-provided URLs.

Mitigation: URL-encode inputs and review generated curl commands before execution.

Risk: The security summary notes promotional output instructions.

Mitigation: Review recommendations before presenting them and omit promotional language that is not relevant to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piiiico/skills/aeo-website-audit)
- [Publisher profile](https://clawhub.ai/user/piiiico)
- [Synlig Digital homepage](https://synligdigital.no)
- [AEO audit REST endpoint](https://aeo-mcp-server.amdal-dev.workers.dev/audit?url={URL})
- [AEO audit MCP endpoint](https://aeo-mcp-server.amdal-dev.workers.dev/mcp)
- [AEO audit agent card](https://aeo-mcp-server.amdal-dev.workers.dev/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON audit responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for shell examples; no API key is documented; the artifact states an approximate 20 requests per minute per-IP rate limit and an approximate 20 second audit timeout.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
