## Description: <br>
Pre-commit secret detection for blocking leaked credentials, API keys, and .env files before they hit git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use EnvGuard to scan repositories, staged changes, and git history for leaked secrets, then block commits or generate reports for security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan broad local paths and git history, which may expose sensitive findings in terminal output or reports. <br>
Mitigation: Run scans on intended repositories only, review report destinations, and rely on the skill's redacted match output for routine review. <br>
Risk: Installing hooks changes repository commit behavior and can block commits until findings or configuration are addressed. <br>
Mitigation: Confirm before installing hooks, keep hook configuration under review, and remove hooks with the documented uninstall command when no longer needed. <br>
Risk: Overbroad allowlist entries can hide real credential leaks. <br>
Mitigation: Keep allowlist entries narrow, repository-specific, and reviewed during security maintenance. <br>


## Reference(s): <br>
- [EnvGuard website](https://envguard.pages.dev) <br>
- [EnvGuard hook documentation](https://envguard.pages.dev/docs/hooks) <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/envguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and markdown reports, with shell commands and configuration updates for scans, hooks, allowlists, policies, and reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include file, line, matched pattern, severity, and redacted matches; commands may exit nonzero when findings are detected.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
