## Description: <br>
The gh CLI skill helps an agent use GitHub's official command line tool to work with repositories, issues, pull requests, workflow runs, GitHub API requests, and search syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to form GitHub CLI commands for repository, issue, pull request, workflow, API, and search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide GitHub CLI actions that merge pull requests, delete issues or repositories, archive repositories, edit settings, or call gh api with the user's GitHub permissions. <br>
Mitigation: Review high-impact gh commands before execution and confirm they target the intended repository, issue, pull request, or API endpoint. <br>


## Reference(s): <br>
- [GitHub CLI manual](https://cli.github.com/manual) <br>
- [GitHub search syntax documentation](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/understanding-the-search-syntax) <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/gh-repo-analytics-gh-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; the skill does not include executable scripts or hidden behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
