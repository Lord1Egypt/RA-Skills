## Description: <br>
AtomGit (GitCode) code hosting platform integration using Curl and Bash for pull request review, approval, merge, repository management, issue management, CI checks, and collaboration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panchenbo](https://clawhub.ai/user/panchenbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to inspect AtomGit repositories, review pull requests, trigger CI checks, approve or merge pull requests, manage issues, and administer collaborators through shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact AtomGit repository actions with a bearer token, including approving or merging pull requests, creating issues, and changing collaborator access. <br>
Mitigation: Use a least-privilege ATOMGIT_TOKEN and verify owner, repository, pull request, issue, and collaborator arguments before running any write command. <br>
Risk: Token handling relies on environment or local configuration and can expose credentials if tokens are copied into command lines, URLs, logs, or shared output. <br>
Mitigation: Set ATOMGIT_TOKEN through environment or managed configuration, avoid URL token parameters, and redact command output before sharing. <br>
Risk: Batch and merge commands can make remote repository changes quickly and may affect code or access if run against the wrong target. <br>
Mitigation: Review command targets and prefer dry inspection commands before approve, merge, batch, issue update, or collaborator commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panchenbo/atomgit-curl) <br>
- [AtomGit API documentation](https://docs.atomgit.com/docs/apis/) <br>
- [AtomGit token settings](https://atomgit.com/setting/token-classic) <br>
- [AtomGit help center](https://atomgit.com/help) <br>
- [API reference](artifact/API-REFERENCE.md) <br>
- [Command reference](artifact/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, network access to AtomGit, and ATOMGIT_TOKEN for authenticated operations.] <br>

## Skill Version(s): <br>
3.0.4 (source: frontmatter, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
