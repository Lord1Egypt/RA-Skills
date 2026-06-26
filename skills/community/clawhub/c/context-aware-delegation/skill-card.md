## Description: <br>
Give isolated sessions (cron jobs, sub-agents, event handlers) full conversation context from your main session using sessions_history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RGBA-Research](https://clawhub.ai/user/RGBA-Research) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to design scheduled jobs, sub-agents, and event handlers that retrieve main-session history before producing reports, summaries, or delegated task outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background or isolated agents may read private main-session chat history and personal data. <br>
Mitigation: Install only when this access is intentional, reduce history limits, and pass task-specific summaries instead of raw conversation history where possible. <br>
Risk: Scheduled examples can send sensitive summaries through Telegram or email without sufficient guardrails. <br>
Mitigation: Restrict message, email, and calendar permissions, verify recipients, and avoid automatic external delivery of sensitive summaries. <br>
Risk: Cron jobs or spawned sessions may continue running after the original need has passed. <br>
Mitigation: Keep a record of enabled cron jobs and spawned sessions and review them regularly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RGBA-Research/context-aware-delegation) <br>
- [Project Homepage](https://gitlab.com/rgba_research/context-aware-delegation) <br>
- [Publisher Website](https://rgbaresearch.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance depends on sessions_list and sessions_history availability.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
