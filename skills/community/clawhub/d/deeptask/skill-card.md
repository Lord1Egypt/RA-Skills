## Description:

DeepTask manages an AI-assisted workflow that decomposes requirements into reviewed tasks, executes minimal functional units, runs unit tests, and records successful work with Git commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spaceack](https://clawhub.ai/user/spaceack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use DeepTask to structure implementation work into projects, sessions, subtasks, minimal functional units, unit tests, human reviews, and traceable Git commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can execute local tests and toolchain commands during a full cycle.

Mitigation: Run it only in an isolated test workspace or disposable repository, and confirm the intended toolchain before execution.

Risk: The workflow can mutate repositories and auto-commit all changed files after unit tests pass.

Mitigation: Use a clean repository without unrelated changes or secrets, then review the Git diff and generated SQLite records before allowing a full cycle to commit.

Risk: Unit test content is stored and later executed by the worker.

Mitigation: Review SQLite unit_tests content before execution and avoid storing untrusted test code.

## Reference(s):

- [DeepTask database schema](artifact/references/schema.md)
- [MoonBit syntax reference](artifact/references/moonbit-syntax.md)
- [DeepTask ClawHub skill page](https://clawhub.ai/spaceack/skills/deeptask)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, generated code and test files, SQLite records, and Git commit messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local toolchain checks and commit repository changes after unit tests pass.]

## Skill Version(s):

1.2.0 (source: server release metadata, target metadata, SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
