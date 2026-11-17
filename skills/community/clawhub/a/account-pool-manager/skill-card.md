## Description:

Account Pool Manager helps agents manage social-media account pools by department or client, check cookie health, and rotate publishing accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content operations teams use this skill to register account-pool entries, select available publishing accounts by business type, enforce rotation constraints, and review cookie health status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookie files and account state may contain sensitive credentials or tenant data.

Mitigation: Install only in intended account-pool environments, restrict access to account and cookie data directories, and use tenant-specific checks where available.

Risk: Optional cookie verification can send cookie-derived request headers to platform verification APIs.

Mitigation: Run verification only when needed, avoid broad verification across all cookies, and review platform handling before enabling API or MCP checks.

Risk: Untrusted account registration data can write account records and cookie paths.

Mitigation: Validate account_id, department, tenant_id, platform names, and daily limits before accepting registration input from untrusted sources.

Risk: Publishing rotation may contribute to account or platform enforcement issues if cooldowns and limits are bypassed.

Mitigation: Honor the skill's cooldowns, daily limits, cookie health status, and health warnings before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/account-pool-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)
- [Bilibili cookie verification API](https://api.bilibili.com/x/web-interface/nav)
- [Zhihu profile verification API](https://www.zhihu.com/api/v4/me)
- [Juejin user verification API](https://api.juejin.cn/user_api/v1/user/get)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account selection results, cookie health summaries, report paths, error codes, and operational warnings.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
