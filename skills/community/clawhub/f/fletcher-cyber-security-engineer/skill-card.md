## Description:

This skill supports OpenClaw security hardening through least-privilege and approval-first execution, idle timeouts, port and egress monitoring, and ISO 27001/NIST-aligned compliance reporting with mitigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fletcherfrimpong](https://clawhub.ai/user/fletcherfrimpong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to review and harden OpenClaw deployments, govern privileged actions, monitor network exposure, and produce compliance assessment reports with mitigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious due to reported weaknesses in privileged execution, persistence, and monitoring controls.

Mitigation: Install only if these capabilities are needed, and review the privileged-execution controls and persistent PATH changes before enabling them.

Risk: Scan coverage is incomplete: 27 of 29 components were fully inspected and two were only partially inspected.

Mitigation: Review the partially inspected components and do not treat the scan as establishing that all behavior is safe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fletcherfrimpong/skills/fletcher-cyber-security-engineer)
- [Project homepage](https://github.com/FletcherFrimpong/OpenClaw-Cyber-Analyst)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, JSON, HTML reports]

**Output Format:** [Markdown guidance, JSON assessment data, and an HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessment output reports affected check IDs, status, risk, evidence, and mitigations; findings depend on the host state and configured policies.]

## Skill Version(s):

0.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
