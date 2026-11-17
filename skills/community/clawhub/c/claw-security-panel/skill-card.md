## Description:

OpenClaw security panel for Python 3.7+ that runs access, permission, execution, and resilience checks and generates token-protected temporary report pages with risk details and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haxsscker](https://clawhub.ai/user/haxsscker)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and operators use this skill to launch local security checks, review categorized risks, and receive remediation guidance for their OpenClaw setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive local data such as host logs, shell history, credential-like files, and OpenClaw configuration or workspace content.

Mitigation: Run only in an isolated, non-privileged environment after reviewing the collected paths and confirming the scan scope is acceptable.

Risk: The skill writes report files and token-bearing HTML pages under /tmp.

Mitigation: Treat generated reports and URLs as sensitive, remove them after review, and avoid running on shared machines.

Risk: The launcher executes a server file from /tmp that is not included in the reviewed package.

Mitigation: Do not run the launcher until the server file source is reviewed and packaged or replaced with reviewed code.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/haxsscker/skills/claw-security-panel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text plus local HTML pages and a JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces temporary token-bearing local URLs and report files under /tmp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
