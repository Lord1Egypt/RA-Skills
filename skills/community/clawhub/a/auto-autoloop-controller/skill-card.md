## Description: <br>
When continuous automated improvement of a Skill is needed, this skill wraps improvement-orchestrator in a persistent loop with convergence detection, cost control, and cross-session state persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run repeated skill-improvement iterations with automatic stop conditions for maximum iterations, budget, score plateau, or oscillation. It is intended for supervised continuous, scheduled, or fixed-count improvement runs where state and handoff artifacts need to survive across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run nested improvement/review commands with broad local authority by default. <br>
Mitigation: Use it only on trusted local skill sources, prefer disabling broad authority with --no-yolo or AUTOREVIEW_YOLO=0 when available, and review generated changes before accepting them. <br>
Risk: Continuous or scheduled runs can spend budget and keep modifying state until a stop condition is reached. <br>
Mitigation: Set conservative max-cost, max-iterations, and plateau-window values before launch, and use dry-run mode to check loop behavior before unattended execution. <br>


## Reference(s): <br>
- [Autoloop Controller Skill Source](artifact/SKILL.md) <br>
- [Scheduling Guide](artifact/references/scheduling-guide.md) <br>
- [State Format](artifact/references/state-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/auto-autoloop-controller) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/lanyasheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON state/log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent autoloop_state.json, iteration_log.jsonl, and per-iteration Markdown handoff files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
