## Description: <br>
Openclaw Backup creates encrypted, verifiable OpenClaw backup sets, supports dry-run and staged restores with rollback, and can schedule backups or push operational archives to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to back up OpenClaw workspaces, redacted configuration, cron definitions, and optional encrypted secrets, then verify or restore those backup sets during recovery. It is also used to schedule daily backups, run restore drills, and push operational archives to a private GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup and GitHub push workflows can expose sensitive operational archives or encrypted secrets if repository visibility or archive selection is wrong. <br>
Mitigation: Review scripts before installation, verify that any GitHub repository is private, push operational archives by default, and include encrypted secrets only with explicit operator intent. <br>
Risk: Restore workflows mutate the local OpenClaw filesystem and may execute a restored health-check script. <br>
Mitigation: Run restore with --dry-run first, avoid --force except in a controlled recovery procedure, and inspect untrusted archives or disable restored health-check scripts before a real restore. <br>
Risk: Retention and verification workflows can delete older backup runs, orphaned manifests, or orphaned encrypted secrets. <br>
Mitigation: Review the retention policy, keep an independent copy of critical backup sets, and confirm verification results before relying on automated pruning. <br>
Risk: Cron scheduling creates persistent recurring backup behavior on the host. <br>
Mitigation: Review the scheduled command, backup destination, and encryption settings before enabling daily backups. <br>


## Reference(s): <br>
- [Restore Guide](artifact/references/restore-guide.md) <br>
- [What to Back Up](artifact/references/what-to-backup.md) <br>
- [Retention Policy](artifact/references/retention-policy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zurbrick/agent-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and shell-script workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local backup archives, manifests, cron entries, and GitHub pushes when the user runs the scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and changelog, released 2026-03-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
