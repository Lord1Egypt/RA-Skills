## Description:

Teach OpenClaw how to work in Feishu (Lark) group chats by recognizing speakers, behaving appropriately in groups and DMs, respecting multi-user privacy, and formatting messages for the platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ier](https://clawhub.ai/user/4ier)

### License/Terms of Use:


## Use Case:

Developers and operators connecting OpenClaw to Feishu use this skill to configure group-chat etiquette, sender identification, DM privacy behavior, Feishu-safe formatting, and optional contact syncing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Organization contacts may be bulk-synced into prompt-loaded memory without sanitizing names.

Mitigation: Use a least-privileged Feishu app, sync only needed users where possible, keep USER.md out of version control, and inspect or sanitize generated contact names before restarting the gateway.

Risk: The optional cron setup can persistently refresh contact mappings.

Mitigation: Avoid automatic sync unless it is necessary, and review scheduled jobs and generated contact mappings regularly.

## Reference(s):

- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu contact users API](https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50)
- [ClawHub skill page](https://clawhub.ai/4ier/skills/feishu-group)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with plain-text snippets, bash commands, and Python script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu-specific etiquette, privacy, formatting guidance, and an optional contact-sync command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
