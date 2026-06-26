## Description: <br>
Prevent 429s with automatic tier-based throttling and exponential backoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheAgentWire](https://clawhub.ai/user/TheAgentWire) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add local rate-limit awareness to agent workflows, including gate checks before expensive work, usage recording after work, and pause or resume behavior after 429 errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local rate-limit estimates can be inaccurate, which may throttle the agent too early or fail to prevent every 429. <br>
Mitigation: Start with conservative limits, review status output, tune RATE_LIMIT_ESTIMATE from real usage, and use pause behavior when a 429 occurs. <br>
Risk: The local state file records request history and can be overwritten or exposed if shared across agents or stored in a sensitive path. <br>
Mitigation: Point RATE_LIMIT_STATE to a non-sensitive JSON path, use a separate state file per agent instance, and avoid storing secrets in the state file. <br>
Risk: Prompt, heartbeat, or cron integrations can suppress useful work if exit-code handling is applied too broadly. <br>
Mitigation: Review each integration before enabling it and map gate exit codes only to the intended workflow reductions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheAgentWire/agent-rate-limiter) <br>
- [The Agent Wire](https://theagentwire.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON state and exit codes to guide throttling behavior.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
