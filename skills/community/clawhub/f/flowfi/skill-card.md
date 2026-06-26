## Description: <br>
FlowFi provides REST API guidance for authorization, smart accounts, AI-generated workflows, workflow lifecycle actions, executions, WebSocket status updates, prices, templates, DTOs, and related request and response shapes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devarogundade](https://clawhub.ai/user/devarogundade) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill to integrate with the FlowFi backend API, including creating and managing workflows, starting or canceling executions, subscribing to real-time status updates, and using templates or price endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires agents to handle FlowFi bearer tokens, including long-lived tokens. <br>
Mitigation: Use trusted OpenClaw environments only, prefer short-lived and least-privileged FlowFi tokens, avoid exposing tokens in logs or chat, and revoke tokens after use. <br>
Risk: The skill covers high-impact workflow actions such as deploy, start, edit, stop, cancel, and delete. <br>
Mitigation: Require the agent to list and confirm exact workflow or execution IDs before performing mutating actions. <br>
Risk: Server security evidence marks the release as suspicious because token-safety and confirmation guidance is not strong enough for workflow mutations. <br>
Mitigation: Review the skill before installation and add operational guardrails for token handling and user confirmation before using it in production workflows. <br>


## Reference(s): <br>
- [ClawHub FlowFi Skill Page](https://clawhub.ai/devarogundade/flowfi) <br>
- [FlowFi Skill Instructions](SKILL.md) <br>
- [FlowFi Documentation Index](docs/README.md) <br>
- [Authorization](docs/authorization.md) <br>
- [Workflows](docs/workflows.md) <br>
- [Executions](docs/execution.md) <br>
- [WebSocket Status Updates](docs/websocket.md) <br>
- [DTO and Request/Response Shapes](docs/dto.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown with endpoint descriptions and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST endpoints, bearer-token header guidance, WebSocket subscription details, workflow IDs, request bodies, and response shapes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
