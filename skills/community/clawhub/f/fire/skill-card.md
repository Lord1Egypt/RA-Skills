## Description: <br>
Executes written implementation plans task by task, with explicit preconditions, verification checkpoints, commits, checkbox updates, and finish options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to execute an already-written implementation plan in order, while preserving task boundaries, verification evidence, commits, and plan checkbox state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to continue executing a prepared coding plan once invoked, which can amplify mistakes in an unclear or stale plan. <br>
Mitigation: Review the plan before invocation and require the agent to stop on structural divergence, repeated verification failure, or unresolved blockers. <br>
Risk: Execution may involve git branches, worktrees, test runs, commits, and subagent delegation. <br>
Mitigation: Use a specific instruction when invoking the skill, confirm the baseline is green, and inspect verification output and diffs at each task boundary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/fire) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown] <br>
**Output Format:** [Markdown guidance with inline commands and implementation checkpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing written plan and produces task execution, verification notes, commits, and updated plan checkboxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
