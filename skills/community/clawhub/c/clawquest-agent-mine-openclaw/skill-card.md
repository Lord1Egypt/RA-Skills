## Description: <br>
The managed automated mining server interface supports OpenClaw session mode and incremental event retrieval, enabling mining startup, status query, settlement, and stamina management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhzai30](https://clawhub.ai/user/zhzai30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to manage ClawQuest mining sessions through OpenClaw-compatible HTTP tools, including setup, status checks, reward settlement, event retrieval, and optional stamina management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and can expose a game API code used for authenticated game actions. <br>
Mitigation: Treat apiCode as a secret, keep the service local or access-controlled, avoid get_api_code unless necessary, and clear cached codes when finished. <br>
Risk: The skill can spend in-game diamonds when stamina buying is requested or auto-buy is enabled. <br>
Mitigation: Leave autoBuyStamina disabled unless unattended diamond spending is acceptable, and review stamina and diamond state before enabling purchase flows. <br>
Risk: Unauthenticated local HTTP tools can trigger mining actions if the service is reachable by untrusted clients. <br>
Mitigation: Run the service only on trusted hosts and restrict network access to the tool endpoint. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zhzai30/clawquest-agent-mine-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON responses from HTTP tool calls, with setup and operating guidance in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes managed mining status, incremental session events, stamina and diamond snapshots, reward details, and error responses from upstream game APIs.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
