## Description: <br>
B站关键词搜账号工具。根据用户输入的关键词查询B站相关账号，支持按综合排序或粉丝数排序，返回账号列表（含粉丝数、等级、简介等信息）。当用户需要搜索B站账号、查找B站UP主、找B站同类账号时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, MCNs, brands, advertisers, creators, and researchers use this skill to discover Bilibili accounts by keyword, compare creator metrics, and browse categorized account results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili search keywords are sent to RedFox for account search. <br>
Mitigation: Use the skill only when users are comfortable sharing those search terms with redfox.hk. <br>
Risk: The skill requires a REDFOX_API_KEY for API access. <br>
Mitigation: Use a revocable key, store it in local environment configuration, and avoid exposing it in code, prompts, logs, or output files. <br>
Risk: Generic follow-up prompts such as "show me more" continue the previous Bilibili search. <br>
Mitigation: Preserve the prior keyword and page state only for the active search flow, and clarify user intent when context is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/redfox-data/skills/bilibili-keywords-accounts) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox Bilibili user search API endpoint](https://redfox.hk/story/api/bili/userSearch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables for categorized account results, with JSON produced by the helper script before presentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends Bilibili search keywords to RedFox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
