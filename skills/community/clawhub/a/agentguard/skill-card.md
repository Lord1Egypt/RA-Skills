## Description: <br>
AgentGuard monitors agent file access, API calls, and communications to detect suspicious behavior, log events, and generate actionable security reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manas-io-ai](https://clawhub.ai/user/manas-io-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security operators use AgentGuard to observe AI agent activity, detect suspicious file or network behavior, and review alerts and reports before deciding whether to block, investigate, or tune monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects sensitive activity telemetry, including file access, API calls, and communications. <br>
Mitigation: Limit watched directories, keep retention short, review what is written under ~/.agentguard, and confirm sensitive data hashing before use. <br>
Risk: Privacy claims about local processing may conflict with optional Telegram, Discord, email, or webhook alerting. <br>
Mitigation: Keep alerting console-only unless external delivery is intentional, and review destination settings before enabling any channel. <br>
Risk: The security scan verdict is suspicious and recommends source and dependency review before execution. <br>
Mitigation: Verify the publisher, source, and dependencies, then run the Python scripts only in an environment where monitoring scope is intentionally constrained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manas-io-ai/agentguard) <br>
- [Publisher profile](https://clawhub.ai/user/manas-io-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line status text, JSON logs, YAML configuration, and Markdown security reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local monitoring logs, alerts, anomaly summaries, and periodic reports; external alert channels are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
