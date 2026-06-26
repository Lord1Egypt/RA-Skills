## Description: <br>
Orchestrates external AI planners by validating, scheduling, executing tools, enforcing budgets, and providing replayable telemetry for plans and runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoNightWatch](https://clawhub.ai/user/NoNightWatch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI client builders use this skill to run external planner workflows through an orchestration service that validates plans, schedules tasks, controls budgets, executes tools, and exposes replayable run telemetry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive run data or mutation endpoints could be exposed in shared or network-accessible deployments. <br>
Mitigation: Require strong run tokens, add owner checks before exposing run IDs, and restrict run, replay, report, event, cancellation, and injection endpoints to intended tenants. <br>
Risk: Callback tools and provider gateways can send task inputs, dependency payloads, and tool payloads to outbound destinations. <br>
Mitigation: Keep outbound allowlists strict, keep tool registration disabled unless needed, avoid OUTBOUND_ALLOW_ALL, and verify callback destinations against TOOL_CALLBACK_ALLOWLIST. <br>
Risk: Telemetry, replay, reports, events, or streams can contain sensitive execution data. <br>
Mitigation: Enable telemetry redaction for shared deployments and avoid sharing unredacted replay or report data outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NoNightWatch/agentmanager) <br>
- [Agent Manager README](README.md) <br>
- [Agent Manager integration contract](skill.md) <br>
- [Agent Manager OpenAPI specification](openapi/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, HTTP endpoint descriptions, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include plan validation results, run identifiers, event streams, replay JSON, reports, and tool execution telemetry.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
