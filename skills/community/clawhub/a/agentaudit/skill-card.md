## Description: <br>
Automatic security gate that checks packages against a vulnerability database before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starbuck100](https://clawhub.ai/user/starbuck100) <br>

### License/Terms of Use: <br>
AGPL 3.0 <br>


## Use Case: <br>
Developers and AI-agent users use AgentAudit to check npm, pip, ClawHub, MCP, and similar package installs against a trust registry before installing external code. It also guides static audit report creation for packages that do not already have registry data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store API credentials locally and the release evidence indicates bundled credentials are present. <br>
Mitigation: Replace or remove bundled credentials before use, prefer environment-based keys where appropriate, and rotate keys after installation. <br>
Risk: Audit reports uploaded to the registry may include package metadata and code snippets. <br>
Mitigation: Do not use uploads on private or proprietary packages unless data sharing is explicitly approved and uploads are disabled or verified. <br>
Risk: The security verdict is suspicious because the tool combines package gating with remote registry communication and credential handling. <br>
Mitigation: Review the security guidance, verify configured registry destinations, and test the gate behavior before relying on it in installation workflows. <br>


## Reference(s): <br>
- [ClawHub AgentAudit release](https://clawhub.ai/starbuck100/agentaudit) <br>
- [AgentAudit trust registry](https://agentaudit.dev) <br>
- [AgentAudit leaderboard](https://agentaudit.dev/leaderboard) <br>
- [API Reference](references/API-REFERENCE.md) <br>
- [Manual Audit Methodology](references/AUDIT-METHODOLOGY.md) <br>
- [Detection Patterns Reference](references/DETECTION-PATTERNS.md) <br>
- [Report JSON Format](references/REPORT-FORMAT.md) <br>
- [Trust Score System](references/TRUST-SCORING.md) <br>
- [Troubleshooting Guide](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Registry lookups and report uploads require network access and an AgentAudit API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
