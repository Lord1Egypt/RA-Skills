## Description:

Content Publisher Pro helps agents prepare and publish Markdown articles to GitHub Pages and Dev.to with platform-specific content variants, SEO metadata, duplicate checks, and dry-run previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdsega](https://clawhub.ai/user/wdsega)

### License/Terms of Use:

MIT

## Use Case:

External developers, technical bloggers, and content operators use this skill to configure and run a Python publishing workflow for Markdown articles destined for GitHub Pages and Dev.to.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing requires GitHub and Dev.to credentials that may grant write access to public content destinations.

Mitigation: Use scoped tokens, keep real secrets out of tracked config files, prefer a secret manager or environment variables, and review permissions before publishing.

Risk: Summary and abstract modes can add a fixed blog link and promotional wording to public posts.

Mitigation: Run dry-run mode and review the generated article text before publishing, replacing or removing fixed promotional links as needed.

Risk: The workflow can publish, update, or duplicate public posts if article metadata or duplicate checks do not match the target platform state.

Mitigation: Confirm titles, target repository, and platform selection before execution, and test first with dry-run mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wdsega/skills/content-publisher-pro)
- [Publisher profile](https://clawhub.ai/user/wdsega)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, YAML configuration, Python command-line usage, and publishing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can make GitHub and Dev.to API calls when run with credentials; dry-run mode previews without publishing.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
