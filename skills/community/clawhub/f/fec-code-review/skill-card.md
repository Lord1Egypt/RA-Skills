## Description:

Reviews frontend code and changes for correctness, maintainability, type safety, rendering risks, and test coverage, producing prioritized findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers and reviewers use this skill to assess changes, selected files, or whole projects and receive prioritized, evidence-backed review findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad review may omit files or overstate coverage.

Mitigation: Record reviewed and unreviewed files and exclusions; label incomplete reviews partial and limit conclusions to reviewed scope.

Risk: Review findings may be inaccurate or miss specialized issues.

Mitigation: Confirm findings against cited code and verification results; use specialized reviews for deep security, accessibility, E2E, or performance assessment.

## Reference(s):

- [Code review report template](references/report-template.md)
- [ClawHub skill listing](https://clawhub.ai/bovinphang/skills/fec-code-review)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings with file and line references, coverage and verification status, and a scoped risk or merge recommendation; saved under reports/.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
