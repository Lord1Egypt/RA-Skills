## Description:

Use when the user asks to implement an approved SPEC SDD using test-driven development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to implement approved SPEC SDDs through a strict red-green-refactor loop, mapping tests to numbered requirements and acceptance criteria before changing production code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent proceeds through approved work slices without asking for approval between each slice.

Mitigation: Review the SPEC carefully before invocation and make sure requirements, acceptance criteria, exclusions, and validation strategy are explicit.

Risk: The skill directs user-facing communication in Portuguese (pt-BR), which may not match every team workflow.

Mitigation: Confirm that Portuguese progress reports are acceptable for the intended users before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/execute-tdd-spec)
- [Publisher profile](https://clawhub.ai/user/afonsoft)
- [Source repository](https://github.com/afonsoft/skills)
- [tests.md](artifact/tests.md)
- [mocking.md](artifact/mocking.md)
- [refactoring.md](artifact/refactoring.md)
- [deep-modules.md](artifact/deep-modules.md)
- [interface-design.md](artifact/interface-design.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and progress reports in Portuguese (pt-BR)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces slice-by-slice TDD implementation guidance and repository changes tied to approved SPEC requirements.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
