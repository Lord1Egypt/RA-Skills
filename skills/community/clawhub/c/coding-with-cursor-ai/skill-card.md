## Description:

Runs Cursor AI coding-agent sessions against a specified project to implement features, fix bugs, refactor code, write tests, and perform code reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igrwijaya](https://clawhub.ai/user/igrwijaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate coding tasks to Cursor AI within a selected project directory, including feature work, bug fixes, refactoring, tests, and code reviews. It is intended for reviewed development workflows on feature branches or disposable working copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates broad repository edit and commit authority to a third-party Cursor agent.

Mitigation: Run it only on feature branches or disposable working copies, then review diffs and test results before committing, merging, or deploying.

Risk: Weak task or file scoping can allow unintended changes outside the intended work area.

Mitigation: Provide a narrow project path and focused file list, and confirm the active repository before execution.

Risk: Supply-chain and temporary-file handling gaps can increase exposure when running the wrapper.

Mitigation: Use a pinned and reviewed cursor-agent version, avoid unrelated secrets in the environment, and prefer safer temporary-file handling before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/igrwijaya/skills/coding-with-cursor-ai)
- [Cursor](https://cursor.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown-style task summary, terminal status text, repository file changes, and optional commit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify and commit files in the selected project repository through cursor-agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
