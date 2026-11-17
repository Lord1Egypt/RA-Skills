## Description:

Convert Markdown files to styled PDF or EPUB ebook using md-bookify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielefavi](https://clawhub.ai/user/danielefavi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation authors use this skill to convert Markdown files into styled PDF documents or EPUB ebooks with md-bookify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs npx-based Markdown conversion tools, which carry ordinary npm and Puppeteer supply-chain and browser-installation exposure.

Mitigation: Run it in trusted workspaces, validate selected Markdown paths and metadata, and review npm/Puppeteer exposure before use in sensitive environments.

## Reference(s):

- [md-bookify npm package](https://www.npmjs.com/package/md-bookify)
- [Bookify skill page](https://clawhub.ai/danielefavi/skills/bookify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and conversion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to produce PDF or EPUB files from selected Markdown inputs.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
