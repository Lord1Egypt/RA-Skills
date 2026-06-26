## Description: <br>
Autonomous Cascade guides an agent through bounded Plan, Act, and Evaluate loops for multi-step tasks until the goal is met, a budget is exhausted, or user input is required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hupmann86-cell](https://clawhub.ai/user/hupmann86-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent handle multi-step tasks with explicit planning, bounded action rounds, evaluation checkpoints, and halt conditions. It is suited to workflows such as diagnostics, workspace updates, and parameter tuning where autonomous progress is useful but tool and budget limits must be explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad autonomous action authority across repeated task rounds. <br>
Mitigation: Set explicit allowed tools, paths, hosts, budgets, and stop conditions before use. <br>
Risk: Autonomous actions could perform writes, network changes, restarts, or process termination without enough review. <br>
Mitigation: Require confirmation before write operations, network changes, service restarts, or process termination. <br>
Risk: The included blanket process-kill example could disrupt unrelated work. <br>
Mitigation: Use PID- or service-specific process handling instead of broad process-name termination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hupmann86-cell/autonomous-cascade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured plan, round, action, evaluation, and halt sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed tool calls, stop conditions, budget limits, and status summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
