## Description:

Manages and orchestrates multi-step, stateful agent workflows with task dependencies, persistent state, error recovery, and external rate-limit handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dobbybud](https://clawhub.ai/user/dobbybud)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to structure long-running, multi-step workflows with dependencies, resumable local state, role-based steps, and cooldown handling for rate-limited actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command wrapper can run arbitrary shell text.

Mitigation: Replace eval-based execution with direct argument execution or an allowlist before use.

Risk: Local task state and timestamp paths are not well constrained.

Mitigation: Constrain task names to safe identifiers and write state only to reviewed, expected locations.

Risk: Financial alert and notification behavior is placeholder-oriented and may be mistaken for production automation.

Mitigation: Do not connect placeholders to real data sources or messaging services until data source selection and threshold logic are reviewed and fixed.

## Reference(s):

- [Task Structure Schema](references/task_schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, Bash, and JSON workflow artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local task state JSON and timestamp files when scripts are executed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
