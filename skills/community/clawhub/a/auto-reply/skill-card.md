## Description: <br>
Instagram DM auto-reply system for monitoring, reading, replying to, and checking Instagram direct messages with prompt-injection rejection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check Instagram DM state, read unread conversations, prepare replies, and configure cron or watcher-based DM monitoring. It is intended for accounts already logged into an OpenClaw browser profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access browser session cookies and private Instagram DMs for the account logged into the OpenClaw browser. <br>
Mitigation: Use a dedicated browser profile or account and install only when this access is intentional. <br>
Risk: The background watcher can continuously monitor DMs and write message details to local alert files. <br>
Mitigation: Enable the watcher only when continuous monitoring is desired and review generated alert files regularly. <br>
Risk: DM previews may be forwarded to Discord when Discord credentials are configured. <br>
Mitigation: Do not configure Discord credentials unless forwarding private DM snippets to Discord is acceptable. <br>
Risk: The skill depends on a local browser debug port for Instagram session access. <br>
Mitigation: Keep the browser debug port local and protected from other users or network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/auto-reply) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce reply metadata, notification summaries, security alerts, and browser fallback instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
