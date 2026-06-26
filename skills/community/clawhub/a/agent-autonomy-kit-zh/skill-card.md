## Description: <br>
Stop waiting for prompts. Keep working. (Chinese localized version) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up task queues, heartbeat routines, and scheduled work patterns that let an agent continue approved work between human prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages unattended scheduled agent work without clear limits on what the agent may change or do. <br>
Mitigation: Use it only when scheduled autonomous work is intended, keep the task queue limited to approved low-risk tasks, and require human approval for code changes, deployments, purchases, deletions, public posts, credential use, and agent spawning. <br>
Risk: Cron and heartbeat automation can continue work when a human is not actively supervising the session. <br>
Mitigation: Keep logs private, review scheduled jobs before enabling them, and document how to pause or remove the automation before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ayakolin/agent-autonomy-kit-zh) <br>
- [Publisher Profile](https://clawhub.ai/user/ayakolin) <br>
- [Declared Homepage](https://github.com/itskai-dev/agent-autonomy-kit) <br>
- [README](README.md) <br>
- [Heartbeat Template](templates/HEARTBEAT.md) <br>
- [Queue Template](templates/QUEUE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance and reusable queue and heartbeat templates; it does not provide executable code.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
