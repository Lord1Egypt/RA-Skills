## Description: <br>
Turns a single long-tail query into a publish-ready SEO blog post bundle with research, clean HTML, AI-SEO audit artifacts, JSON-LD, and optional Ghost, WordPress, or static-site publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content marketers, founders, and indie hackers use this skill to turn a specific search query into a reviewed blog post draft or publishable CMS/static-site bundle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CMS publishing credentials can allow the agent to create, schedule, or publish content on the selected platform. <br>
Mitigation: Use limited Ghost or WordPress application credentials where possible and keep the default draft flow for human review before going live. <br>
Risk: Generated SEO content can contain stale facts, weak sourcing, or misleading claims if research and audit steps are skipped. <br>
Mitigation: Run the documented source, freshness, and AI-SEO checks, then review the draft and metadata before publishing. <br>
Risk: Optional MCP or helper package installation adds third-party code to the workflow. <br>
Mitigation: Inspect optional helper scripts and MCP/package installs before enabling those steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/automatelab/ghost-blog-writer) <br>
- [ai-seo-mcp README](https://github.com/AutomateLab-tech/ai-seo-mcp) <br>
- [glossary-schema.md](references/glossary-schema.md) <br>
- [decorate.js](references/decorate.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, HTML draft artifacts, JSON metadata, and JSON-LD schema blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a draft-oriented blog bundle; publishing requires an explicit target adapter and, for CMS targets, user-provided credentials.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
