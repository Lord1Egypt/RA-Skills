## Description: <br>
Schedule delayed tasks between OpenClaw agents - set reminders, chain tasks, coordinate agents on a delay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktech99](https://clawhub.ai/user/ktech99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to schedule delayed reminders, follow-up checks, and handoffs between agents when work needs to continue after the current turn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent local daemon can wake OpenClaw agents later through the local queue-wake plugin endpoint. <br>
Mitigation: Review before installing, configure targets carefully, and unload the launchd plist when the skill is no longer needed. <br>
Risk: Queued text is injected into agent system events through an endpoint with broad authority. <br>
Mitigation: Queue only non-sensitive task text and route tasks only to intended agent targets. <br>


## Reference(s): <br>
- [Async Queue Protocol](references/PROTOCOL.md) <br>
- [ClawHub Async Queue Release Page](https://clawhub.ai/ktech99/async-queue) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON queue records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces delayed agent system-event text through a local file-backed queue and plugin endpoint.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
