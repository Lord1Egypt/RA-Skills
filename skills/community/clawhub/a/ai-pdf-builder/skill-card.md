## Description:

AI-powered PDF generator for legal docs, pitch decks, and reports. SAFEs, NDAs, term sheets, whitepapers. npx ai-pdf-builder. Works with Claude, Cursor, GPT, Copilot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:


## Use Case:

Developers and AI-agent users use this skill to generate professional PDFs, including legal documents, investor materials, reports, and proposals, from Markdown files, prompts, or existing documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running mutable npm code through unpinned npx commands may execute a package version that has not been reviewed.

Mitigation: Use a pinned, reviewed ai-pdf-builder version and avoid automatic execution of unpinned npx commands.

Risk: Legal, investor, and business documents may contain confidential information that is exposed through AI features.

Mitigation: Do not process confidential documents through AI features unless the configured provider and data handling are acceptable for that content.

Risk: The skill requires local tools and credentials that can broaden access if run with excessive permissions.

Mitigation: Run with least privilege, expose only needed input and output files, and provide only the required API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextfrontierbuilds/skills/ai-pdf-builder)
- [Publisher profile](https://clawhub.ai/user/nextfrontierbuilds)
- [npm package](https://www.npmjs.com/package/ai-pdf-builder)
- [Source repository linked in artifact](https://github.com/NextFrontierBuilds/ai-pdf-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or transform Markdown and PDF files through the referenced CLI or package.]

## Skill Version(s):

1.2.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
