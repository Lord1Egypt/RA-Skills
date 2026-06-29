## Description: <br>
Run a fail-closed governance preflight before consequential AI-agent actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentnomos](https://clawhub.ai/user/agentnomos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill before consequential actions to assess identity, authority, scope, risk, human approval requirements, and evidence readiness without executing the action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users or agents may mistake an advisory result for legal, compliance, or production authorization. <br>
Mitigation: Treat the result as a preflight checklist only and keep existing platform policies, user confirmations, and human approvals in force. <br>
Risk: Requests may contain secrets or sensitive raw data. <br>
Mitigation: Do not repeat sensitive values; redact them with neutral placeholders and block when secret exposure is detected. <br>
Risk: Incomplete authority, scope, approval, or evidence can lead to unsafe consequential action. <br>
Mitigation: Hold for review unless the actor, authority, scope, risk, required approval, and evidence are explicit and current. <br>


## Reference(s): <br>
- [AgentNOMOS](https://agentnomos.com) <br>
- [ClawHub skill page](https://clawhub.ai/agentnomos/skills/agentnomos-governance-preflight) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Concise explanation followed by structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory only; the skill returns a not_executed flag and does not authorize or execute the proposed action.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
