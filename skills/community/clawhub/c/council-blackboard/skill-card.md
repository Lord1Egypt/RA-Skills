## Description:

Visible OpenClaw-Open WebUI council rooms with typed blackboards and session handovers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate bounded OpenClaw and Open WebUI model council sessions through visible chat rooms, typed blackboard entries, validation steps, and short handovers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent council transcripts and absolute board paths may expose sensitive collaboration context in shared Open WebUI environments.

Mitigation: Use only in administrator-approved environments with clear user disclosure, retention and deletion rules, and a policy against adding private memory to council rooms.

Risk: Direct Open WebUI database writes and configurable helper paths can affect shared service state.

Mitigation: Restrict configuration of OPENWEBUI_DB, COUNCIL_BLACKBOARD_SCRIPT, COUNCIL_ROOM_SCRIPT, and related helper paths to trusted administrators, and review the deployment before enabling it for multiple users.

Risk: The security evidence flags insufficient per-user authorization around broad board and Open WebUI access.

Mitigation: Add board ownership checks and access controls before shared deployment, and validate each board before every handoff or routed model turn.

Risk: The tool can launch OpenClaw jobs and route content to the configured OpenClaw model.

Mitigation: Limit allowed models and agents to approved choices, keep route leases bounded, and monitor or cancel live routes when they fail or exceed expected behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinguy/skills/council-blackboard)
- [Server-resolved GitHub provenance](https://github.com/pinguy/Skills/tree/main/skills/council-blackboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON helper outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent Open WebUI chat records and JSON blackboard files when the helper scripts run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
