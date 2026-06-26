## Description: <br>
Runtime security hardening for OpenClaw agents that helps protect against prompt injection, data exfiltration, credential leaks, and unauthorized operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iampaulpatterson-boop](https://clawhub.ai/user/iampaulpatterson-boop) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add runtime security guidance, audit checklists, and approval patterns for OpenClaw agents handling external content, credentials, files, browser navigation, and sensitive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad runtime security guidance can affect routine agent behavior by requiring confirmation for file writes, shell commands, browser navigation, configuration changes, credential handling, and external sharing. <br>
Mitigation: Review the activation description and reference files before installation, then tailor allowlists and approval rules to the workspace owner’s operating model. <br>
Risk: Attack examples include malicious URLs and credential-exfiltration patterns as training material. <br>
Mitigation: Treat the examples as inert reference material and do not execute, browse, or copy them into operational workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iampaulpatterson-boop/eridian) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Attack Vectors & Defenses](references/attack-vectors.md) <br>
- [Security Audit Template](references/audit-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with inline code blocks and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces security rules, audit checklist content, attack-pattern references, and browser allowlist configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
