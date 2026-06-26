## Description: <br>
Route risky communications next steps through a typed action-intent bridge so external writes, bookings, settings changes, public posts, and spend decisions require explicit policy and approval handling instead of informal reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyalerio](https://clawhub.ai/user/heyalerio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to convert risky communication and external-write next steps into explicit typed proposals before execution. It is intended for workflows where sends, posts, bookings, settings changes, API writes, or spend decisions need policy and approval handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routed HTTP write requests may have high impact if the downstream sidecar or proxy executes them after approval. <br>
Mitigation: Review the configured endpoint environment variables and use the bridge only with an intended local or configured action-gate sidecar. <br>
Risk: Risky external actions could be sent, posted, confirmed, or spent without sufficient review if approval status is unclear. <br>
Mitigation: Treat red actions as requiring explicit user approval and escalate when policy, scope, approval, or reversibility is unclear. <br>


## Reference(s): <br>
- [Action Bridge](references/action-bridge.md) <br>
- [Approval Matrix](references/approval-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON action proposals or routing responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes proposals and HTTP write intents through configured local sidecar endpoints.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
