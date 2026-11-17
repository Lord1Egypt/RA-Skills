## Description:

Autonomously inspects a live OpenClaw instance across hardware, configuration, security, skills, and autonomy health domains, then delivers a quantified traffic-light report with actionable remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose live OpenClaw installations, collect local health evidence, and receive prioritized remediation guidance across five operational domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read sensitive OpenClaw configuration, logs, environment files, and identity or profile documents.

Mitigation: Run it only in trusted workspaces, review the collected paths before sharing reports, and redact secrets or personal content from generated diagnostics.

Risk: The skill can retain diagnostic snapshots that may contain operational details from the checked instance.

Mitigation: Review retained checkup data, apply short retention windows, and delete old snapshots when they are no longer needed.

Risk: The skill may recommend curl-to-bash, sudo curl-to-bash, or --force install commands.

Mitigation: Verify installer sources independently, inspect scripts before execution, and avoid --force unless the package source and risk prompts have been reviewed.

Risk: Webhook or email report delivery can expose health findings to external destinations.

Mitigation: Disable delivery channels by default and enable only reviewed destinations with tightly scoped report content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-doctor)
- [Skill definition](artifact/SKILL.md)
- [Data collection protocol](artifact/data_collect.md)
- [Security risk checks](artifact/check_security.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Localized Markdown health report with domain scores, findings, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Markdown or HTML report files and optional delivery through configured local channels]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
