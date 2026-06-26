## Description: <br>
Generates structured, concise memory summaries during flush or compaction, detailing conversation stats, tools, user requests, tasks, files, progress, and timeline context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to produce structured OpenClaw memory summaries during flush or compaction. The summaries preserve user requests, tool usage, todos, key files, current work, and timeline context so an agent can resume work cleanly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The resume instruction tells the agent not to acknowledge or recap that it is continuing from a compacted memory summary. <br>
Mitigation: Review that instruction before enabling the skill, and remove or soften it if users should be told when the agent is resuming from compacted context. <br>
Risk: Memory summaries may include conversation details, tool usage, todos, and key file paths. <br>
Mitigation: Store generated summaries only where the workspace's normal memory and access controls are appropriate for that context. <br>


## Reference(s): <br>
- [Compact Summary on ClawHub](https://clawhub.ai/hanxiao-bot/compact-summary) <br>
- [Publisher profile](https://clawhub.ai/user/hanxiao-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown structured summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no code, installer, credentials, or hidden data movement were reported by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
