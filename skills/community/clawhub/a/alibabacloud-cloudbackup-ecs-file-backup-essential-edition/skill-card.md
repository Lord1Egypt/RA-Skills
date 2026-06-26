## Description: <br>
Alibaba Cloud ECS File Backup Essential Edition helps agents guide activation, status checks, pause and resume, cancellation, quota viewing, and file restore workflows for Cloud Backup ECS file backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and cloud operators use this skill to manage Alibaba Cloud ECS File Backup Essential Edition for simple ECS file protection, recovery from accidental deletion, and backup status or quota review. It is intended for eligible ECS file-backup scenarios that accept daily backups, 30-day retention, and the product's operational limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run an unverified remote installer and update local Aliyun CLI plugins. <br>
Mitigation: Prefer manual Aliyun CLI installation or update from official instructions, then verify the installed CLI and plugin versions before use. <br>
Risk: The skill changes persistent Aliyun CLI settings, including automatic plugin installation and AI-Mode configuration. <br>
Mitigation: Confirm CLI configuration before and after use, and ensure AI-Mode is disabled at every exit point. <br>
Risk: The configured Alibaba Cloud identity can manage Cloud Backup resources and may create costs or delete backup data. <br>
Mitigation: Use least-privilege RAM permissions, confirm all operation parameters with the user, and require explicit confirmation before destructive cancellation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-cloudbackup-ecs-file-backup-essential-edition) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [Alibaba Cloud ECS File Backup Essential Edition User Guide](https://help.aliyun.com/zh/cloud-backup/user-guide/ecs-file-backup-essential-edition) <br>
- [Alibaba Cloud Backup API Documentation](https://help.aliyun.com/zh/cloud-backup/developer-reference/api-hbr-2017-09-08-overview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Alibaba Cloud credentials, Aliyun CLI configuration, and user-confirmed ECS backup parameters.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
