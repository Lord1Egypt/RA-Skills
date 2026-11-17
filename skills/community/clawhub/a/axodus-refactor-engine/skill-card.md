## Description:

Refactor code safely without changing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and carry out behavior-preserving code refactors with explicit target areas, goals, constraints, and validation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trigger metadata may cause the skill to activate outside intentional refactoring requests.

Mitigation: Fix or verify the trigger configuration before installation.

Risk: Code refactoring can unintentionally change behavior if applied without a guard.

Mitigation: Use tests, deterministic reproductions, or supplied validation commands before and after meaningful changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-refactor-engine)
- [Publisher profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text describing the refactor summary, changed files, behavior guards, and validation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation commands and test results supplied by the user or repository.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
