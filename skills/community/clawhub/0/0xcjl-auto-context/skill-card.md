## Description: <br>
auto-context analyzes AI agent conversation health, including long sessions, topic drift, noise, repeated tool use, and compression, then recommends whether to continue, fork, focus with /btw, or start a new session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to monitor context health during long or drifting AI coding sessions. It provides compact recommendations for continuing, forking, refocusing, or starting a new session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic reminders may alter the flow or tone of normal agent responses. <br>
Mitigation: Use manual triggering or platform configuration when strictly manual behavior is preferred. <br>
Risk: Context-health recommendations may be unhelpful when the conversation signals are ambiguous. <br>
Mitigation: Treat recommendations as advisory and let the user decide whether to continue, fork, refocus, or start a new session. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xcjl/0xcjl-auto-context) <br>
- [Source repository from release metadata](https://github.com/0xcjl/auto-context) <br>
- [Original auto-context skill credited by artifact](https://github.com/lovstudio/skills/tree/main/skills/lovstudio-auto-context) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Short Markdown or plain text context-health reports and reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual mode produces a compact health report; automatic mode produces brief reminder guidance when triggered.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
