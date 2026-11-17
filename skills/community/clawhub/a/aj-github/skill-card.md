## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aceundefeated](https://clawhub.ai/user/aceundefeated)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent prepare GitHub CLI commands for reviewing pull requests, checking CI runs, listing issues, and querying GitHub API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to use the local GitHub CLI authentication context, where token permissions can allow repository reads or writes.

Mitigation: Review high-impact `gh api` and mutation commands before execution, and use a GitHub token scoped only to the repositories and actions needed.

Risk: Commands that inspect CI runs or logs can expose repository or workflow output to the agent.

Mitigation: Review log-viewing commands before execution in repositories whose CI logs may contain sensitive data.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands that read repository data or perform repository actions depending on the requested task and local GitHub token permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
