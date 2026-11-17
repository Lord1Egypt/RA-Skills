## Description:

Audits URLs for AI citation eligibility, diagnoses why AI systems may not cite a page, scores AI Overview and citation worthiness, generates or validates llms.txt, and drafts AEO/GEO fixes without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO practitioners, and content teams use this skill to audit pages for AI citation blockers, inspect technical SEO signals, and generate practical fixes for AEO, GEO, schema, crawler access, canonical hygiene, and llms.txt coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup uses an npm package that can change over time if installed without a pinned version.

Mitigation: Pin @automatelab/ai-seo-mcp to a reviewed exact version and verify the npm and GitHub publisher before installation.

Risk: URL-based SEO audits require network access and may produce recommendations that affect public content.

Mitigation: Run the MCP server with only the filesystem, environment, and network access needed for the audit, and review generated recommendations before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/automatelab/skills/automatelab-ai-seo)
- [Project Homepage](https://github.com/AutomateLab-tech/ai-seo-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured findings, inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked URL audit findings, prioritized fixes, llms.txt content, rewritten page sections, and MCP setup configuration.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
