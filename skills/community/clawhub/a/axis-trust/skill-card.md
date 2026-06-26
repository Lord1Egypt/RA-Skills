## Description: <br>
Check AI agent trust scores and credit ratings before interacting, delegating tasks, or transacting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonidas-esquire](https://clawhub.ai/user/leonidas-esquire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to look up AXIS trust and economic reliability signals before delegation, data sharing, or transactions. Authenticated users can also register agents, submit behavioral events, inspect score details, and manage API keys through AXIS endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent identifiers and event data may be sent to AXIS endpoints during trust checks and authenticated workflows. <br>
Mitigation: Use the skill only when sharing those identifiers and event details with AXIS is acceptable. <br>
Risk: Session cookies can be exposed through chat transcripts, command history, or process arguments when using authenticated shell examples. <br>
Mitigation: Avoid placing real session cookies in chat, logs, shell history, or long-lived process arguments; prefer safer local handling for credentials. <br>
Risk: Authenticated actions can register agents, submit positive or negative behavioral events, and create or revoke API keys. <br>
Mitigation: Require explicit human confirmation before registration, negative event submission, API key creation, or API key revocation. <br>
Risk: Shell helper scripts execute local commands and may be less suitable for untrusted AUID input. <br>
Mitigation: Prefer the Python trust-check example for untrusted AUIDs and review commands before execution. <br>


## Reference(s): <br>
- [AXIS Trust Infrastructure](https://axistrust.io) <br>
- [AXIS API Explorer](https://axistrust.io/api-explorer) <br>
- [AXIS Documentation](https://axistrust.io/docs) <br>
- [AXIS Agent Directory](https://axistrust.io/directory) <br>
- [ClawHub skill page](https://clawhub.ai/leonidas-esquire/axis-trust) <br>
- [Publisher profile](https://clawhub.ai/user/leonidas-esquire) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with curl commands, Python examples, JSON request and response shapes, and decision thresholds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that call AXIS public or authenticated endpoints and may reference session cookies supplied by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata and changelog, released 2026-03-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
