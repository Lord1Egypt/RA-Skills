## Description:

Applies evidence-based gates to code security reviews, validating findings and downgrading unsupported claims to observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modusensus](https://clawhub.ai/user/modusensus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use Euthyna to audit code, changes, dependencies, or suspected vulnerabilities and produce an evidence-backed report. It helps distinguish confirmed findings from observations or inconclusive claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project tests or exploit demonstrations may be run without safe containment, and the available scan coverage is incomplete.

Mitigation: Review the verification guidance and run project tests or exploit demonstrations only in an isolated, disposable environment; treat the scan as incomplete.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/modusensus/skills/euthyna)
- [Verification gates](references/verification-gates.md)
- [Change audit](references/change-audit.md)
- [Dependency audit](references/dependency-audit.md)
- [Fact producers](references/fact-producers.md)
- [Fact contract](references/fact-contract.md)
- [Bug classes](references/bug-classes.md)
- [Meta mechanisms](references/meta-mechanisms.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Mermaid diagrams]

**Output Format:** [Markdown security audit reports with evidence citations, command guidance, and optional Mermaid lineage diagrams.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports distinguish confirmed findings, false positives, and inconclusive claims.]

## Skill Version(s):

0.11.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
