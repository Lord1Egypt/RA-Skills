## Description: <br>
Helps an agent recover from login walls by detecting sign-in states, collecting user-approved credentials, filling common login forms, and handling verification codes safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddmmddmm](https://clawhub.ai/user/ddmmddmm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when web browsing or task automation is blocked by a login screen, expired session, or verification-code challenge. It guides sign-in assistance while requiring explicit user approval for credential sources and OTP handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive login credentials and session access. <br>
Mitigation: Provide credentials deliberately, avoid shared terminals or logs when using the credential helper, and keep reusable credential files outside repositories with restrictive permissions. <br>
Risk: Email-assisted OTP handling can expose more mailbox content than needed if used too broadly. <br>
Mitigation: Prefer manual OTP entry for important accounts and authorize mailbox access only for the current task and minimum content needed to locate the latest relevant code. <br>


## Reference(s): <br>
- [Credential Config Example](references/config-example.md) <br>
- [ClawHub Release Page](https://clawhub.ai/ddmmddmm/auto-login-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Credential and OTP handling should remain user-directed, with secrets masked in explanations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
