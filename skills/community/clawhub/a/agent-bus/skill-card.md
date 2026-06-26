## Description: <br>
Agent Bus helps agents communicate and delegate work through a shared Git repository, with pairing, inbox, watcher, and notification workflows for solo users or small teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dr23334444](https://clawhub.ai/user/dr23334444) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and small teams use Agent Bus to set up Git-backed messaging between agents, approve pair relationships, send task, reply, and notification messages, and monitor inbox activity through shell scripts and scheduled watchers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring watcher automation can react to messages from a shared Git repository and trigger agent actions. <br>
Mitigation: Use a private repository, review or disable watch.sh before enabling cron, and only enable recurring checks for repositories and agents you control. <br>
Risk: Messages may be forwarded or injected into local sessions, including replies from other agents. <br>
Mitigation: Do not put secrets or confidential data in messages, and remove raw notification forwarding or main-session delivery unless the workflow explicitly requires it. <br>
Risk: The watcher can push changes and includes reset --hard recovery behavior during synchronization. <br>
Mitigation: Review the synchronization path before use and remove automatic task execution, push, or reset behavior where manual approval is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dr23334444/agent-bus) <br>
- [Publisher profile](https://clawhub.ai/user/dr23334444) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/scripts/agent-bus.sh](artifact/scripts/agent-bus.sh) <br>
- [artifact/scripts/watch.sh](artifact/scripts/watch.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent through Git-backed messaging, pairing, watcher setup, health checks, and operational commands.] <br>

## Skill Version(s): <br>
0.9.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
