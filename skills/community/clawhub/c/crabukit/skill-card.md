## Description:

Crabukit scans OpenClaw skills and related scripts for dangerous permissions, hardcoded secrets, shell injection vulnerabilities, malicious code patterns, and known-bad skills through optional Clawdex integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tnbradley](https://clawhub.ai/user/tnbradley)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use Crabukit to scan OpenClaw skills before installation, during development, while auditing installed skills, or as a CI security gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because install workflows and scan-boundary handling need review before users trust the tool with untrusted skills.

Mitigation: Use scan-only mode in a sandbox for untrusted skills and review findings before installing or executing the scanned skill.

Risk: The shell helper may run installation paths that carry higher local system risk.

Mitigation: Avoid running the shell helper as root and prefer direct scan commands until symlink, file-size, temporary workspace, and scan-then-install artifact identity checks are tightened.

Risk: Static analysis can miss runtime behavior or intentionally evasive code.

Mitigation: Combine Crabukit results with manual review, least-privilege execution, and monitoring for critical skills.

## Reference(s):

- [README](README.md)
- [Research Summary](RESEARCH_SUMMARY.md)
- [Security Policy](SECURITY.md)
- [Safe Install Scripts](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal output, with optional JSON or SARIF scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk scores, severity labels, findings, remediation guidance, and process exit codes for automation]

## Skill Version(s):

0.1.3 (source: pyproject.toml, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
