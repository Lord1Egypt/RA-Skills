## Description: <br>
A futures trading assistant for China's CTP market that helps an agent monitor prices, query accounts and positions, place or cancel orders, manage conditional and scheduled orders, and produce closing reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a chat-driven CTP futures trading assistant for market data, account and position queries, order workflows, local conditional orders, scheduled tasks, and end-of-day reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real CTP futures trading account through a local background daemon. <br>
Mitigation: Install only when agent-operated futures trading is intended, test first with SimNow or a small non-production account, and stop the daemon when it is not needed. <br>
Risk: Conditional orders and scheduled orders can execute later without another user prompt once they are created. <br>
Mitigation: Require explicit confirmation before creating these orders, review active conditions and schedules regularly, and remove any that are no longer intended. <br>
Risk: The local config.json stores broker credentials and connection details. <br>
Mitigation: Protect config.json with local filesystem permissions, avoid sharing it, and rotate credentials if the file is exposed. <br>
Risk: The release has a Review-oriented security verdict because broad activation and automatic order features can create unintended trading impact. <br>
Mitigation: Review the skill code and build scripts before deployment, keep human confirmation for high-impact actions, and monitor daemon events while trading is enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoborlon-alpha/claw-future) <br>
- [Project homepage from metadata](https://github.com/your-org/claw-future) <br>
- [CTP SDK version record](artifact/api/VERSIONS.md) <br>
- [Common futures contract reference](artifact/references/instruments.md) <br>
- [SFIT document download page](https://www.sfit.com.cn/5_2_DocumentDown.htm) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables and concise text with inline shell commands; the CLI returns JSON that the agent reformats for users.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on freshly executed CTP queries for account, position, order, trade, and price data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; changelog labels v1.0.0-beta, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
