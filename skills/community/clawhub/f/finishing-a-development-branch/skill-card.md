## Description: <br>
Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill after implementation and test verification to choose and execute a branch completion path: local merge, pull request creation, preserving the branch, or confirmed discard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contradictory cleanup guidance could remove a local git worktree after the user chooses to create a pull request. <br>
Mitigation: Before cleanup, verify the selected option, branch, base branch, remote, GitHub account, and worktree path; preserve the worktree for pull request and keep-as-is workflows unless the user explicitly chooses removal. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured option prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before destructive discard actions and recommends test verification before merge or pull request workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
