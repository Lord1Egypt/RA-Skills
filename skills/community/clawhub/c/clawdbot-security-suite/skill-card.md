## Description:

Advanced security validation for Clawdbot - pattern detection, command sanitization, and threat monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtrusler](https://clawhub.ai/user/gtrusler)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent operators use this skill to validate commands, URLs, paths, and external content before execution and to monitor local security events for Clawdbot workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic hook may observe broad tool activity and store sensitive arguments in local logs.

Mitigation: Review the hook before enabling it, disable or minimize local logging where sensitive arguments may appear, and define retention and redaction expectations before deployment.

Risk: The security evidence warns that fail-open behavior and shell invocation patterns prevent this package from acting as a dependable security boundary.

Mitigation: Treat validation output as advisory until fail-open paths, shell invocation, and command execution examples are reviewed and fixed.

Risk: Installation guidance relies on unpinned package or repository retrieval.

Mitigation: Install only a reviewed release artifact and verify the release hash or source fingerprint supplied by the server evidence before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtrusler/skills/clawdbot-security-suite)
- [Project overview](README.md)
- [Security skill reference](skills/security/SKILL.md)
- [Installation guide](skills/security/INSTALL.md)
- [Agent integration guide](skills/security/CLAWDBOT-INSTRUCTIONS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented text with shell commands, status strings, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local validation results and security event summaries; requires jq according to server-resolved metadata.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
