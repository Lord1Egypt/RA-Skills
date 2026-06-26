## Description: <br>
Create and implement new features in Chief-managed projects using the Chief CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nogara](https://clawhub.ai/user/nogara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create Chief PRDs, set up feature worktrees and branches, run Chief implementation loops, and prepare pull requests for feature work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can modify repositories, create commits, push branches, open pull requests, and remove worktrees. <br>
Mitigation: Run it only in trusted repositories and require explicit review before commits, pushes, pull request creation, or branch and worktree deletion. <br>
Risk: The workflow includes command approval patterns that could reduce user control over shell execution. <br>
Mitigation: Avoid always-allow approvals and review shell commands before execution. <br>


## Reference(s): <br>
- [Chief CLI Reference](references/chief-commands.md) <br>
- [Chief Website](https://chiefloop.com/) <br>
- [Chief GitHub Repository](https://github.com/minicodemonkey/chief) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline bash commands and workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through repository-changing feature workflow steps, including commits, pushes, pull requests, and worktree cleanup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
