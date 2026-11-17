## Description:

Interact with Forgejo using the `tea` CLI. Use `tea issue`, `tea pr`, `tea actions`, and `tea api` for issues, PRs, Actions, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[razzeee](https://clawhub.ai/user/razzeee)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage Forgejo repositories through Tea CLI commands for pull requests, issues, Actions secrets and variables, API queries, and login configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forgejo tokens used with Tea CLI commands can be exposed if pasted into commands that are logged.

Mitigation: Use narrowly scoped tokens and avoid pasting real tokens into shell commands or logs.

Risk: Commands that inspect Actions secrets and variables may reveal sensitive repository configuration.

Mitigation: Review command targets before running secret or variable operations and limit repository permissions.

Risk: Installing Tea CLI from an unpinned or untrusted source can reduce installation trust and reproducibility.

Mitigation: Prefer a pinned or otherwise trusted Tea CLI installation source when possible.

## Reference(s):

- [ClawHub Forgejo Skill](https://clawhub.ai/razzeee/skills/forgejo)
- [razzeee ClawHub Profile](https://clawhub.ai/user/razzeee)
- [Tea CLI Go Module](https://code.gitea.io/tea/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Tea CLI; jq is useful for filtering advanced API query output.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
