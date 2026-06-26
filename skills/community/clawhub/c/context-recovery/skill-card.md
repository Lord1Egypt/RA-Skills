## Description: <br>
Automatically recover working context after session compaction or when continuation is implied but context is missing. Works across Discord, Slack, Telegram, Signal, and other supported channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to recover recent working context when conversation history is compacted, truncated, or implied by continuation requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect recent channel or session history to restore missing context. <br>
Mitigation: Install it only where recent history inspection is acceptable and platform history permissions are tightly scoped. <br>
Risk: Recovered context may contain sensitive or stale details if cached without review. <br>
Mitigation: Do not persist recovered context unless the user explicitly approves after reviewing the summary. <br>


## Reference(s): <br>
- [Context Recovery on ClawHub](https://clawhub.ai/jdrhyne/context-recovery) <br>
- [jdrhyne Publisher Profile](https://clawhub.ai/user/jdrhyne) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with structured recovery details and next-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include channel, time range, messages analyzed, active task details, pending actions, and the last user request when available.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
