## Description: <br>
Context-aware session manager that monitors token usage and automatically extracts key information to create continuation sessions when approaching context limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ericgogogogogo](https://clawhub.ai/user/Ericgogogogogo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to monitor long-running OpenClaw sessions, extract unfinished work and key context, and prepare continuation prompts before context limits are reached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation history and user preferences may be carried into continuation sessions without clear redaction controls. <br>
Mitigation: Use preview or manual split mode, inspect the continuation prompt before starting a new session, and avoid using the skill with secrets or confidential conversations. <br>
Risk: Automatic cron or heartbeat use can repeatedly process session history without active confirmation. <br>
Mitigation: Keep automation disabled unless needed, set strict cron limits, and require review before spawning continuation sessions. <br>


## Reference(s): <br>
- [Context Auto-Split](references/auto-split.md) <br>
- [Context Optimizer Cron Template](references/cron-usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Ericgogogogogo/context-optimizer-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown continuation summaries, JSON analysis output, and CLI text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Continuation content may include extracted conversation context, unfinished tasks, decisions, user preferences, and file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
