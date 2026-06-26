## Description: <br>
Context Monitor Helper estimates conversation context usage, appends percentage and progress indicators to responses, and warns users when context usage crosses configured thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to monitor long conversations, track estimated token consumption, and receive reminders to start a new session or compact context before limits are reached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects current conversation contents in memory to estimate token usage. <br>
Mitigation: Use it only in conversations where in-memory token estimation is acceptable, and rely on the security finding that no hidden storage or network behavior was detected. <br>
Risk: The /context off command is reported not to disable future monitoring until fixed by the publisher. <br>
Mitigation: Do not rely on /context off as a privacy or behavior control; uninstall or disable the skill at the platform level when monitoring should stop. <br>
Risk: Token counts are estimates and may differ from platform-reported usage. <br>
Mitigation: Treat displayed percentages as planning guidance and verify exact usage with platform statistics when precision matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/context-monitor-helper) <br>
- [Publisher profile](https://clawhub.ai/user/rfdiosuao) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-compatible status text with context percentage, optional progress bar, token estimate, and threshold guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses estimated token counts and configured warning and critical thresholds; does not persist conversation content according to security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
