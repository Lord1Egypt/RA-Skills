## Description: <br>
Effective Git helps agents analyze Git repository state, recommend commit strategies, write commit messages, run explicit quick Git commands, and guide safer push, rebase, merge, and conflict-resolution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guguoyi](https://clawhub.ai/user/guguoyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect Git changes, choose commit and push workflows, follow project commit conventions, and handle merge conflicts with user confirmation for risky operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quick commands can mutate repository state by switching or creating branches, deleting branches, stashing changes, fetching remotes, committing all changes, or amending the latest commit. <br>
Mitigation: Review the exact `gq` expansion before execution and inspect `git status` and relevant diffs before any commit, amend, stash, branch, or remote operation. <br>
Risk: Diff shortcuts can display untracked file contents, which may expose secrets or private data in the agent transcript. <br>
Mitigation: Avoid diff shortcuts in repositories with untracked secrets and inspect untracked paths before printing full file contents. <br>
Risk: Pushes, rebases, resets, and conflict resolutions can rewrite history or lose work if applied without sufficient review. <br>
Mitigation: Require explicit user confirmation, explain the risk, save a pre-operation diff or backup branch where appropriate, and preserve both sides of conflicts unless the user directs otherwise. <br>


## Reference(s): <br>
- [Git Best Practices](references/best-practices.md) <br>
- [Conflict Resolution Guide](references/conflict-resolution.md) <br>
- [Quick Git Commands Reference](references/quick-commands.md) <br>
- [Effective Git on ClawHub](https://clawhub.ai/guguoyi/effective-git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured Git analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that inspect or mutate the current Git repository; risky operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
