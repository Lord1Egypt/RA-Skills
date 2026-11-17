## Description:

Complete skill for operating GitHub CLI (gh) on cli-trunk: full command map, subcommands, usage patterns, JSON output, and practical workflows for Issues, PRs, Actions, Repos, Releases, Projects, Secrets, Variables, Codespaces, Extensions, and API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiroak](https://clawhub.ai/user/iiroak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select and run practical GitHub CLI commands for repository, issue, pull request, Actions, release, project, secret, Codespaces, extension, and API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to make real authenticated GitHub changes, including deleting resources, changing secrets, running workflows, installing extensions, and using raw API calls.

Mitigation: Use minimally scoped credentials and require explicit confirmation before destructive, secret, workflow, repository administration, extension execution, or gh api operations.

Risk: The security review notes broad authenticated GitHub operations without clear guardrails for destructive or secret-related actions.

Mitigation: Review proposed commands before execution and scan the skill before deployment.

## Reference(s):

- [GitHub CLI official site](https://cli.github.com/)
- [GitHub CLI Linux package repository](https://cli.github.com/packages)
- [GitHub CLI releases](https://github.com/cli/cli/releases/latest)
- [ClawHub skill page](https://clawhub.ai/iiroak/skills/gh-complete)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes structured-output patterns using gh --json and --jq for automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
