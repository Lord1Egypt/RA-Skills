## Description: <br>
Autogoal automates ongoing progress on user-defined long-term goals with periodic check-ins, adaptive strategies, and progress reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandongraves08](https://clawhub.ai/user/brandongraves08) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn open-ended goals into recurring check-ins that evaluate progress, take one concrete action, update strategy, and report status. It is suited to long-running operational or financial goals where progress is tracked over repeated agent turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring autonomous check-ins can lead an agent to take broad real-world actions with weak scoping. <br>
Mitigation: Inspect each generated cron payload, restrict allowed tools and actions, and require explicit user confirmation before enabling actions that change accounts, post externally, delete data, buy, sell, or otherwise create irreversible effects. <br>
Risk: Financial and trading goals can influence decisions with real monetary consequences. <br>
Mitigation: Start financial goals in paper or simulation mode, configure risk rules such as position limits and drawdown caps, and require explicit approval before any live trading or account changes. <br>
Risk: The bundled goal registry contains sample active financial goals that may not match a new user's intent. <br>
Mitigation: Review and remove or archive bundled active goals before scheduling check-ins in a new environment. <br>
Risk: Long-running goals can keep executing after they are no longer useful or safe. <br>
Mitigation: Close, pause, disable, or remove the associated cron job when a goal is completed, abandoned, blocked, or no longer authorized. <br>


## Reference(s): <br>
- [Goal Lifecycle Patterns](references/goal-lifecycle.md) <br>
- [Planning Depth & Strategy Reference](references/planning-depth.md) <br>
- [Autogoal on ClawHub](https://clawhub.ai/brandongraves08/autogoal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON cron payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recurring check-in prompts, goal registry updates, progress reports, and cron configuration for agent execution.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
