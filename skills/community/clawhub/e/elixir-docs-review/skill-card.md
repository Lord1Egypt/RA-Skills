## Description:

Reviews Elixir documentation for completeness, quality, and ExDoc best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Elixir modules, functions, specs, doctests, and ExDoc cross-references for documentation completeness and quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review findings may be misleading if based on narrow snippets or vague project scope.

Mitigation: Use the skill's gates to lock exact files or modules, read full surrounding definitions, and include file-line evidence before reporting findings.

Risk: The optional verification flow may involve running project tests.

Mitigation: Run tests only in an appropriate workspace and cite exact test output when making doctest-failure claims.

Risk: The skill references a separate review-verification-protocol dependency.

Mitigation: Review and trust that dependency before relying on the pre-report verification protocol.

## Reference(s):

- [Documentation Quality](references/doc-quality.md)
- [Spec Coverage](references/spec-coverage.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown review findings with file-line anchors, evidence quotes, and optional shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include relevant mix test output for doctest-failure claims.]

## Skill Version(s):

1.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
