## Description:

Syncs Feishu (Lark) contacts into USER.md so an agent can identify direct-message senders by name from Feishu open_id metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ier](https://clawhub.ai/user/4ier)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to keep a Feishu contact lookup table current in USER.md. The lookup helps agents identify DM senders by actual name instead of assuming the primary user identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu contact names and open_ids are stored in USER.md, which is prompt-loaded for the agent.

Mitigation: Install only when this directory is acceptable in the agent prompt, and review the generated table before restarting the gateway.

Risk: A scheduled sync can repeatedly rewrite USER.md with tenant contact data.

Mitigation: Use the cron setup only when freshness is needed and keep the schedule, account, and target USER.md path under operator review.

Risk: Unvalidated contact names or open_ids can affect the prompt-loaded contacts table in shared or high-privilege environments.

Mitigation: Add validation or escaping for contact names and open_ids before using the skill in those environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ier/skills/feishu-contacts-sync)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu contact users endpoint](https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and USER.md contact table updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local OpenClaw Feishu account configuration and writes the synced contact table into USER.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
