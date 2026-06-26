## Description: <br>
Local-first budget and policy guardrails for agent actions, with optional remote sync to AgentSentinel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmystacks](https://clawhub.ai/user/jimmystacks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check costly, destructive, or policy-sensitive agent actions before execution. It provides local budget tracking and policy gating, with optional cloud sync when centralized monitoring is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local event logs can contain command text, paths, and operational context. <br>
Mitigation: Treat .agent-sentinel/openclaw_events.jsonl as sensitive and review local retention before sharing workspaces or uploading events. <br>
Risk: Optional cloud sync sends locally recorded events to AgentSentinel when enabled. <br>
Mitigation: Set AGENT_SENTINEL_API_KEY and run sync only when the operator trusts AgentSentinel with the logged event details. <br>
Risk: Resetting local state can clear run or session accounting. <br>
Mitigation: Use reset deliberately and preserve any needed audit records before clearing local accounting. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jimmystacks/agent-sentinel) <br>
- [AgentSentinel skill homepage](https://github.com/jimmystacks/agent-sentinel/tree/main/skills/agent-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands, plus JSON status and decision payloads from the wrapper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create callguard.yaml and local .agent-sentinel state/event files; cloud sync is optional and requires AGENT_SENTINEL_API_KEY plus an explicit sync command.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
