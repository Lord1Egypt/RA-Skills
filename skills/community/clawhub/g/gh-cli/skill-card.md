## Description: <br>
GitHub CLI for remote repository analysis, file fetching, codebase comparison, and discovering trending code/repos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide GitHub CLI workflows for inspecting repositories without cloning, comparing codebases, fetching files, searching GitHub, and operating on issues, pull requests, actions, releases, and repository settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide authenticated GitHub CLI commands that change repositories, issues, pull requests, releases, workflows, variables, secrets, or Codespaces. <br>
Mitigation: Use least-privilege GitHub credentials and require explicit user confirmation before any write, delete, workflow, secret, token, Codespaces, or raw gh api operation. <br>
Risk: GitHub CLI commands may expose token-bearing environment, credential state, secrets, private repository data, or other sensitive results. <br>
Mitigation: Avoid printing credentials or secrets, redact sensitive command output, and scope GH_TOKEN or GITHUB_TOKEN to only the repositories and permissions needed for the task. <br>
Risk: Generated command guidance may be incorrect for some gh versions, hosts, or command families. <br>
Mitigation: Review proposed commands against the installed gh version and GitHub Enterprise host before execution, especially for search syntax and raw API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/gh-cli) <br>
- [Skill homepage](https://github.com/tenequm/skills/tree/main/skills/gh-cli) <br>
- [GitHub CLI manual](https://cli.github.com/manual/) <br>
- [GitHub CLI repository](https://github.com/cli/cli) <br>
- [GitHub search documentation](https://docs.github.com/en/search-github) <br>
- [Gh-Cli Documentation Index](references/index.md) <br>
- [Remote Repository Analysis](references/remote-analysis.md) <br>
- [Compare Two Codebases](references/comparison.md) <br>
- [Discovering Trending Content](references/discovery.md) <br>
- [Gh-Cli - Search](references/search.md) <br>
- [Gh-Cli - Syntax](references/syntax.md) <br>
- [Gh-Cli - Getting Started](references/getting_started.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, code, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command examples may use authenticated GitHub CLI access and can return repository data, issue data, pull request data, workflow data, files, or API responses.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and changelog, released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
