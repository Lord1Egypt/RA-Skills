## Description:

Manages a public Blog System REST API through CLI commands for articles, labels, users, comments, messages, moods, uploads, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage a Blog System instance from an agent workflow, including content, users, comments, messages, file uploads, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fall back to a hard-coded HTTP endpoint while supporting uploads, passwords, and destructive API actions.

Mitigation: Install only when the publisher is trusted, configure BLOG_MANAGER_KIT_BASE_URL to a trusted HTTPS or local endpoint before use, and avoid sending passwords, personal data, or local files through the default configuration.

Risk: Delete, hard-delete, upload, and Issue/PR comment actions can modify remote state or publish visible content.

Mitigation: Require explicit human review before these actions and confirm the target endpoint, operation, and content before execution.

## Reference(s):

- [Blog System API endpoint reference](artifact/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/blog-manager-kit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses, Markdown tables, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Issue or PR comment summaries prefixed with [blog-manager-kit].]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
