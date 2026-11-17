## Description:

Security scanner for OpenClaw skills. Scans SKILL.md files and scripts for prompt injection, data exfiltration, malicious patterns, and unauthorized network calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xeonai44](https://clawhub.ai/user/xeonai44)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use ClawSkillGuard to locally audit OpenClaw skills before installation or execution and to produce findings, severity levels, and a verdict for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A target named clawskillguard can bypass scanning and still produce a clean-style result.

Mitigation: Do not rely on clean verdicts for targets with that name; use a fixed release that fails closed when scans are skipped or incomplete.

Risk: A clean scan is advisory and does not prove a skill is safe.

Mitigation: Review flagged source files manually and treat high or critical findings as blockers until resolved.

Risk: Scanning broad local directories can include unintended skill paths or miss the intended target.

Mitigation: Confirm the exact skill path before scanning installed or workspace skill directories.

## Reference(s):

- [ClawSkillGuard ClawHub release page](https://clawhub.ai/xeonai44/skills/clawskillguard)
- [xeonai44 publisher profile](https://clawhub.ai/user/xeonai44)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON security scan report with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity-filtered findings, scanned file counts, errors, maximum severity, and an advisory verdict.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
