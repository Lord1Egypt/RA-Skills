## Description:

Manages 32 FastAPI blog-system API endpoints for article CRUD and recovery, popular posts, tags, users, comments, messages, moods, file uploads, admin operations, frontend pages, and health checks using curl and JSON examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage a configured FastAPI blog service through documented API calls. It supports read-only checks as well as content creation, update, upload, delete, restore, and admin bulk-delete workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Content changes, file uploads, delete actions, hard deletes, and admin bulk deletes can alter or remove blog data.

Mitigation: Install only for a trusted blog API that you administer and require explicit user confirmation before delete, hard-delete, upload-delete, or admin bulk-delete actions.

Risk: Admin login and token handling can expose credentials or tokens if they are placed directly in shell commands.

Mitigation: Prefer HTTPS, change any default admin credentials before use, and avoid placing passwords or tokens directly in shell commands.

Risk: The skill targets public unauthenticated API endpoints, so an incorrect base URL could affect the wrong service.

Mitigation: Confirm the BLOG_MINI_KIT_LIUFEI_BASE_URL value before execution and stop when permission or authorization errors occur.

## Reference(s):

- [API Reference](artifact/references/api-reference.md)
- [Test Variables](artifact/templates/test-vars.json)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, JSON, Markdown]

**Output Format:** [JSON or Markdown summaries with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLOG_MINI_KIT_LIUFEI_BASE_URL and may perform mutating operations against the configured blog API.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
