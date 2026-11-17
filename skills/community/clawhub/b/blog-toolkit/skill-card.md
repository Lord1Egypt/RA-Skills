## Description:

blog-toolkit manages Blog System API v1.0.0 content, users, comments, messages, moods, uploads, and health checks through 27 unauthenticated CLI subcommands that return JSON or Markdown tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to inspect and manage a Blog System API instance from an agent-driven CLI, including creating, updating, uploading, and deleting blog resources after confirming the target endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, modify, upload, and delete public blog data through an unauthenticated API.

Mitigation: Use only trusted Blog API endpoints, prefer non-production or least-privileged protected deployments, and require human approval before create, update, upload, or delete operations.

Risk: A wrong or untrusted base URL could direct management commands at an unintended service.

Mitigation: Confirm BLOG_TOOLKIT_BASE_URL or project knowledge before running commands and prefer HTTPS endpoints.

Risk: File upload commands may expose sensitive local files or publish unintended content.

Mitigation: Review file paths before upload and avoid passing sensitive files or passwords through commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/blog-toolkit)
- [Blog System API v1.0.0 endpoint documentation](artifact/api-reference.md)
- [Test command variables](artifact/test-vars.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands; invoked commands return JSON by default or Markdown tables when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses BLOG_TOOLKIT_BASE_URL or project knowledge to select the target API endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
