## Description: <br>
Sends a daily 9:45 AM A-share market opening summary with key indices, sector activity, volume, and trading suggestions, optionally through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrislzg](https://clawhub.ai/user/chrislzg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate or schedule a weekday morning A-share market briefing and send it through Feishu. The report summarizes major indices, fund-flow search results, hot sectors, turnover, and suggested market posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an undeclared local Tavily search command while building fund-flow and sector sections. <br>
Mitigation: Review or remove the hard-coded Tavily command before installing, and configure any search dependency explicitly in the OpenClaw environment. <br>
Risk: The skill can send generated reports through shell commands and uses the Feishu target resolution configured in OpenClaw. <br>
Mitigation: Confirm what the Feishu target resolves to, review message contents before first use, and enable the cron job only when automatic weekday posts are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrislzg/a-stock-morning) <br>
- [Tencent stock quote API endpoint](https://qt.gtimg.cn/q=sh000001) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown market report emitted to stdout or sent through Feishu] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live market and search data; the --send flag posts through the OpenClaw Feishu channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
