## Description:

Manages a blog system REST API for articles, tags, users, comments, messages, moods, file uploads, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and blog operators use this skill to run read and write workflows against a configured blog REST API, including content publishing, comment and message management, file upload management, and service health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send passwords, personal data, and uploaded files over plaintext HTTP.

Mitigation: Install it only for a blog API you control, prefer HTTPS endpoints, avoid passing real passwords with --pwd, and do not upload sensitive local files unless the configured host is trusted.

Risk: Delete and admin-delete-articles commands are potentially destructive and the artifact does not add confirmation or rollback safeguards.

Mitigation: Review command arguments and target resources before execution, test read-only commands first, and keep backups or recovery procedures for managed blog content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/blog-kimi-test-kit)
- [Blog System REST API Reference](references/api-reference.md)
- [Test variables](templates/test-vars.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured BLOG_KIMI_TEST_KIT_BASE_URL and supports JSON output by default with optional Markdown tables for capability listings.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
