## Description: <br>
防遗忘防卡顿的context管理协议。自动监控水位、分区管理、压缩前存档、压缩后恢复。适用于所有OpenClaw agent和sub-agent。在heartbeat或session启动时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unicornnoway](https://clawhub.ai/user/unicornnoway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to manage OpenClaw session context, checkpoint local progress, recover after compression, and coordinate sub-agent work without losing task state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local checkpoint files may capture secrets, private keys, personal data, financial details, or other sensitive information. <br>
Mitigation: Review STATUS.md, MEMORY.md, memory logs, and HEARTBEAT.md periodically, and avoid writing sensitive data into those files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and checkpoint file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local checkpointing and recovery procedures for STATUS.md, MEMORY.md, memory logs, and HEARTBEAT.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
