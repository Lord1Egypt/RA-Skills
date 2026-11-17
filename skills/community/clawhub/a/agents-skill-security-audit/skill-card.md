## Description:

Minimal helper to audit skill.md-style instructions for supply-chain risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scan skill instruction files for supply-chain risk indicators and receive a concise review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may produce false positives because it matches risky words in documentation or detection rules.

Mitigation: Treat reports as review aids and confirm findings through manual inspection before blocking or approving a skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cerbug45/skills/agents-skill-security-audit)
- [Publisher Profile](https://clawhub.ai/user/cerbug45)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown risk report with risk level, finding bullets, and suggested action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided skill file path and writes the report to standard output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
