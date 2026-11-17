## Description:

Audit whether tests detect regressions in claimed behavior by finding mocked-away subjects, weak assertions, undiscriminating fixtures, swallowed failures, and tests missing from gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this workflow to assess whether a test suite would fail on plausible regressions and to produce actionable, evidence-backed audit findings. It is read-only by default; test or production changes are made only when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The test reach probe records failures through a limited subprocess hook, so some subprocess paths may not be observed.

Mitigation: Run probes in a scratch copy and account for the documented subprocess coverage limits before relying on their results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/iliaal/skills/compound-eng-test-audit)
- [Behavioral review guide](references/behavioral-review.md)
- [Detector diagnostics and blind spots](references/detectors.md)
- [Mutation probes and repairs](references/mutation-and-repair.md)
- [Per-stack commands](references/stacks.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown audit report with findings, evidence, execution notes, and repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; changes are made only when requested]

## Skill Version(s):

5.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
