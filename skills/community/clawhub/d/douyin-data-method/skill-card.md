## Description: <br>
Douyin Data Method helps agents query and analyze Douyin videos, users, search results, trending topics, Xingtu creator data, index trends, and livestream data through MaxHub API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to map Douyin business questions to supported MaxHub API endpoints, construct parameters, run data lookups, handle endpoint failures, and format results for browsing, analysis, and comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MaxHub API key and sends Douyin query data to a third-party API service. <br>
Mitigation: Use the skill only when the user trusts the MaxHub/aconfig.cn service with the API key and query data; keep API key values out of chat output and environment logs. <br>
Risk: Providing Douyin session cookies to third-party services can expose account access. <br>
Mitigation: Do not provide Douyin session cookies unless the user fully understands the account-access risk and has approval to share those credentials. <br>
Risk: Some documented endpoints may fail, be unavailable, or return incomplete data. <br>
Mitigation: Use the skill's documented retry and downgrade rules, report unavailable endpoints clearly, and treat returned data as third-party reference data rather than definitive ground truth. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/douyin-data-method) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with endpoint tables, query plans, curl-style command examples, and formatted analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps API key values out of output, labels third-party API data as reference data, and preserves the user's detected language.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
