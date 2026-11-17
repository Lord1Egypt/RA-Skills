## Description:

AI Agent security scanner for detecting malicious code patterns across multiple languages with CLI-based scanning and layered output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT

## Use Case:

Developers, security reviewers, and marketplace operators use this skill to scan AI agent skills, local files, and code packages for suspicious behavior before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and persistence guidance contains unsafe or inconsistent commands.

Mitigation: Review commands before execution, use a verified local clone in a Python virtual environment, and avoid the pending global npm command unless the namespace is verified.

Risk: Release checklist cleanup and force-push examples could affect an active repository if copied directly.

Mitigation: Do not run cleanup, force-push, or broad repository maintenance commands from the checklist in a working repository without an explicit release workflow review.

Risk: Cron removal guidance could delete unrelated scheduled jobs.

Mitigation: Inspect and edit only the scanner-specific cron entry instead of using broad removal commands such as crontab -r.

Risk: Optional LLM and alert integrations can expose secrets or send data to configured endpoints.

Mitigation: Use only test or scoped API keys, prefer local or offline model endpoints, and verify alert webhook destinations before enabling integrations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caidongyun/skills/agent-security-skill-scanner-gitee)
- [Project Homepage](https://gitee.com/caidongyun/agent-security-skill-scanner)
- [Capabilities](docs/CAPABILITIES.md)
- [User Guide](docs/USER_GUIDE.md)
- [Delivery Report](docs/DELIVERY_REPORT.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown, JSON, and concise CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk levels, key findings, and review guidance for scanned targets.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact SKILL.md reports 5.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
