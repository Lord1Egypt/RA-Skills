## Description:

Manage all 32 Blog System (FastAPI) API endpoints for articles, tags, users, comments, messages, moods, uploads, health checks, blog pages, and admin operations through CLI subcommands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage a FastAPI Blog System through documented REST API and CLI workflows. It supports content management, user and comment operations, file upload management, health checks, public blog page retrieval, and admin article deletion after login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill reads unnecessary local credential fields from project metadata.

Mitigation: Review the workspace before installation, keep .project-info contents minimal, and avoid storing unrelated BLOG_MINI_KIT_MYS_* secrets in project metadata.

Risk: The security evidence reports that sensitive admin and upload traffic can be sent over plaintext HTTP.

Mitigation: Prefer HTTPS base URLs, especially for non-local Blog deployments and any workflow involving admin login, delete, or upload operations.

Risk: Admin delete and upload commands are high-impact operations.

Mitigation: Confirm the target base URL, resource identifiers, and intended operation before running admin delete or file upload commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/blog-mini-kit-mys)
- [API endpoint index](references/api-reference.md)
- [Articles API](references/articles.md)
- [Tags API](references/tags.md)
- [Users API](references/users.md)
- [Comments API](references/comments.md)
- [Messages API](references/messages.md)
- [Moods API](references/moods.md)
- [Uploads API](references/uploads.md)
- [Health API](references/health.md)
- [Blog pages API](references/pages.md)
- [Admin API](references/admin.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON by default, with optional Markdown tables and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may issue HTTP requests to the configured Blog System base URL and returns operation summaries suitable for issue or pull request comments.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
