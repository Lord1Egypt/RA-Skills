## Description: <br>
Claw Def provides AI-driven security protection for OpenClaw with threat detection, install-time risk alerts, runtime interception, file protection, permission management, and security logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cubeclaw](https://clawhub.ai/user/cubeclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use Claw Def to add security checks around skill installation and runtime activity, including threat lookups, file access controls, permission review, and security logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release suspicious because it claims automatic interception and cloud threat reporting without clearly explaining scope, controls, or data handling. <br>
Mitigation: Before installation, confirm what runs automatically, what permissions it receives, what actions it can block or log, and whether behavior traces, paths, hashes, metadata, or source code are sent to a cloud service. <br>
Risk: Publishing materials include a token-in-URL pattern for GitHub operations. <br>
Mitigation: Use GitHub CLI, SSH, or a credential helper instead of embedding tokens in URLs. <br>
Risk: Runtime file protection can block or require approval for sensitive file operations. <br>
Mitigation: Test configured protection levels in a non-production workspace and confirm that prompts, overrides, and audit logs match organizational policy. <br>


## Reference(s): <br>
- [Claw Def ClawHub listing](https://clawhub.ai/cubeclaw/claw-def) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill metadata](artifact/skill.json) <br>
- [Artifact test report](artifact/TEST-REPORT.md) <br>
- [File protection module](artifact/src/file_protection.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Security alerts, Security logs] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured security decisions or log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May block, allow, or ask before file operations based on configured protection levels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
