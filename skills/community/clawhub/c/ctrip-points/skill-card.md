## Description: <br>
管理携程积分，查询余额、查看和推荐积分商城商品，并帮助检查积分商城新品。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[totti10hj](https://clawhub.ai/user/totti10hj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ctrip users and agents use this skill to track a local points balance, maintain a local rewards catalog, find affordable redemptions, and get exchange recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Ctrip cookie file can contain account-sensitive credentials. <br>
Mitigation: Treat the cookie file like an account password, keep it private, and avoid sharing or publishing it. <br>
Risk: The documentation claims cron and Feishu notification automation that the included artifact does not implement or install. <br>
Mitigation: Verify and configure any scheduled task or notification integration separately before relying on automation. <br>
Risk: Local points and product data can become stale or differ from official Ctrip account data. <br>
Mitigation: Confirm important balances and redemption decisions against Ctrip's official site or app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/totti10hj/ctrip-points) <br>
- [Publisher profile](https://clawhub.ai/user/totti10hj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and local command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON files for points and product data; no external Python dependencies are required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
