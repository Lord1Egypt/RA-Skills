## Description: <br>
Manage Git worktrees for isolated parallel development, including creating, listing, switching, cleaning up worktrees, and using isolated branches for concurrent reviews or feature work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage Git worktrees for isolated code reviews, feature branches, and parallel development without repeatedly cloning or stashing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can duplicate local .env files, including sensitive tokens, into each created worktree. <br>
Mitigation: Inspect existing .env files before running create or copy-env, and avoid using the skill on repositories where secrets should not be copied into worktrees. <br>
Risk: The cleanup command can force-remove inactive worktrees. <br>
Mitigation: Manually check inactive worktrees for uncommitted or unpushed work before approving cleanup. <br>
Risk: The tool changes local Git state by creating branches, checking out base branches, pulling from origin, and adding or removing worktrees. <br>
Mitigation: Run it only in repositories where local Git state changes are expected, and review the target branch and worktree list before create or cleanup operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iliaal/compound-eng-git-worktree) <br>
- [Workflow Examples](references/workflow-examples.md) <br>
- [Troubleshooting and Technical Details](references/troubleshooting.md) <br>
- [Worktree Manager Script](scripts/worktree-manager.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run a bundled shell script that changes local Git worktree state and copies environment files.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
