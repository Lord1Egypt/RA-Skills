## Description: <br>
Meta-skill for AI agent self-improvement that analyzes runtime logs to detect error patterns, regressions, and inefficiencies, then generates structured improvement proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackey001-wq](https://clawhub.ai/user/jackey001-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect structured runtime logs, identify recurring failures or regressions, compute health scores, and produce prioritized improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime logs can contain secrets, personal data, tenant identifiers, or stack traces that should not be retained or shared unnecessarily. <br>
Mitigation: Redact sensitive fields before passing logs to the skill, especially when using production or fleet logs. <br>
Risk: Generated recommendations may be incomplete or unsuitable for a specific production environment. <br>
Mitigation: Review recommendations before storing them, applying changes, or turning them into automated remediation tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackey001-wq/capability-evolver-pro-1-0-2) <br>
- [Claw0x Capability Evolver](https://claw0x.com/skills/capability-evolver) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON objects containing detected patterns, health scores, recommendations, evolution proposals, status details, or validation errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local deterministic processing; analyze and evolve actions require structured log entries, and outputs may include up to 50 patterns and 20 recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
