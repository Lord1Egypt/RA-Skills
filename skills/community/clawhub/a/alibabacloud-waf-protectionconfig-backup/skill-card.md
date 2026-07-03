## Description: <br>
Exports Alibaba Cloud WAF 3.0 and WAF 2.0 protection configurations into regional Excel workbooks for backup, disaster recovery, auditing, migration, and compliance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud security engineers use this skill to back up Alibaba Cloud WAF protection settings for operational recovery, audit evidence, configuration migration, and compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles cloud credentials during WAF backup operations. <br>
Mitigation: Use a least-privilege read-only RAM role or short-lived credentials, and do not paste real access keys into commands, chats, or logs. <br>
Risk: Generated Excel backups can expose sensitive security configuration. <br>
Mitigation: Store backup files only in restricted, approved locations, preferably encrypted or otherwise access-controlled. <br>
Risk: Debug or configuration output may reveal sensitive account details. <br>
Mitigation: Redact debug, credential, and configuration output before sharing logs or support material. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [DefenseScene / DefenseType Enum Reference](references/defense-scene-values.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [WAF 2.0 Backup Workflow](references/waf2-backup-workflow.md) <br>
- [WAF 3.0 Backup Workflow](references/waf3-backup-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated Excel workbooks (.xlsx) and JSON manifest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Backups may contain sensitive WAF configuration and should be stored in a restricted, approved location.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
