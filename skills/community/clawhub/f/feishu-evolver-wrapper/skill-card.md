## Description: <br>
Feishu-integrated wrapper for the capability-evolver. Manages the evolution loop lifecycle (start/stop/ensure), sends rich Feishu card reports, and provides dashboard visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autogame-17](https://clawhub.ai/user/autogame-17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run and supervise a capability-evolver loop with Feishu reporting, lifecycle controls, dashboard generation, and watchdog recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep an autonomous evolver manager running and restart it through watchdog behavior. <br>
Mitigation: Run it only in an isolated workspace with explicit lifecycle controls and backups. <br>
Risk: The skill can send operational data to Feishu and depends on Feishu token scope and target configuration. <br>
Mitigation: Review Feishu app permissions, token scope, target chats, and document tokens before use. <br>
Risk: The skill can modify installed skills and push workspace changes to git. <br>
Mitigation: Review git remote, branch, auto-heal behavior, and any generated changes before enabling automated push behavior. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/autogame-17/feishu-evolver-wrapper) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Console text, Markdown dashboards, Feishu card payloads, and lifecycle command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send operational reports to Feishu, manage a watchdog process, and coordinate git synchronization when configured.] <br>

## Skill Version(s): <br>
1.8.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
