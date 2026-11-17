## Description:

Automatically generates unit tests by analyzing code logic and producing pytest, JUnit, Jest, and related framework test cases, with support for coverage report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgbin](https://clawhub.ai/user/zgbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate unit tests and coverage reports for new features, legacy code, refactoring, and code review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tests or coverage reports may write files into a project workspace.

Mitigation: Run the skill in dry-run or preview mode first, then review diffs before committing generated tests or reports.

Risk: Generated tests may not fully capture intended behavior or edge-case expectations.

Mitigation: Review generated assertions and add project-specific cases before relying on the tests in CI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zgbin/skills/auto-test)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with generated test code examples, shell commands, configuration options, and coverage report guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create test files and coverage reports in the target workspace; preview generated changes with dry-run before committing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
