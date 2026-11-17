## Description: <br>
Exports and imports Alibaba Cloud DDoS Pro domain-level Layer 7 website configurations as YAML v2.0 for backup, audit, rollback, and migration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations and security engineers use this skill to back up, compare, restore, or migrate Alibaba Cloud DDoS Pro domain configurations across explicit domain scopes and regions. It is limited to Layer 7 website configuration and does not cover Layer 4 TCP/UDP port forwarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imports can change live Alibaba Cloud DDoS Pro protection behavior. <br>
Mitigation: Use the documented dry-run diff, confirm region and domain scope before execution, and require user confirmation before applying import changes. <br>
Risk: Over-broad or long-lived credentials can increase blast radius during backup or migration work. <br>
Mitigation: Use a least-privilege RAM user, prefer short-lived STS credentials, and avoid placing access keys in commands or logs. <br>
Risk: Running the workflow against the wrong region can miss or alter the intended domain configuration set. <br>
Mitigation: Confirm whether the target is cn-hangzhou or ap-southeast-1 and run separate workflows when domains exist in both regions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ddoscoo-domain-configuration-backup) <br>
- [Export workflow](references/export-workflow.md) <br>
- [Import workflow](references/import-workflow.md) <br>
- [YAML schema](references/yaml-schema.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with aliyun CLI commands and YAML configuration artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or consumes YAML v2.0 domain configuration files and may generate audit, rollback, result, or mismatch files during workflows.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
