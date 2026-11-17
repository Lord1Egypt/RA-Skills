## Description:

FlowFi provides REST and WebSocket API guidance for authorization, smart accounts, workflow generation and lifecycle operations, executions, token prices, templates, DTOs, and real-time workflow status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devarogundade](https://clawhub.ai/user/devarogundade)

### License/Terms of Use:


## Use Case:

Developers and external integrators use this skill to build agents that call FlowFi APIs for creating, editing, deploying, monitoring, and managing workflows tied to smart accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill may receive bearer tokens that permit broad FlowFi account and workflow control.

Mitigation: Use short-lived, narrowly scoped tokens where possible, keep JWTs out of URLs and logs, and revoke tokens that are no longer needed.

Risk: Workflow actions such as deploy, start, edit, cancel, stop, and delete can materially affect user workflows and may trigger transactions or public notifications.

Mitigation: Require explicit user confirmation before state-changing workflow or execution operations.

## Reference(s):

- [FlowFi ClawHub Skill Page](https://clawhub.ai/devarogundade/skills/flowfi)
- [FlowFi Documentation Index](docs/README.md)
- [Authorization](docs/authorization.md)
- [Smart Accounts](docs/smart-accounts.md)
- [AI Workflows](docs/ai-workflows.md)
- [Workflow REST API](docs/workflows.md)
- [DTO and Request/Response Shapes](docs/dto.md)
- [Execution REST API](docs/execution.md)
- [WebSocket Real-Time Status](docs/websocket.md)
- [Price API](docs/price.md)
- [Templates API](docs/templates.md)
- [Endpoint Summary](docs/summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP endpoints and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST endpoint summaries, WebSocket event shapes, bearer-token usage guidance, DTO schemas, and workflow lifecycle instructions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
