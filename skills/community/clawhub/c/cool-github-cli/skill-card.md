## Description: <br>
This skill helps agents use the GitHub CLI (`gh`) to inspect and manage GitHub issues, pull requests, workflow runs, and API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check pull request status and CI, manage issues and pull requests, inspect workflow logs, and query GitHub API data through an authenticated `gh` installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on repositories through the user's configured GitHub CLI account. <br>
Mitigation: Install it only where that access is intended, verify `gh auth status` and token scopes, and limit repository permissions where possible. <br>
Risk: Commands that merge pull requests, close issues, rerun workflows, create resources, or call mutating API endpoints can change real repositories. <br>
Mitigation: Require clear user intent before mutation commands and review the target repository, issue, pull request, or workflow run before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chuangyinbot-boop/cool-github-cli) <br>
- [Publisher profile](https://clawhub.ai/user/chuangyinbot-boop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub CLI commands that depend on the user's configured `gh` authentication, repository permissions, and token scopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
