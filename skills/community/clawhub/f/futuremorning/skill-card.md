## Description: <br>
查询未来清晨的活动信息。当用户询问未来清晨的活动、近期活动、活动安排、某个活动详情时使用。支持列出所有活动和根据活动ID获取详情。默认输出JSON，用户要求时可输出Markdown格式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longbai](https://clawhub.ai/user/longbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to list Future Morning activities or retrieve details for a specific activity by campaign ID. It is intended for event lookup workflows where JSON is useful by default and Markdown is preferred for human-facing summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs shell commands that call an external activity API and may return current event data that changes over time. <br>
Mitigation: Review the command target and campaign ID before execution, and verify time-sensitive activity details before relying on them. <br>
Risk: Security guidance notes that privileged ClawHub moderation commands can make real account, role, package, and skill visibility changes when run with a privileged token. <br>
Mitigation: Use only when intended for ClawHub or staff operations, and review the exact command, target, reason, and confirmation before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longbai/futuremorning) <br>
- [Cumen campaign list API](https://api.cumen.fun/api/xx.cumen.v1.CumenService/ListCampaignsOfClub) <br>
- [Cumen campaign detail API](https://api.cumen.fun/api/xx.cumen.v1.CumenService/GetCampaign) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON by default; Markdown table or detail summary when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js HTTPS POST calls to Cumen campaign endpoints; converts timestamps from UTC to UTC+8 for display.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
