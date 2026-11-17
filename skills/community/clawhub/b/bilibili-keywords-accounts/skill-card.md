## Description:

B站关键词搜账号工具。根据用户输入的关键词查询B站相关账号，支持按综合排序或粉丝数排序，返回账号列表（含粉丝数、等级、简介等信息）。当用户需要搜索B站账号、查找B站UP主、找B站同类账号时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content operators, MCNs, brands, advertisers, creators, and researchers use this skill to discover and compare Bilibili accounts by keyword, follower count, account level, bio, live status, and content category.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends Bilibili search keywords to RedFox.

Mitigation: Install only when RedFox API-key use is acceptable, configure the key through environment variables, and avoid hard-coding or exposing it in prompts, logs, or files.

Risk: Returned Bilibili profile names, bios, and account claims are untrusted public content.

Mitigation: Verify important account links or claims before using the results for outreach, reporting, or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/bilibili-keywords-accounts)
- [Core Workflow](references/core_workflow.md)
- [RedFox API keys](https://redfox.hk/settings/api-keys?source=clawhub)
- [Bilibili user profile URL format](https://space.bilibili.com/{uid})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and summaries, with JSON produced by the helper script before agent formatting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends search keywords to RedFox; returned public profile names and bios should be treated as untrusted content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
