## Description: <br>
AgentClear helps agents discover, call, and pay for APIs through a proxy marketplace using an AgentClear API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwflickinger](https://clawhub.ai/user/dwflickinger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover API services by natural-language query, inspect price and trust signals, call selected paid services through AgentClear, and check marketplace or account status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected requests can be routed to AgentClear and upstream providers, which may expose payload contents outside the local agent environment. <br>
Mitigation: Send only approved, non-sensitive payloads and review the selected provider's trust details before proxy calls. <br>
Risk: Per-call billing can spend AgentClear account credits. <br>
Mitigation: Check service pricing, trust score, and account balance before calls, and use a revocable API key. <br>
Risk: The skill requires AGENTCLEAR_API_KEY for authentication and metering. <br>
Mitigation: Store the key in an environment variable or secrets manager, scope access to the intended account, and revoke the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dwflickinger/agentclear) <br>
- [AgentClear](https://agentclear.dev) <br>
- [AgentClear API Docs](https://agentclear.dev/docs) <br>
- [AgentClear Security](https://agentclear.dev/security) <br>
- [AgentClear Bounty Board](https://agentclear.dev/bounties) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell commands and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTCLEAR_API_KEY; API calls can spend AgentClear credits and may forward selected payloads to upstream providers.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
