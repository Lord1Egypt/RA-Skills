## Description: <br>
Creates and queries Alibaba Cloud SASE Private Access network diagnosis tasks to troubleshoot connectivity between enterprise endpoints, SASE clusters, and origin servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to create, poll, and analyze Alibaba Cloud SASE Private Access diagnosis tasks for FullLink and Application connectivity troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires cloud CLI credentials and may use broader CLI/plugin authority than the diagnosis task itself needs. <br>
Mitigation: Use a dedicated least-privilege RAM profile with only the listed csas diagnosis permissions, avoid sharing AK/SK secrets in chat or commands, and verify credentials only through the configured Aliyun CLI profile. <br>
Risk: CLI setup and plugin updates can change the local execution environment before diagnosis commands run. <br>
Mitigation: Prefer a verified package-manager or signed installer path, review setup steps before installation, and consider disabling automatic Aliyun plugin installation after use. <br>


## Reference(s): <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Alibaba Cloud Network Diagnostics Guide](https://help.aliyun.com/zh/sase/user-guide/network-diagnostics) <br>
- [CreatePADiagnosisTask API](https://api.aliyun.com/document/csas/2023-01-20/CreatePADiagnosisTask) <br>
- [GetPADiagnosisTask API](https://api.aliyun.com/document/csas/2023-01-20/GetPADiagnosisTask) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI result analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for user confirmation of custom parameters, uses bounded polling, and avoids exposing credential values.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
