## Description: <br>
Wraps improvement-orchestrator in a persistent loop with convergence detection, cost control, and cross-session state persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to run repeated improvement cycles on a target skill with explicit budget, iteration, convergence, and recovery controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repeated automated improvement can consume budget or run longer than intended. <br>
Mitigation: Set explicit max-cost and max-iterations values, start with a low budget, and prefer dry-run or single-run before continuous or cron scheduling. <br>
Risk: Running the loop against the wrong target can repeatedly change an unintended skill. <br>
Mitigation: Use an explicit target path and a dedicated state directory for each run, then review generated outputs before deployment. <br>
Risk: Scheduled or continuous operation can continue across sessions if configured too broadly. <br>
Mitigation: Use scoped cron entries or scheduled invocations, inspect autoloop_state.json and iteration_log.jsonl, and stop when plateau, oscillation, cost, or error limits are reached. <br>


## Reference(s): <br>
- [Autoloop Controller ClawHub page](https://clawhub.ai/lanyasheng/autoloop-controller) <br>
- [State Format](references/state-format.md) <br>
- [Scheduling Guide](references/scheduling-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON state/log artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists autoloop_state.json and iteration_log.jsonl under the configured state root.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
