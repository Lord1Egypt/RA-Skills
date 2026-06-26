## Description: <br>
Automatically execute tasks from checklist.md with state management and scheduled checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lightconsen](https://clawhub.ai/user/lightconsen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill in Claude Code projects to run and resume checklist.md task batches with project-local monitoring, state tracking, logs, and checklist updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project-local auto-start behavior can start monitoring in future Claude Code sessions. <br>
Mitigation: Review .claude/settings.local.json after installation and remove the SessionStart hook or run the uninstall script when monitoring is no longer wanted. <br>
Risk: Checklist text can drive automated Claude Code work, which is risky if checklist.md is edited by untrusted parties. <br>
Mitigation: Use only in trusted projects and review checklist.md before starting or resuming execution. <br>
Risk: Completion safeguards are weak because tasks may be marked complete after the task text is emitted for Claude Code execution. <br>
Mitigation: Review task results, changed files, and logs before relying on completed checklist state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lightconsen/fullrun) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown checklist updates, shell command output, and project-local configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local status, log, monitor PID, and Claude Code project settings files during use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
