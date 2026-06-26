## Description: <br>
Guides an agent through a disciplined Git development workflow for larger feature and bug-fix tasks, including branch creation, implementation, review, and pull request creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luciuscao](https://clawhub.ai/user/luciuscao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage substantial code changes through a Git workflow that starts from develop, scopes implementation, runs tests and review, and opens a pull request. It is intended for feature work and bug fixes that exceed simple single-file edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to edit a repository and create pull requests. <br>
Mitigation: Use it only in the intended repository and review branch contents and pull request changes before remote actions. <br>
Risk: GitHub credentials may be used when GitHub CLI authentication or GITHUB_TOKEN is available. <br>
Mitigation: Limit credentials to the permissions required for the target repository and rotate or revoke them if no longer needed. <br>
Risk: Incorrect workflow guidance or proposed edits could introduce defects into the target codebase. <br>
Mitigation: Run the required tests, lint, type checks, and code review loop before merging any pull request. <br>


## Reference(s): <br>
- [Code Dev on ClawHub](https://clawhub.ai/luciuscao/code-dev) <br>
- [Conventional Commits](https://www.conventionalcommits.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript snippets, and pull request templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository edits, git branch operations, GitHub CLI commands, tests, review steps, and pull request content.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
