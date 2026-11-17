## Description:

Provides agents with GitHub CLI guidance and command examples for repositories, issues, pull requests, Actions, releases, and other GitHub workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[return054](https://clawhub.ai/user/return054)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this reference to choose GitHub CLI commands for repository management, collaboration, automation, and related terminal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference includes commands that can delete content, publish changes, change permissions, manage secrets or keys, or bypass prompts and protections.

Mitigation: Require explicit approval before running these commands, including those using --admin, --force, or --yes.

Risk: Token-displaying commands can expose active GitHub credentials.

Mitigation: Do not print or export active tokens without a controlled secret-handling workflow.

## Reference(s):

- [GitHub CLI manual](https://cli.github.com/manual/)
- [GitHub CLI documentation](https://docs.github.com/en/github-cli)
- [GitHub REST API documentation](https://docs.github.com/en/rest)
- [GitHub GraphQL API documentation](https://docs.github.com/en/graphql)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration instructions]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gh CLI for executing suggested commands.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
