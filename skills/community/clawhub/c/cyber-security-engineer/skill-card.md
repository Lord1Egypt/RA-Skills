## Description:

Security engineering workflow for OpenClaw privilege governance and hardening. Use for least-privilege execution, approval-first privileged actions, idle timeout controls, port + egress monitoring, and ISO 27001/NIST-aligned compliance reporting with mitigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fletcherfrimpong](https://clawhub.ai/user/fletcherfrimpong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to harden OpenClaw privilege handling, monitor ports and outbound connections, and produce ISO 27001/NIST-aligned assessment reports with mitigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious because of reported weaknesses in privilege controls and security checks; some files and analyses were only partially inspected.

Mitigation: Review the reported sudo authentication assumptions, executable replacement protections, and checks that may fail open before installation. Treat the scan as a review warning, not a claim about the author's intent.

Risk: The security scan is incomplete: 27 of 29 components were fully inspected, two were partially inspected, and several static analyzers were degraded.

Mitigation: Review the partially inspected components and rerun suitable analysis before relying on the skill's security controls.

## Reference(s):

- [Project homepage](https://github.com/FletcherFrimpong/OpenClaw-Cyber-Analyst)
- [ClawHub release page](https://clawhub.ai/fletcherfrimpong/skills/cyber-security-engineer)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown reports, JSON assessments and configuration, HTML dashboards, and Python or shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include evidence, affected checks, risks, and concrete mitigations when available.]

## Skill Version(s):

0.2.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
