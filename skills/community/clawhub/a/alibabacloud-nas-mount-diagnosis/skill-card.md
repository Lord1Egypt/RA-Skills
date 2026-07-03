## Description: <br>
Diagnoses Alibaba Cloud NAS mount failures across Linux and Windows NFS or SMB environments, including connectivity, permission, security group, mount command, container, cross-VPC, and error-code scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to triage Alibaba Cloud NAS mount failures, collect required environment details, run read-only Alibaba Cloud CLI checks, and produce a diagnosis report with likely root causes and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some remediation guidance can weaken Windows SMB security, including guest authentication or signing policy changes. <br>
Mitigation: Prefer read-only diagnosis first; apply SMB guest-auth or signing changes only after review by an administrator who understands the security impact and rollback path. <br>
Risk: Some troubleshooting steps can make persistent host changes, such as boot-service, registry, or module configuration updates. <br>
Mitigation: Treat persistent changes as operator-approved remediation steps, document the current setting, and keep a rollback plan before applying them on production hosts. <br>
Risk: The skill may direct users to download and run external diagnostic scripts. <br>
Mitigation: Inspect downloaded scripts before execution and prefer the read-only aliyun API diagnosis path when operating in production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-nas-mount-diagnosis) <br>
- [Alibaba Cloud CLI installation](https://help.aliyun.com/document_detail/139508.html) <br>
- [Alibaba Cloud CLI credentials configuration](https://help.aliyun.com/document_detail/123181.html) <br>
- [Linux NFS mount error reference](references/nfs-linux-errors.md) <br>
- [RAM permission list](references/ram-policies.md) <br>
- [Linux SMB mount system requirements](references/smb-linux-requirements.md) <br>
- [Windows SMB mount error reference](references/smb-windows-errors.md) <br>
- [Linux NAS mount auto-check script](https://nas-client-tools.oss-cn-hangzhou.aliyuncs.com/linux_client/check_alinas_nfs_mount.py) <br>
- [Windows SMB NAS inspection script](https://nas-client-tools.oss-cn-hangzhou.aliyuncs.com/windows_client/alinas_smb_windows_inspection.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnosis report with inline shell, PowerShell, and Alibaba Cloud CLI commands; bundled diagnostic script output is structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic posture; may ask the user to inspect or run downloaded Alibaba Cloud diagnostic scripts before using their results.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
