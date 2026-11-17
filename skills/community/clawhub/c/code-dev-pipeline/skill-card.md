## Description:

Code Dev Pipeline is a Chinese-language agent workflow that coordinates specialist roles for complex code development, UI work, review, testing, and final validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawaizhang](https://clawhub.ai/user/clawaizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to structure complex code work into coordinated requirements analysis, architecture, implementation, review, testing, and acceptance steps. It is especially suited to multi-file changes, UI/frontend work, test-sensitive tasks, and code that needs explicit quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to make broad persistent repository and filesystem changes.

Mitigation: Require explicit confirmation before commits, review staged files before commit, and restrict work to the intended project paths.

Risk: The coder and coordinator references encourage broad Git staging and commits.

Mitigation: Avoid `git add .`; stage only reviewed files and inspect diffs before each commit.

Risk: Logging templates can cause generated code to store raw personal data if applied without adjustment.

Mitigation: Revise logging requirements before use so sensitive data is redacted or omitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawaizhang/skills/code-dev-pipeline)
- [Coordinator instructions](artifact/references/coordinator.md)
- [Analyst instructions](artifact/references/analyst.md)
- [Architect instructions](artifact/references/architect.md)
- [Coder instructions](artifact/references/coder.md)
- [Reviewer instructions](artifact/references/reviewer.md)
- [Tester instructions](artifact/references/tester.md)
- [Validator instructions](artifact/references/validator.md)
- [Workflow reference](artifact/references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured reports, code blocks, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow expects review, test, and validation reports; generated code changes may be persisted in the user's repository.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact package.json reports v2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
