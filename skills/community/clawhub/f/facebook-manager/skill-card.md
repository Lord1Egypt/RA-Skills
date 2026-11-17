## Description:

Facebook Manager helps agents manage Facebook Page and User Token workflows with guidance for Page posting, comment replies, Messenger replies, insights, group reading, page search, public post search, and access-token setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustydev212](https://clawhub.ai/user/trustydev212)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Facebook Page and User access tokens, then get API guidance, shell commands, and configuration examples for Facebook Page management, Messenger replies, insights, group workflows, and public search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful long-lived Facebook Page and User tokens can enable posting, messaging, reading, deletion, or account access if exposed.

Mitigation: Use only the minimum Meta scopes needed, avoid pasting tokens into chats or logs, store tokens outside plaintext configuration when possible, and restrict access to the runtime environment.

Risk: Generated Graph API calls can post, delete, reply, or send Messenger messages on behalf of a Page.

Mitigation: Require manual confirmation before any post, deletion, comment reply, or Messenger send, and review targets and message content before execution.

Risk: The token refresh example updates local OpenClaw configuration and may be unsafe on shared or sensitive systems.

Mitigation: Treat the cron refresh example as illustrative and replace it with an approved secret-management workflow before operational use.

## Reference(s):

- [Setup Guide](artifact/references/setup-guide.md)
- [Facebook Graph API Reference](artifact/references/api-reference.md)
- [Meta Graph API Documentation](https://developers.facebook.com/docs/graph-api/)
- [Meta Permissions Documentation](https://developers.facebook.com/docs/permissions/)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Meta Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- [OpenClaw Viet Nam Community](https://zalo.me/g/lajsqc334jqc5fezevvo)
- [ClawHub Skill Page](https://clawhub.ai/trustydev212/skills/facebook-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and curl-based API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Facebook Page/User tokens and curl; mutating actions should be manually reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
