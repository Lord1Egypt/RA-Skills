## Description:

OpenClaw skill that provides a WordPress REST API CLI for posts, pages, categories, tags, users, and custom requests using plain HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akkualle](https://clawhub.ai/user/akkualle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to manage WordPress posts, pages, categories, tags, user reads, and custom REST API requests from a Node.js CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can create, edit, or delete live WordPress content when provided credentials with sufficient permissions.

Mitigation: Use a dedicated low-privilege WordPress account, stage changes as drafts first, and review delete or raw request commands before execution.

Risk: WordPress credentials may be sent over non-HTTPS if WP_BASE_URL is misconfigured.

Mitigation: Configure only an HTTPS WP_BASE_URL and avoid logging or committing tokens, application passwords, or JWTs.

## Reference(s):

- [WordPress REST API Guide](assets/wordpress-rest-api-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/akkualle/skills/akkualle-wordpress-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and CLI output as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI writes JSON to stdout and uses non-zero exit codes on errors.]

## Skill Version(s):

1.0.0 (source: release metadata, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
