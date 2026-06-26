## Description: <br>
OKR-style goal tracking for solopreneurs with quarterly goals, weekly check-ins, progress scoring, and accountability prompts that flag drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
Solopreneurs and individual operators use this skill to structure quarterly goals, update weekly progress, score key results, and receive direct prompts when goals drift or become unrealistic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Goal files can contain sensitive personal, financial, or business details that an agent may reread during later check-ins. <br>
Mitigation: Keep highly sensitive details out of goals/GOALS.md unless the user is comfortable with the agent retaining and rereading that context. <br>
Risk: Optional heartbeat or cron examples can create scheduled reminders or reviews the user may not expect. <br>
Mitigation: Enable scheduled check-ins only when the user explicitly wants recurring goal reviews and has reviewed the schedule. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Clawdssen/agentledger-goal-tracker) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>
- [The Agent Ledger](https://theagentledger.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local goal-tracking Markdown files and can provide optional heartbeat or cron reminder configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
