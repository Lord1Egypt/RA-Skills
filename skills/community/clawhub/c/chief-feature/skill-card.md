## Description:

Create and implement new features in Chief-managed projects using the Chief CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nogara](https://clawhub.ai/user/nogara)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to create Chief PRDs, run Chief-driven feature implementation loops, manage feature worktrees and branches, and open pull requests for completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can direct an agent to run commands, approve prompts, commit changes, push branches, and create pull requests with broad autonomy.

Mitigation: Use it only in trusted repositories and require human approval for shell commands, generated diffs, commits, pushes, pull request creation, and cleanup operations.

Risk: Untrusted project names or PRD names could lead to unsafe paths, branches, or command arguments.

Mitigation: Validate project and PRD names as simple safe identifiers before using them in paths, branch names, or commands.

Risk: Parallel Chief runs may increase cost, rate-limit pressure, and review burden.

Mitigation: Limit concurrent runs to the documented 2-3 range and review each worktree's changes before publishing.

## Reference(s):

- [Chief CLI Reference](references/chief-commands.md)
- [Chief Website](https://chiefloop.com/)
- [Chief GitHub Repository](https://github.com/minicodemonkey/chief)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through local repository, Git worktree, Chief CLI, commit, push, and pull request workflows.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
