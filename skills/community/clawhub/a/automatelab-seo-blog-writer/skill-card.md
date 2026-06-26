## Description: <br>
Turn a single long-tail query into a publish-ready blog post that ranks in search and gets quoted by AI assistants by classifying the topic, researching real sources, drafting clean HTML, auditing AI-SEO structure, and preparing a Ghost, WordPress, or static-site publishing bundle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, founders, content marketers, and developer-marketing teams use this skill to turn a focused search query into a reviewed blog draft or publishing bundle. It supports static-site output by default and can publish through Ghost or WordPress adapters when credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing adapters can use sensitive Ghost or WordPress credentials. <br>
Mitigation: Configure least-privilege integrations where possible, keep admin keys and application passwords out of git, and install the skill only for agents trusted to create blog drafts or posts. <br>
Risk: Generated drafts may contain private material or content that should not go live without editorial review. <br>
Mitigation: Review generated drafts before using publish or schedule flags, and periodically clean tmp/blog-drafts when drafts may include private material. <br>
Risk: Live or scheduled publishing can make content public through the connected platform. <br>
Mitigation: Use the default draft flow for normal operation and reserve publish or publish-at flags for posts that have passed review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/automatelab/automatelab-seo-blog-writer) <br>
- [Publisher Profile](https://clawhub.ai/user/automatelab) <br>
- [Glossary Schema Reference](references/glossary-schema.md) <br>
- [Glossary Tooltip Decorator](references/decorate.js) <br>
- [ai-seo MCP](https://github.com/AutomateLab-tech/ai-seo-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files, API calls] <br>
**Output Format:** [Markdown guidance with HTML, JSON, JSON-LD, and shell command snippets; generated post bundles include draft HTML, schema HTML, metadata JSON, and optional image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a static draft bundle; Ghost and WordPress publishing paths require platform credentials and default to draft unless publish flags are used.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
