## Description: <br>
ClawConnect is a universal account connector for AI agents that can send tweets, read and send Gmail, manage calendar data, and send Slack messages through one API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiweil](https://clawhub.ai/user/yiweil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use ClawConnect to connect AI agents to Gmail, Calendar, Twitter, Slack, and Discord account data and actions through a single API. It is intended for workflows where the operator has connected the relevant accounts and wants the agent to read account information or prepare account actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A single API key can provide broad read and send access across connected email, social, calendar, and workspace accounts. <br>
Mitigation: Connect only the minimum accounts needed, keep the API key secret, and verify OAuth scopes and revocation options in the ClawConnect dashboard. <br>
Risk: Agent-driven account actions could send tweets, emails, Slack messages, or other communications unintentionally. <br>
Mitigation: Require explicit user confirmation before any tweet, email, Slack message, or other account action is sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiweil/clawconnect) <br>
- [ClawConnect service](https://clawconnect.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bearer API key for connected account API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
