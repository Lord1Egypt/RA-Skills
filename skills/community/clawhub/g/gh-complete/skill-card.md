## Description: <br>
Complete skill for operating GitHub CLI (gh) on cli-trunk: full command map, subcommands, usage patterns, JSON output, and practical workflows for Issues, PRs, Actions, Repos, Releases, Projects, Secrets, Variables, Codespaces, Extensions, and API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiroak](https://clawhub.ai/user/iiroak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and run practical GitHub CLI commands for repository, issue, pull request, Actions, release, project, secret, codespace, extension, and API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-manager installation commands can run with elevated privileges. <br>
Mitigation: Verify the GitHub CLI package source before installation and review sudo package-manager commands before running them. <br>
Risk: Authentication tokens and secrets can be exposed through logs, command history, or overly broad scopes. <br>
Mitigation: Use least-privilege tokens and avoid placing secrets in logs, shell history, or shared command transcripts. <br>
Risk: Delete, archive, transfer, key, secret, workflow, extension, and raw API operations can change or remove GitHub resources. <br>
Mitigation: Manually confirm the target repository, scope, and intended effect before running destructive or administrative gh commands. <br>


## Reference(s): <br>
- [GitHub CLI official site](https://cli.github.com/) <br>
- [GitHub CLI Linux packages](https://cli.github.com/packages) <br>
- [GitHub CLI releases](https://github.com/cli/cli/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and structured-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include gh command examples using --json and --jq for automation-friendly output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
