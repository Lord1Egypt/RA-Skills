## Description: <br>
Helps an agent maintain per-project context, status, decisions, todos, timelines, risk notes, and recovery anchors across sessions using local project records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krislu1221](https://clawhub.ai/user/krislu1221) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, project-focused agent users, and teams use this skill to resume work across sessions, keep project state isolated, and maintain concise project status files instead of relying on chat history alone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived project information in local status files, checkpoint files, daily memory summaries, project logs, or an external MemPalace archive. <br>
Mitigation: Use explicit project commands, require confirmation before writes, and enable session sync, dialogue logs, risk scans, cron checks, or MemPalace archival only when the user opts in. <br>
Risk: Periodic scanning and checkpoint behavior can process new conversation content after activation. <br>
Mitigation: Keep state synchronization disabled by default, set short checkpoint expiration, and stop synchronization immediately when the user asks. <br>
Risk: The documented read-merge-write workflow reduces accidental overwrites but does not fully prevent concurrent update conflicts. <br>
Mitigation: Read the latest project file before each write, summarize the intended change, and ask for confirmation before updating shared project records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krislu1221/agent-project-manager) <br>
- [README.md](README.md) <br>
- [STATUS-A.md template](templates/STATUS-A.md) <br>
- [STATUS-B.md template](templates/STATUS-B.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with project status templates, local file paths, YAML blocks, and optional read-only git commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project state artifacts such as STATUS.md, index.md, GANTT.md, project logs, and checkpoint JSON when the user confirms or opts in.] <br>

## Skill Version(s): <br>
2.7.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
