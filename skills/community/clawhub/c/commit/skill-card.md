## Description: <br>
Create a git commit with a contextual message based on current changes, then push the branch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to turn current Git worktree changes into a contextual commit and push the active branch to origin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage every current repository change, create a commit, and push the active branch without a built-in review step. <br>
Mitigation: Before use, inspect the branch, remote, git status, full diff, untracked files, generated files, and secrets; confirm that pushing will not expose private work or trigger unwanted CI/CD. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrennerSpear/commit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Non-interactive shell command execution with a contextual commit message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stages all current changes, creates one commit, and pushes the current branch.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
