## Description:

Orchestrates external AI planners by validating, scheduling, executing tools, enforcing budgets, and providing replayable telemetry for plans and runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonightwatch](https://clawhub.ai/user/nonightwatch)

### License/Terms of Use:


## Use Case:

Developers and external AI client operators use this skill to validate plans, schedule and execute tool-enabled multi-agent runs, enforce budgets, and retrieve telemetry or replay outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared deployments have serious access-control gaps according to the ClawHub security summary.

Mitigation: Install only in a tightly controlled environment, avoid shared or multi-tenant use until controls are fixed, and require run tokens for access-controlled endpoints.

Risk: Outbound provider and callback behavior can expose task inputs, dependency payloads, and tool payloads.

Mitigation: Keep tool registration disabled for untrusted users, configure explicit outbound allowlists, and avoid callback credentials for untrusted registrants.

Risk: Persisted run files and replay data may contain sensitive plaintext records.

Mitigation: Treat persisted run files as sensitive data, restrict storage access, and enable telemetry redaction for shared deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nonightwatch/skills/agentmanager)
- [README](README.md)
- [Skill integration guide](skill.md)
- [OpenAPI document](openapi/openapi.json)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON, configuration]

**Output Format:** [Markdown integration guidance with JSON API request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes run events, replay telemetry, budget and cost metrics, and OpenAPI-compatible endpoint descriptions.]

## Skill Version(s):

1.0.2 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
