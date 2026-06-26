## Description: <br>
This skill helps users migrate OpenClaw data to Tencent Cloud instances across single-instance, batch, and custom migration scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoikin-yiu](https://clawhub.ai/user/hoikin-yiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and run OpenClaw migrations to Tencent Cloud Lighthouse or CVM instances. It provides migration steps, command templates, required inputs, and troubleshooting guidance for supported and custom scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to handle powerful server login and cloud API credentials during migration. <br>
Mitigation: Use temporary least-privilege credentials, prefer SSH keys with verified host fingerprints, and revoke credentials after migration. <br>
Risk: The batch workflow downloads and runs an external migration script. <br>
Mitigation: Review the downloaded script before execution and run it only in a trusted maintenance environment. <br>
Risk: Migration can stop source OpenClaw services and overwrite target OpenClaw data. <br>
Mitigation: Make tested backups, confirm source and target instances, and run the migration during a planned maintenance window. <br>
Risk: Temporary migration archives may contain sensitive OpenClaw state. <br>
Mitigation: Delete temporary archives and copied state files after verifying the migration result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoikin-yiu/claw2tencentcloud) <br>
- [OpenClaw migration command reference](references/migration_commands.md) <br>
- [Batch migration script](https://go2tencentcloud-1251783334.cos.ap-guangzhou.myqcloud.com/others/claw2tencentcloud.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and migration result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include credential prompts, instance pairing formats, backup steps, and operational warnings before migration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
