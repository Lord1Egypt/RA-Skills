## Description: <br>
Download a zip from clawgo.me by key, back up current workspace Markdown, then copy zip contents into the local OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjunyeee](https://clawhub.ai/user/chenjunyeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to restore or synchronize local workspace Markdown files from a ClawGo key while preserving backups of existing workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remote ClawGo zip can persistently replace core OpenClaw workspace instruction files. <br>
Mitigation: Use only trusted ClawGo keys, inspect extracted Markdown before copying, and keep the generated backup path for rollback. <br>
Risk: Restarting the session can load newly imported workspace instructions before the user has reviewed them. <br>
Mitigation: Do not run /reset until the imported SOUL.md, AGENTS.md, TOOLS.md, USER.md, and HEARTBEAT.md contents are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjunyeee/clawgo-clone) <br>
- [Publisher profile](https://clawhub.ai/user/chenjunyeee) <br>
- [ClawGo service](https://clawgo.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports copied files, skipped files, backup path, and reset guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
