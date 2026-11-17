## Description:

Publish editorial and dynamic section content with blog-publish, enforce quality gates for hot/news/ai_news, and sync repository skills to ClawHub via clawhub sync --all.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:


## Use Case:

Developers, editors, and automation agents use this skill to publish or update editorial posts and hot/news/ai_news dynamic section content while applying source-grounded quality checks before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install and run an unpinned third-party publishing CLI with credentials that can publish content and sync skills.

Mitigation: Review and pin @leeguoo/blog-publish before installation, prefer a project-local install, use least-privileged publishing credentials, and confirm target site, locale, input files, and sync effects before real publish, update, upload, or sync commands.

Risk: Dynamic content could publish weakly sourced claims, repeated generic links, leaked placeholders, or internal producer identity.

Mitigation: Run the documented dry-run and markdown guardrails, verify Source, Evidence, Summary, Interpretation, and Action lines for each topic, and keep producer metadata out of public bylines, metadata, and body content.

## Reference(s):

- [Blog Content Publish on ClawHub](https://clawhub.ai/leeguooooo/skills/blog-content-publish)
- [Misonote blog publishing service](https://blog.misonote.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and content templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run checks, content quality gates, publishing rules, and failure handling guidance.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
