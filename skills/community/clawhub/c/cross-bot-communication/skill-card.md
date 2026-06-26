## Description: <br>
Enables Telegram-oriented agents and bots to scan shared groups or channels, check communication conditions, and relay messages when configured relationships allow it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate cross-bot communication in Telegram groups or channels by building relationship tables, checking membership and admin status, and selecting a feasible delivery path. When the required conditions are not met, it guides the agent to tell the user honestly and propose alternatives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can map Telegram group and channel relationships and relay messages without clear user controls. <br>
Mitigation: Review before installation, restrict scans to approved groups or channels, require a visible preview and confirmation before sending messages, and allow relationship tables to be reviewed and deleted. <br>
Risk: Bot credentials or elevated permissions could increase the impact of unintended scans or messages. <br>
Mitigation: Use a dedicated low-privilege Telegram bot token and avoid granting admin rights unless they are necessary for the intended communication path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adminlove520/cross-bot-communication) <br>
- [Publisher Profile](https://clawhub.ai/user/adminlove520) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include relationship-table structures, condition checks, suggested communication methods, and user-facing fallback guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
