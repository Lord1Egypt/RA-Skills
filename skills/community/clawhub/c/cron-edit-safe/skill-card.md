## Description: <br>
cron-edit-safe helps agents edit OpenClaw cron jobs with backup, dry-run, verification, and rollback steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colbertlee](https://clawhub.ai/user/colbertlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when changing OpenClaw cron jobs and want a guarded command-line workflow. It backs up the current job, tests the proposed command, applies the edit, verifies the result, and rolls back on failure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default dry-run executes the proposed command once, so commands with side effects can write files, call external services, or send notifications before the cron edit is applied. <br>
Mitigation: Review the command before running the skill, avoid untrusted commands, and use --dry-run-only or --no-dry-run deliberately based on whether side effects are acceptable. <br>
Risk: The skill edits a selected OpenClaw cron job and can leave scheduled automation in an unintended state if backup or rollback controls are disabled. <br>
Mitigation: Keep backup and rollback enabled for normal use, review the generated backup path, and use the printed manual recovery command if automatic rollback fails. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/colbertlee/skills/cron-edit-safe) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal command invocations with status text, backup paths, and recovery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create JSON backups under ~/.openclaw/backups and temporary execution logs under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
