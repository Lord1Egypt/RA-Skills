## Description:

Turn a single long-tail query into a publish-ready blog post by classifying the topic, researching real sources, drafting clean HTML, auditing AI-SEO structure, and preparing publication through Ghost, WordPress, or static-site output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, indie hackers, content marketers, and developers use this skill to turn a specific long-tail topic into a reviewed blog-post bundle. It is suited for draft-first publication workflows where a human reviews source grounding, SEO structure, CMS settings, and publishing credentials before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may use unpinned external installs or unbundled publishing scripts that interact with CMS accounts.

Mitigation: Review and pin optional dependencies, inspect local scripts before use, and run static or draft-only output until the generated post and platform settings are confirmed.

Risk: Publishing adapters may require CMS credentials and can create or publish content through Ghost or WordPress.

Mitigation: Use least-privilege CMS credentials and avoid live publish flags unless a human has reviewed the generated post, metadata, and target platform configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/automatelab/skills/automatelab-seo-blog-writer)
- [Publishing Skills Repository](https://github.com/AutomateLab-tech/publishing-skills)
- [ai-seo-mcp README](https://github.com/AutomateLab-tech/ai-seo-mcp)
- [glossary-schema.md](references/glossary-schema.md)
- [decorate.js](references/decorate.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JSON-LD, JSON metadata, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft-first blog publishing artifacts such as clean HTML, schema blocks, metadata, research notes, and platform adapter commands.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
