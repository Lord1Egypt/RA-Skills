## Description: <br>
Manage GitHub repositories, pull requests, issues, and workflows from OpenClaw for repository coordination tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to inspect pull requests, triage issues, list repositories and branches, and coordinate GitHub workflow tasks from an agent-assisted environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises broad repository-changing capabilities and token-based access. <br>
Mitigation: Use a fine-grained GitHub token scoped only to the intended repositories and permissions, and require explicit confirmation before merges, branch deletion, issue closure, release creation, or multi-repo operations. <br>
Risk: Some advertised commands or integrations may be under-documented or not implemented by the included script. <br>
Mitigation: Validate supported commands in a test repository before operational use, and review generated guidance against the repository's actual GitHub state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-github-manager) <br>
- [GitHub token settings](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell examples and text summaries from GitHub API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitHub token and repository or organization arguments; proposed mutating actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
