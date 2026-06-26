## Description: <br>
Apollo Workflow turns coding ideas into working code through a gated five-phase workflow for brainstorming, planning, subagent development, debugging, and branch finishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use Apollo Workflow to structure feature work, bug fixing, planning, implementation, review, testing, and branch handoff with explicit phase gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly activate for coding, planning, debugging, and branch completion requests and may modify repositories or spawn agents. <br>
Mitigation: Install it only when an agent should follow this workflow, require user approval at phase gates, and review diffs, tests, commits, and branch actions before handoff. <br>
Risk: Workflow scripts run shell commands, manage state files, and interact with git. <br>
Mitigation: Review the shell scripts before use, avoid untrusted task values, keep secrets out of workflow topics and result files, and confirm branch, remote, diff, and test status before merge, push, PR creation, or deletion. <br>
Risk: The security summary reports a packaged metadata identity mismatch with the registry identity. <br>
Mitigation: Verify the publisher and resolve the _meta.json identity mismatch before relying on this release in sensitive workspaces. <br>


## Reference(s): <br>
- [Apollo Workflow on ClawHub](https://clawhub.ai/nic-yuan/apollo-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/nic-yuan) <br>
- [Brainstorming reference](references/brainstorming.md) <br>
- [Writing plans reference](references/writing-plans.md) <br>
- [Subagent development reference](references/subagent-development.md) <br>
- [Systematic debugging reference](references/systematic-debugging.md) <br>
- [Finishing branch reference](references/finishing-branch.md) <br>
- [TDD reference](references/tdd.md) <br>
- [Testing reference](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, JSON gate files, and code changes when implementing tasks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workflow state and gate files under .workflow and may modify repository files during approved coding workflows.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata; artifact frontmatter states 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
