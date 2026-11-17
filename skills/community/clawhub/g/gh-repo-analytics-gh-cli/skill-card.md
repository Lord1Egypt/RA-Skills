## Description:

The gh CLI skill helps an agent work with GitHub repositories, issues, pull requests, workflow runs, and authenticated GitHub API requests from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and manage GitHub repositories, pull requests, issues, workflow runs, and GitHub API requests through the GitHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated GitHub CLI access can perform destructive repository, issue, pull request, and raw API actions.

Mitigation: Require the agent to state the target owner and repository, then get explicit confirmation before merges, comments, edits, transfers, deletes, archives, renames, or raw gh api calls.

Risk: The release security summary flags broad authenticated GitHub action capability without clear confirmation guidance.

Mitigation: Install only in environments where agents are intended to use the authenticated GitHub CLI and where high-impact GitHub actions are reviewed before execution.

## Reference(s):

- [GitHub CLI Manual](https://cli.github.com/manual)
- [GitHub Search Syntax Documentation](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/understanding-the-search-syntax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline GitHub CLI command examples and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on the authenticated GitHub CLI available in the agent execution environment.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
