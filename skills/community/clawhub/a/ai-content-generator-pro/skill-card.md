## Description:

AI Content Generator Pro is an OpenClaw content creation skill for generating, optimizing, scheduling, analyzing, and exporting blog, social, email, product, ad, and script content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacealllc](https://clawhub.ai/user/jacealllc)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, business owners, agencies, and developers use this skill to draft marketing and editorial content, plan content calendars, optimize readability and SEO, and export files for downstream publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be stored in local configuration files.

Mitigation: Move real credentials to a secret manager or environment-backed configuration and keep release config files redacted.

Risk: Content optimization, analysis, and export commands can read from and write to caller-supplied local paths.

Mitigation: Run the skill in a constrained workspace, review file paths before execution, and grant only the read and write permissions needed for the task.

Risk: HTML export can include generated or user-provided content without escaping or sanitization.

Mitigation: Treat exported HTML as unsafe until content is escaped or sanitized before opening, publishing, or sharing.

Risk: Requested exec and web permissions increase installation risk when they are not needed for a specific workflow.

Mitigation: Disable unused permissions and review setup, test, and runtime commands before granting execution or network access.

## Reference(s):

- [AI Content Generator Pro on ClawHub](https://clawhub.ai/jacealllc/skills/ai-content-generator-pro)
- [JacealLLC Publisher Profile](https://clawhub.ai/user/jacealllc)
- [API Documentation](references/api-docs.md)
- [Market Research](references/market-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses, with generated files in Markdown, HTML, PDF, or DOCX-like formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated and optimized content is written to local files; configuration controls model provider, tone, SEO settings, and brand voice options.]

## Skill Version(s):

1.0.1 (source: server release evidence, target metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
