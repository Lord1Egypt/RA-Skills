## Description: <br>
Checks MCP skills for trust scores, staking, sybil resistance, and attestation signals to guide secure skill usage decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drewM33](https://clawhub.ai/user/drewM33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to request an advisory trust lookup before deciding whether to use another MCP skill. It helps summarize reputation, staking, sybil, and attestation signals without requiring credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried skill IDs are sent to a publisher-operated hosted API. <br>
Mitigation: Use the lookup only when a trust check is appropriate, and avoid sending sensitive user data or private context in the skill ID. <br>
Risk: A high trust score may be mistaken for a complete security review. <br>
Mitigation: Treat ClawMon results as advisory and still review permissions, source, and task sensitivity before using another skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drewM33/clawmon) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown or plain-text guidance with JSON-derived trust-score details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only HTTPS lookups are used for trust checks; optional feedback is only submitted when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
