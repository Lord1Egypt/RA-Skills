## Description:

Use when the user asks to implement an approved SPEC SDD using test-driven development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to execute an approved SPEC SDD through a test-driven development loop, mapping each test and implementation slice to documented requirements and acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may change linked GitHub issue labels, comments, closure state, and SPEC status while executing an approved SPEC.

Mitigation: Use a GitHub token with limited repository permissions, verify that the SPEC ticket points to the intended issue, and require explicit confirmation before label edits, comments, or issue closure when that control is needed.

Risk: The server security verdict is suspicious because the skill combines implementation work with linked issue state management.

Mitigation: Review the skill before installation and monitor execution when it can affect repository workflow state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/execute-specs)
- [Source repository](https://github.com/afonsoft/skills)
- [Good and Bad Tests](references/tests.md)
- [When to Mock](references/mocking.md)
- [Refactor Candidates](references/refactoring.md)
- [Deep Modules](references/deep-modules.md)
- [Interface Design for Testability](references/interface-design.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Portuguese progress reports with markdown, code changes, tests, validation commands, and issue-status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay grounded in the approved SPEC and map tests to numbered requirements or acceptance criteria.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
