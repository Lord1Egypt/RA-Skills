## Description:

Turns a single long-tail query into a publish-ready SEO blog post bundle with research notes, clean HTML, metadata, structured data, AI-SEO checks, and optional publishing through Ghost, WordPress, or static-site output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, indie hackers, and content marketers use this skill to turn a specific blog topic into a draft-ready or publish-ready article package. It is intended for SEO-focused editorial workflows that need source research, HTML output, metadata, JSON-LD schema, and optional CMS publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can draft, schedule, or publish content through CMS integrations, which may expose a site to incorrect, misleading, or prematurely published material.

Mitigation: Use the static target or draft-only CMS mode by default, and require human editorial review before publication.

Risk: The security evidence notes unpinned third-party tools and optional MCP or Python dependencies.

Mitigation: Pin and review MCP and Python dependencies before running the workflow in a production publishing environment.

Risk: The security evidence notes administrator-level WordPress credential guidance.

Mitigation: Use a dedicated low-privilege Ghost or WordPress integration account with only the permissions needed for draft or publish actions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/automatelab/skills/ghost-blog-writer)
- [Project homepage from skill metadata](https://github.com/AutomateLab-tech/publishing-skills)
- [ai-seo-mcp reference](https://github.com/AutomateLab-tech/ai-seo-mcp)
- [glossary-schema.md](references/glossary-schema.md)
- [decorate.js](references/decorate.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce draft HTML, metadata JSON, JSON-LD schema blocks, research notes, refresh metadata, and CMS or static-site publishing guidance.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
