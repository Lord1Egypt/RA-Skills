## Description:

Scan any OpenClaw skill for security issues before installing, including malware, prompt injection, obfuscation, and supply chain attacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mackding](https://clawhub.ai/user/mackding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan OpenClaw skill directories before installation and review reported issues, install recommendations, and remediation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to execute mutable external npm code without version pinning or reviewable dependency metadata.

Mitigation: Use an exact audited package version with a lockfile or integrity verification before installation or execution.

Risk: Running the scanner with broad local access could expose credentials or sensitive directories.

Mitigation: Run it in a restricted environment with read-only access to the skill being scanned and avoid exposing credentials or sensitive directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mackding/skills/claws-security-scanner)
- [Publisher profile](https://clawhub.ai/user/mackding)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, shell commands]

**Output Format:** [JSON scan report with human-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes security grade, confidence score, severity breakdown, install recommendation, manual review flags, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
