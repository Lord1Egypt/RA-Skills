## Description:

Axiomata Guard Scanner scans OpenClaw skills for malicious patterns, C2 or exfiltration indicators, cross-vector attack chains, rootkit or bootkit patterns, and package ecosystem risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before installing or reviewing OpenClaw skills to identify suspicious code patterns and produce a security decision for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because directory scans can silently miss executable skill files while presenting a security decision.

Mitigation: Use this scanner as a lightweight pattern check only; inspect scripts and other executable files separately before approving a skill package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiomata-guard-scanner)
- [ClawHub publisher profile](https://clawhub.ai/user/kofna3369)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Plain text security report or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports threat level, score, decision, triggered vaccines, findings, and timestamp.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
