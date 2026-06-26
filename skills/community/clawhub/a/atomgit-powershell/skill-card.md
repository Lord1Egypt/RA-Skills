## Description: <br>
PowerShell commands for AtomGit/GitCode repository, pull request, issue, CI, and collaborator management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panchenbo](https://clawhub.ai/user/panchenbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to operate AtomGit/GitCode projects from PowerShell, including reviewing pull requests, approving or merging changes, checking CI status, managing repositories, managing collaborators, and working with issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AtomGit token exposure or overly broad credentials could grant unintended repository access. <br>
Mitigation: Use a dedicated least-privileged token through ATOMGIT_TOKEN and avoid placing real tokens in command history or plaintext configuration. <br>
Risk: Write-capable commands can approve pull requests, merge changes, create or update issues, and alter collaborators. <br>
Mitigation: Review the target owner, repository, branch, issue, or pull request before running mutating commands and prefer explicit manual confirmation. <br>
Risk: The batch script can automatically approve multiple real pull requests. <br>
Mitigation: Load the batch script only when batch approval is intended, use an explicit PR list, and keep concurrency bounded. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/panchenbo/atomgit-powershell) <br>
- [Publisher profile](https://clawhub.ai/user/panchenbo) <br>
- [AtomGit API documentation](https://docs.atomgit.com/docs/apis/) <br>
- [README.md](README.md) <br>
- [commands.md](commands.md) <br>
- [API-REFERENCE.md](API-REFERENCE.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell commands and script-backed AtomGit API actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PowerShell and ATOMGIT_TOKEN; performs HTTPS network calls to AtomGit and can execute remote write actions when the user invokes mutating commands.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
