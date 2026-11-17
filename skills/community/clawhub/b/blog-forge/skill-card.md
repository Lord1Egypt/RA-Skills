## Description:

Blog Forge helps agents generate SEO-oriented blog drafts, readability metadata, image suggestions, platform-formatted content, and optional draft publishing workflows for Medium, WordPress, Ghost, Dev.to, and Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers, content teams, and publishing-focused agents can use Blog Forge to turn topics and style settings into draft blog content with SEO metadata, readability analysis, suggested images, and platform-specific formatting. Users can also configure publishing credentials to create draft posts on supported blogging platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, drafts, and API keys may be sent to configured external model or publishing providers.

Mitigation: Use only trusted providers, prefer narrowly scoped tokens, and review provider settings before running generation or publishing flows.

Risk: Publishing credentials can be sent over plaintext HTTP when WordPress or Ghost URLs are configured that way.

Mitigation: Use HTTPS-only WordPress and Ghost URLs and avoid passing credentials to unencrypted endpoints.

Risk: Humanization features may be used to obscure AI involvement where disclosure is required.

Mitigation: Review generated drafts and follow applicable platform, organizational, and legal disclosure requirements before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/blog-forge)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JavaScript objects containing blog content, titles, SEO metadata, image prompts, readability scores, formatted Markdown or HTML, and publishing results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated drafts should be reviewed before publication; publishing integrations use user-supplied provider credentials.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
