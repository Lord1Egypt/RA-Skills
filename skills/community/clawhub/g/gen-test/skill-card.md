## Description:

Generates unit and E2E tests for existing projects by analyzing design documents and public API signatures, reviewing testability, producing test code, and reporting coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdingiit](https://clawhub.ai/user/fdingiit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add tests to existing projects, prioritize testable APIs, surface design issues that block reliable tests, and establish coverage baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run unpinned third-party testing or coverage tools.

Mitigation: Review each proposed install command, prefer pinned project-local dependencies resolved through the repository lockfile, and avoid global installs where possible.

Risk: The skill may add reusable Makefile targets that affect future project workflows.

Mitigation: Approve Makefile edits only after checking target names, command scope, and whether existing project targets already cover the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fdingiit/skills/gen-test)
- [Coverage recipes](coverage-recipes.md)
- [Design analysis guide](design-analysis-guide.md)
- [Testability checklist](testability-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with code blocks, generated test files, coverage summaries, and optional Makefile targets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dependency installation and reusable Makefile edits after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
