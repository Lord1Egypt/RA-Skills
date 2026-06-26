## Description: <br>
Tamper-evident audit logger that pairs with Guardian safety skill and captures safety decisions, approvals, halts, escalations, and execution outcomes in an append-only, hash-chained log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tooled-app](https://clawhub.ai/user/tooled-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to record safety-gate decisions and compliance-relevant agent actions for later review, incident reconstruction, and audit reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit logs can contain sensitive paths, commands, reasoning, approval context, personal data, or business data. <br>
Mitigation: Define log storage, access control, retention, redaction, and encryption requirements before installation. <br>
Risk: Integrity and compliance claims may be overstated if the logger is treated as complete proof of all agent activity. <br>
Mitigation: Run the dedicated chain verifier before trusting log integrity and use the audit trail as one control among broader monitoring and compliance processes. <br>
Risk: The skill records decisions after they occur and does not itself block unsafe actions. <br>
Mitigation: Pair it with an appropriate safety gatekeeper and periodically test that expected safety decisions are actually captured. <br>


## Reference(s): <br>
- [Guardian Audit ClawHub release](https://clawhub.ai/tooled-app/data-guardian-audit) <br>
- [Guardian project](https://github.com/openclaw/guardian) <br>
- [Log Schema](LOG-SCHEMA.md) <br>
- [Compliance Mapping](COMPLIANCE-MAPPING.md) <br>
- [Replay and Analysis](REPLAY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON log records and Python or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces append-only NDJSON audit entries, chain verification output, and Markdown compliance reports.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
