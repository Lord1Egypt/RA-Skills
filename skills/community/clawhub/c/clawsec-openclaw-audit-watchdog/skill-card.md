## Description:

Automated daily security audits for OpenClaw agents with DM delivery and optional email reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and security operators use this skill to schedule recurring OpenClaw security audits, summarize findings, and deliver reports to configured DM targets with optional email copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or updates a recurring unattended OpenClaw audit job.

Mitigation: Enable it only on hosts where persistent auditing is intended; review the schedule, timezone, install directory, and runtime requirements before setup.

Risk: Audit reports are delivered to a configured DM target and may also be sent by email.

Mitigation: Verify PROMPTSEC_DM_CHANNEL, PROMPTSEC_DM_TO, and PROMPTSEC_EMAIL_TO before installation; leave email unset when external copies are not required.

Risk: PROMPTSEC_GIT_PULL can update the installed skill before audits run when enabled.

Mitigation: Leave PROMPTSEC_GIT_PULL disabled unless updates are controlled by a trusted release process.

Risk: SMTP fallback may send reports through a configured relay.

Mitigation: Prefer local sendmail or a trusted SMTP relay and avoid remote plaintext SMTP for sensitive audit output.

Risk: Standalone installs rely on release artifact integrity.

Mitigation: Verify the signed release manifest, public key fingerprint, archive checksum, and SKILL.md/skill.json hashes before extraction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-openclaw-audit-watchdog)
- [Skill Homepage](https://clawsec.prompt.security)
- [README](README.md)
- [Security Audit Configuration Examples](examples/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit setup guidance and formatted security audit reports; requires bash, openclaw, node, and configured DM recipient environment variables.]

## Skill Version(s):

0.1.9 (source: SKILL.md frontmatter, skill.json, changelog released 2026-06-23, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
