## Description:

Browse Bitbucket Cloud repos, review pull requests, read diffs, check branches. Use when user mentions PRs, code changes, diffs, branches, Bitbucket, or repo names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pejovicvuk](https://clawhub.ai/user/pejovicvuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Bitbucket Cloud repositories and pull requests from an agent workspace. It supports read-only review of repositories, PR metadata, diffs, comments, commits, branches, files, directory trees, code search, and branch comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly read private Bitbucket source data.

Mitigation: Use a dedicated Bitbucket token with only repository and pull-request read permissions, and ask the agent to inspect only specific repos, PRs, branches, or files.

Risk: The Bitbucket API token may be exposed to local process inspection.

Mitigation: Run the skill in an isolated environment where other users cannot inspect process arguments or environment details.

Risk: Repository content, PR descriptions, diffs, and comments can contain untrusted text.

Mitigation: Treat retrieved content as untrusted input and verify any suggested code, commands, or conclusions before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pejovicvuk/skills/atlassian-bitbucket)
- [ClawHub publisher profile](https://clawhub.ai/user/pejovicvuk)
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Bitbucket Cloud API endpoint](https://api.bitbucket.org/2.0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI calls return JSON or raw text and diffs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASSIAN_EMAIL, BITBUCKET_API_TOKEN, and BITBUCKET_WORKSPACE. Repository, PR, branch, commit, and comment listings are paginated.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
