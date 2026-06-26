## Description: <br>
Manage OpenClaw conversation memory by archiving sessions, creating structured markdown summaries, and compacting older tool output locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miaoxingjun](https://clawhub.ai/user/miaoxingjun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to reduce long-session context size, preserve recent project decisions, and keep local conversation archives for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local archives, summaries, and backups can contain private conversation content or secrets. <br>
Mitigation: Use only on sessions suitable for local retention, secure the ~/.openclaw workspace, and delete generated archive, summary, or backup files when they should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miaoxingjun/asclaude-compact) <br>
- [Publisher profile](https://clawhub.ai/user/miaoxingjun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper scripts write JSONL archives and markdown summaries when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against OpenClaw session files and may write archives, summaries, and backups under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
