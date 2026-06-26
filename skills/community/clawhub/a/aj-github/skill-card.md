## Description: <br>
Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, and advanced API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aceundefeated](https://clawhub.ai/user/aceundefeated) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for GitHub CLI commands and guidance for inspecting issues, pull requests, workflow runs, and GitHub API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to use the local GitHub CLI, which may act with the currently authenticated account and token scopes. <br>
Mitigation: Check `gh auth status`, confirm the intended repository, and review `gh api` commands before using them for changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aceundefeated/aj-github) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
