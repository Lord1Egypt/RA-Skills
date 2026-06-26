## Description: <br>
Control LLM API spending per agent. Set daily/weekly/monthly limits with real-time tracking and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set per-agent and global LLM API budgets, log token usage, calculate costs, and review budget status before or after agent activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI writes budget configuration, pricing overrides, and usage logs under ~/.openclaw/budget. <br>
Mitigation: Run it only in the intended user account and back up or archive usage.jsonl as audit data instead of deleting it. <br>
Risk: Documentation includes a broad `pkill -f` process-stop example. <br>
Mitigation: Verify the exact process before stopping it, and prefer targeted process controls where available. <br>
Risk: Budget checks do not automatically block API calls unless they are integrated into a wrapper or hook. <br>
Mitigation: Run `budget check` before LLM calls and fail closed in the calling script when it exits nonzero. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChloePark85/agent-budget-controller) <br>
- [Publisher profile](https://clawhub.ai/user/ChloePark85) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and CLI text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local budget configuration, pricing overrides, and usage logs under ~/.openclaw/budget when commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
