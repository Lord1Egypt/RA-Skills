## Description:

Scans OpenClaw skill files for potential security threats, including credential exposure, malicious code patterns, dependency risks, and unsafe configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betsymalthus](https://clawhub.ai/user/betsymalthus)

### License/Terms of Use:

MIT

## Use Case:

Developers, skill users, and teams use this skill to scan OpenClaw skill directories before installation, release, or CI deployment and review findings with remediation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may expose real secrets, sensitive file paths, or other confidential evidence discovered during scanning.

Mitigation: Treat reports as sensitive, review them before uploading to CI artifacts, tickets, or logs, and restrict access to shared report outputs.

Risk: Mutable install sources can change after review and may not match the assessed release.

Mitigation: Install only from a pinned, reviewed release or commit and run the scanner as an unprivileged user without sudo.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/betsymalthus/skills/claw-security-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text, JSON, or Markdown reports with risk levels, matched evidence, and remediation recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include scanned file paths, line numbers, risk statistics, and sensitive findings that should be reviewed before sharing.]

## Skill Version(s):

0.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
