## Description:

Manages a public FastAPI blog API for articles, tags, users, comments, messages, mood posts, file uploads, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage a controlled FastAPI blog service, including publishing and updating content, moderating comments and messages, managing tags and users, checking service health, and uploading files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live public blog content and delete or restore records.

Mitigation: Use it only against a blog API you control and require explicit human confirmation before create, update, delete, restore, account creation, or hard-delete operations.

Risk: The skill can upload local files to the configured blog API.

Mitigation: Confirm each file path and file contents before upload, and avoid sensitive local paths.

Risk: The API is documented as unauthenticated while the script scans BLOG_BIG_KIMI_KIT-prefixed credential-like variables.

Mitigation: Do not store credentials under the BLOG_BIG_KIMI_KIT prefix for this no-auth API; configure only BLOG_BIG_KIMI_KIT_BASE_URL and prefer HTTPS.

## Reference(s):

- [API endpoint documentation](artifact/api-reference.md)
- [Test cases](artifact/test-vars.json)
- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/blog-big-kimi-kit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON by default, with optional Markdown tables and issue-comment Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue live HTTP requests against the configured blog API and may create, update, delete, restore, or upload content.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
