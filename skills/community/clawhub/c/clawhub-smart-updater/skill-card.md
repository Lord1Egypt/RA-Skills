## Description: <br>
ClawHub Smart Updater helps agents check installed ClawHub skills for updates, preserve local changes, create backups, detect conflicts, and produce merge recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vilda007](https://clawhub.ai/user/vilda007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage ClawHub skill updates without blindly overwriting local modifications. It is most useful for workspaces where installed skills are customized and update reports, backups, and conflict review are needed before changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change installed skills. <br>
Mitigation: Run it first with --dry-run and --slug for a specific skill, then review the report before allowing broader updates. <br>
Risk: Automated cron use can apply update behavior repeatedly before the operator has established trust. <br>
Mitigation: Avoid cron automation until the behavior has been reviewed and tested in the target workspace. <br>
Risk: External notification settings may expose update information in sensitive environments. <br>
Mitigation: Do not enable external notifications in sensitive environments, and keep placeholder notification targets until explicitly configured. <br>
Risk: The advertised restore-backup.py rollback tool is not present in this version. <br>
Mitigation: Do not rely on that rollback path; confirm backups manually before applying updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vilda007/clawhub-smart-updater) <br>
- [README](artifact/README.md) <br>
- [Vetting report](artifact/VETTING_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, terminal status text, diff files, and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local backup folders, temporary downloaded skill copies, diff reports, and update reports when executed.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
