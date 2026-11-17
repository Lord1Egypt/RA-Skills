## Description:

OpenClaw skill for Facebook Graph API workflows focused on Pages posting, comments, and Page management using direct HTTPS requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinkom-byte](https://clawhub.ai/user/kevinkom-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan Facebook Page publishing, comment moderation, webhook, permission, and token workflows with direct Graph API HTTPS requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Facebook credentials can be exposed through logs, source control, or query-string access tokens.

Mitigation: Store FB_APP_SECRET and FB_ACCESS_TOKEN in environment variables or a secrets manager, avoid logging them, rotate them after suspected exposure, and prefer Authorization headers.

Risk: Page publishing or moderation actions can affect live Facebook content, including hiding or deleting posts and comments.

Mitigation: Use the narrowest Page permissions possible and confirm target Page IDs, post IDs, and comment IDs before write, hide, or delete actions.

## Reference(s):

- [Facebook Graph API Overview](artifact/references/graph-api-overview.md)
- [Page Posting Guide](artifact/references/page-posting.md)
- [Comments and Moderation](artifact/references/comments-moderation.md)
- [Permissions and Tokens](artifact/references/permissions-and-tokens.md)
- [Webhooks (Pages)](artifact/references/webhooks.md)
- [HTTP Request Templates (Graph API)](artifact/references/http-request-templates.md)
- [Security and Secrets Management](artifact/references/security-and-secrets.md)
- [ClawHub Skill Page](https://clawhub.ai/kevinkom-byte/skills/facebook-secure)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline HTTP request examples, JSON payloads, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include permissions checklists, workflow plans, and operational guardrails for Facebook Page API actions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
