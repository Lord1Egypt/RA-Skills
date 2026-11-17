## Description:

fboc helps agents manage Facebook Pages through CLI commands for listing, creating, scheduling, hiding, and deleting posts and comments via the Facebook Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phuongsky](https://clawhub.ai/user/phuongsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent configure Facebook Page credentials, test access, and manage Page content from terminal workflows. It is suited to publishing, scheduling, reviewing, hiding, or deleting Facebook Page posts when the operator has approved credentials and content changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, schedule, hide, or delete live Facebook Page content.

Mitigation: Use a test Page first, manually review commands before execution, and require explicit confirmation for destructive actions.

Risk: The skill requires a Facebook Page token with permissions that can modify Page content.

Mitigation: Use least-privilege Page tokens, avoid pasting tokens into chats or shell history, store credentials securely, and rotate any token used with this version.

Risk: Automated test or cron examples can affect a production Page if run with production credentials.

Mitigation: Run tests and scheduled jobs only against reviewed Page IDs and tokens, and avoid production cron jobs without manual approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phuongsky/skills/facebook-openclaw)
- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api)
- [Facebook Pages API](https://developers.facebook.com/docs/graph-api/reference/page)
- [Facebook Page Posts API](https://developers.facebook.com/docs/graph-api/reference/page/posts)
- [Facebook Post Comments API](https://developers.facebook.com/docs/graph-api/reference/post/comments)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Facebook Graph API actions that modify live Page content when executed with valid Page credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
