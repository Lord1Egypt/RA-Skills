## Description:

ClawHub Skill Scanner audits skill directories before installation, checking for malicious patterns such as credential access, data exfiltration, command injection, persistence, and obfuscation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amir-ag](https://clawhub.ai/user/amir-ag)

### License/Terms of Use:

MIT License

## Use Case:

Developers and engineers use this skill to review ClawHub, GitHub, URL, or manually downloaded skill packages before installation. It produces risk-oriented findings and installation guidance for human review or CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review says the scanner's automatic approval guidance is easy to bypass.

Mitigation: Treat results as advisory, keep manual review for external skill packages, and do not auto-install third-party skills solely because this scanner reports SAFE.

## Reference(s):

- [Threat Patterns Reference](references/threat-patterns.md)
- [ClawHavoc campaign report](https://www.esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub/)
- [OpenClaw](https://openclaw.ai)
- [ClawHub](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-readable audit report or JSON, with optional shell exit status for automation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk levels are reported as SAFE, CAUTION, DANGER, or BLOCKED.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
