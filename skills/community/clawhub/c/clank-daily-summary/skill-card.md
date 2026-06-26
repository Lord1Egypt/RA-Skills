## Description: <br>
Generate a daily summary of your agent's activities. Perfect for tracking progress and sharing updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t3mr0i](https://clawhub.ai/user/t3mr0i) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to summarize daily activity, including commits, emails, messages, progress, blockers, and next steps. It can also help prepare a shareable update for Telegram when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily summaries and Telegram sending may expose private work details from repositories, email, or messages. <br>
Mitigation: Limit access to data intended for summarization, review summaries before sending, and use --send only with a trusted Telegram bot and chat. <br>
Risk: The artifact references a clank-summary command but does not include the command implementation. <br>
Mitigation: Confirm what provides clank-summary before installation or execution. <br>


## Reference(s): <br>
- [Clank Daily Summary on ClawHub](https://clawhub.ai/t3mr0i/clank-daily-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include counts of commits, emails, and messages, plus blockers, next steps, and optional Telegram sending guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
