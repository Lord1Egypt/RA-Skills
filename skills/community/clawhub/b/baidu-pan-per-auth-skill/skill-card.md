## Description:

Manages Baidu Pan OAuth 2.0 authorization-code token exchange, access-token refresh, and scheduled refresh guidance for personal applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users maintaining Baidu Pan personal applications use this skill to exchange one-time authorization codes for access tokens, refresh expired tokens, and set up token refresh guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Baidu OAuth app secrets and refresh tokens may be stored in a local plaintext .env file.

Mitigation: Use a dedicated credential file with restrictive permissions and avoid exposing authorization codes, token URLs, secrets, or token values in command history or logs.

Risk: An indefinite scheduled refresh job may keep credentials active longer than intended.

Mitigation: Prefer manual refresh unless scheduling is needed; if a cron job is added, document how to remove it and review the schedule and credential path before enabling it.

## Reference(s):

- [Baidu Pan Open Platform OAuth documentation](https://pan.baidu.com/union/doc/al0rwqzzl)
- [Baidu Pan Open Platform application console](https://pan.baidu.com/union/console/applist)
- [ClawHub release page](https://clawhub.ai/ugpoor/skills/baidu-pan-per-auth-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, configuration values, and a Python helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local environment file for OAuth app credentials and token fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
