## Description:

Facebook Page manager: post, schedule, reply, get insights, and manage page interactions through Meta Graph API calls using PowerShell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seph1709](https://clawhub.ai/user/seph1709)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate Facebook Pages from an agent, including publishing or scheduling posts, reading insights, handling comments, and setting up the required page token credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived Facebook Page credentials could allow broad page access if exposed.

Mitigation: Grant only the minimum Meta permissions, remove FB_APP_SECRET after setup, keep credentials out of backups and repositories, and rotate or revoke tokens regularly.

Risk: The skill can perform public-facing or destructive Page actions allowed by the token, including publishing, deletion, and moderation.

Mitigation: Use it only for Pages where this agent access is acceptable and manually confirm destructive or public-facing actions before execution.

## Reference(s):

- [ClawHub Facebook Page skill](https://clawhub.ai/seph1709/skills/facebook-page)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Meta for Developers Apps](https://developers.facebook.com/apps/)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Meta Graph API v25.0 endpoint](https://graph.facebook.com/v25.0)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PowerShell examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Meta Graph API v25.0 and a local credentials file at ~/.config/fb-page/credentials.json.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
