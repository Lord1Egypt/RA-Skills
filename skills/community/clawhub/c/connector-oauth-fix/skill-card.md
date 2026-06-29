## Description: <br>
修复 WorkBuddy 连接器 OAuth 授权失败问题，覆盖第三方连接器出现 0x800401F5、找不到应用程序、SSE error 405、授权超时或 streamableHttp connect failed 等错误时的诊断、根因定位、注册表修复和验证流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and WorkBuddy operators use this skill to diagnose and repair Windows browser-launch failures that interrupt OAuth authorization for third-party connectors. It guides log review, network checks, default-browser ProgId inspection, current-user registry override, and post-fix validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A current-user registry override can leave URL handling pointed at an unintended browser command if the failing ProgId or replacement path is wrong. <br>
Mitigation: Verify the failing ProgId and browser executable path first, prefer changing the default browser through Windows settings when practical, and back up or note the existing registry value before applying the override. <br>
Risk: OAuth troubleshooting may involve logs, connector endpoints, or credentials-sensitive context. <br>
Mitigation: Limit installation and use to the specific WorkBuddy connector OAuth issue, and avoid sharing logs or command output that contains tokens or sensitive connector details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuwenqi123123/connector-oauth-fix) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Windows-specific registry repair guidance and validation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
