## Description: <br>
抖音相似账号推荐工具，输入抖音账号名称或账号ID，通过红狐API接口获取本账号数据、内容数据和相似账号推荐数据，深度分析共通点、差异点和优化建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Douyin creators, content operators, MCN teams, and marketing teams use this skill to find comparable or leading Douyin accounts, review account and recent-content metrics, and benchmark content strategy. It supports account-name or account-ID queries through the RedFox API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and may normalize persistent API-key storage in shell or user environment files. <br>
Mitigation: Prefer setting REDFOX_API_KEY only for the current session or through a secure secret manager, and avoid writing long-lived credentials into shell startup files. <br>
Risk: Douyin account identifiers are sent to RedFox for lookup, account collection, and similar-account reporting. <br>
Mitigation: Use the skill only when sharing those identifiers with RedFox is acceptable for the user's privacy, policy, and compliance requirements. <br>
Risk: The --sync and subscription or push options can enroll an account for remote collection or future notifications. <br>
Mitigation: Confirm the enrollment action, stored data, push schedule, and opt-out path before using sync or subscription features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/douyin-similar-account) <br>
- [RedFox Hub](https://redfox.hk/) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFox querySimilarAccounts API](https://redfox.hk/story/api/dyUser/querySimilarAccounts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with account summaries, recent works, comparison tables, analysis, and setup commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends Douyin account identifiers to RedFox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
