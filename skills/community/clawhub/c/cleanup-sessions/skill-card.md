## Description: <br>
Helps an agent identify and clean aborted OpenClaw sub-agent session files and stale backup files to reclaim disk space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phenixMiao](https://clawhub.ai/user/phenixMiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to inspect aborted sub-agent sessions, preview cleanup candidates, remove confirmed stale session files, and keep session indexes consistent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup guidance may include destructive deletion commands that do not themselves enforce the documented safety checks. <br>
Mitigation: Review commands before use, prefer dry-run or interactive deletion, verify the exact backup directory and file list, and confirm the command enforces the intended age-based safeguards. <br>
Risk: Deleting session files or stale backups can remove recoverable session history or leave session metadata inconsistent. <br>
Mitigation: Preview candidate files with sizes and timestamps, require user confirmation, preserve recent sessions, and update the session index only after confirmed file deletion. <br>


## Reference(s): <br>
- [Cleanup Sessions skill page](https://clawhub.ai/phenixMiao/cleanup-sessions) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with command examples and cleanup workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file lists, deletion previews, and confirmation prompts before cleanup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
