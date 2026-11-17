## Description:

Security auditor for AI agent skills. Scans SKILL.md files for prompt injection, data exfiltration, obfuscation, and dangerous capability combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4worlds4w-svg](https://clawhub.ai/user/4worlds4w-svg)

### License/Terms of Use:


## Use Case:

Developers and skill reviewers use this skill to audit OpenClaw SKILL.md files before installation or release. It helps identify prompt injection, data exfiltration, obfuscation, credential-harvesting patterns, dangerous shell commands, compound threats, and permission mismatches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends submitted skill content to the 4Worlds-hosted ClawAudit service.

Mitigation: Avoid submitting private skills that contain secrets, credentials, proprietary code, or sensitive internal instructions unless you trust that service's handling of the data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4worlds4w-svg/skills/clauwdit)
- [ClawAudit author skill audit endpoint](https://clauwdit.4worlds.dev/audit/author/skill-name)
- [ClawAudit raw skill audit endpoint](https://clauwdit.4worlds.dev/audit)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [JSON audit results and concise markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports trust score, trust tier, findings, capabilities, compound threats, and permission-integrity results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
