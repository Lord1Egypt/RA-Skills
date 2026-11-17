## Description:

Use when the user asks to implement an approved SPEC SDD using test-driven development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to implement an approved SPEC SDD through a test-driven red-green-refactor workflow. It helps map tests to numbered requirements and acceptance criteria, run validation after each slice, and report progress in Portuguese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to modify repository code according to the approved SPEC.

Mitigation: Install and use it only when the SPEC has already been reviewed and approved for implementation.

Risk: An incomplete or incorrect SPEC may lead to tests and implementation that satisfy the written artifact but not the intended product behavior.

Mitigation: Review the SPEC first and require each test to map to a numbered requirement or acceptance criterion before implementation proceeds.

Risk: Progress messages are expected in Portuguese, which may reduce review clarity for teams that do not use Portuguese.

Mitigation: Confirm the expected communication language with the project team before using the skill in shared workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/execute-spec)
- [Publisher profile](https://clawhub.ai/user/afonsoft)
- [Metadata URL declared by skill](https://github.com/afonsoft/skills)
- [Good and Bad Tests](references/tests.md)
- [When to Mock](references/mocking.md)
- [Refactor Candidates](references/refactoring.md)
- [Deep Modules](references/deep-modules.md)
- [Interface Design for Testability](references/interface-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress reports to the user are expected in Portuguese.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
