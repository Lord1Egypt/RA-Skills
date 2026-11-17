## Description:

Security scanner and hardening tool for OpenClaw. Use when the user asks about security, wants to scan installed skills for malware or vulnerabilities, audit their OpenClaw configuration, check their security score, or harden their setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[u45362](https://clawhub.ai/user/u45362)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to scan installed skills, audit OpenClaw and host security settings, calculate a security score, and get hardening guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence marks the release suspicious due to unsafe scanner and system-audit behavior.

Mitigation: Review the scanner bypass and system-audit behavior before installation, then run audits only as an unprivileged user.

Risk: Audit coverage guidance may encourage elevated local privileges such as shadow, adm, docker, or NOPASSWD sudo access.

Mitigation: Do not grant additional groups or NOPASSWD sudo only to improve audit coverage; accept skipped checks or use a controlled review environment.

Risk: Evidence warns that async system auditors should not be relied on until fixed.

Mitigation: Avoid the async system-audit scripts for trust decisions and prefer reviewed stable audit paths until the issues are resolved.

Risk: A skill that can include its own .claw-audit-trusted file may bypass scanner review.

Mitigation: Do not rely on scanner results for skills carrying their own trust marker; remove or independently verify such markers before using scan results.

## Reference(s):

- [Claw Audit on ClawHub](https://clawhub.ai/u45362/skills/claw-audit)
- [README.md](README.md)
- [PROJECT.md](PROJECT.md)
- [Release Notes v1.1.0](RELEASE-NOTES-v1.1.0.md)
- [Performance Improvements](PERFORMANCE-IMPROVEMENTS.md)
- [Malicious Pattern Database](references/malicious-patterns.json)
- [Scan Rules](references/scan-rules.json)
- [ClawHavoc Campaign Analysis](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with command recommendations and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces security findings, scores, fix guidance, and audit command suggestions; some commands inspect local system and OpenClaw configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
