## Description: <br>
MoltGuard helps protect agents and users from prompt injection, data exfiltration, malicious commands, and related runtime security risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomas-security](https://clawhub.ai/user/thomas-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and operate MoltGuard protections for prompt-injection, command-risk, and data-leakage checks. It provides setup commands, status and account-linking commands, and guidance for default or enterprise Core deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a third-party security service that participates in runtime checks. <br>
Mitigation: Install only after confirming trust in OpenGuardrails/MoltGuard and reviewing what data is sent to Core. <br>
Risk: The skill handles API credentials and can expose an API key through /og_claim. <br>
Mitigation: Confirm credential storage and revocation procedures before use, and avoid sharing /og_claim output in shared or logged chats. <br>
Risk: The artifact provides broad agent-side installation, dashboard, account-linking, and enterprise-enrollment commands. <br>
Mitigation: Review commands before execution and prefer managed enterprise Core configuration when organizational policy requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomas-security/antivirus) <br>
- [MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational commands for installation, status checks, dashboard access, account linking, enterprise enrollment, updates, and uninstall.] <br>

## Skill Version(s): <br>
6.8.20 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
