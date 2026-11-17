## Description:

Validate git commit messages against Conventional Commits and configurable rules for local development, git hooks, and CI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to lint individual commit messages, commit ranges, branch history, commit-msg hook inputs, or CI validation against Conventional Commits and project-specific rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linter reads commit messages and commit-message files in repositories where it is run.

Mitigation: Use it only in repositories where local inspection of commit metadata and commit-message files is acceptable.

Risk: The init command writes a .commitlintrc.json file in the current working directory.

Mitigation: Run init from the intended repository and review the generated configuration before committing or enforcing it.

Risk: Strict mode can fail commits or CI jobs on warnings as well as errors.

Mitigation: Test the configured rules on representative commit history before enabling strict enforcement in hooks or CI.

## Reference(s):

- [Commit Message Linter on ClawHub](https://clawhub.ai/charlie-morrison/skills/commit-message-linter)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, or Markdown lint results; Markdown guidance with shell commands for hook and CI setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes 0, 1, and 2 indicate pass, lint failure, and git or system error; strict mode treats warnings as failures.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
