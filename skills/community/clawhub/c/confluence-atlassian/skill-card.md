## Description:

Full-featured Confluence Cloud REST API v2 skill for managing pages, spaces, blog posts, attachments, comments, labels, and other Confluence content through direct API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersonling1217-png](https://clawhub.ai/user/jeffersonling1217-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to have an agent prepare Confluence Cloud REST API v2 requests for creating, reading, updating, deleting, searching, and organizing Confluence content. It is suited to authenticated Confluence administration and content-management workflows that require direct API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide powerful Confluence operations such as admin-key changes, invites, deletion, purge, redaction, and space modification.

Mitigation: Require explicit user confirmation before any admin-key, invite, delete, purge, redaction, or space-modifying action.

Risk: Authenticated API calls depend on an Atlassian API token that could expose Confluence access if pasted into commands, logs, or shared transcripts.

Mitigation: Use a least-privilege Atlassian API token stored in environment variables, and avoid emitting secrets in command text or logs.

Risk: The security verdict is suspicious because the artifact documents high-impact actions without enough built-in guardrails.

Mitigation: Install only for workflows that require direct Confluence Cloud API calls, and review generated requests before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffersonling1217-png/skills/confluence-atlassian)
- [ClawHub release homepage](https://clawhub.ai/jeffersonling1217-png/confluence-atlassian)
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN, and CONFLUENCE_DOMAIN environment variables for authenticated Confluence Cloud API use.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
