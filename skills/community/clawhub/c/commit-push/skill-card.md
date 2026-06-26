## Description: <br>
commit and push all local changes to remote repo <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide an agent through reviewing local repository changes, preparing a Conventional Commits message, staging the intended files, committing, pushing to the configured remote, and verifying the branch is caught up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may push secrets, private files, unrelated changes, or work to the wrong remote or branch if the repository state is not reviewed. <br>
Mitigation: Review `git status`, staged files, the target branch, and configured remotes before push; verify the branch is caught up afterward. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review of git status, staged files, branch, remote, and upstream sync before and after push.] <br>

## Skill Version(s): <br>
1.1.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
