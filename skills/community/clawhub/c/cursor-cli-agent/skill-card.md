## Description:

Delegate coding tasks to Cursor Agent CLI for feature work, PR review, large refactors, and iterative code changes that need file exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rare](https://clawhub.ai/user/rare)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to delegate coding, refactoring, scripted analysis, and read-only review tasks to the Cursor Agent CLI from a focused workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended agent sessions can edit, commit, or push repository changes without a review checkpoint.

Mitigation: Prefer --plan or interactive mode first, inspect git status and diffs before committing, and require a separate explicit decision before any push or PR creation.

Risk: Broad workspaces or trusted execution modes can expose more code, credentials, or account access than the task requires.

Mitigation: Use isolated temporary worktrees or narrow project directories, and avoid --yolo, --trust, background execution, and broad project roots unless their access is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rare/skills/cursor-cli-agent)
- [Publisher profile](https://clawhub.ai/user/rare)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch interactive or background Cursor Agent sessions that inspect and modify repository files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
