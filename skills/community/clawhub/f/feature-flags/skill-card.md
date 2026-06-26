## Description: <br>
Deep feature flag workflow--taxonomy, targeting, lifecycle, safety and kill switches, cleanup, and governance for gradual shipping, experimentation, and decoupling deploy from release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release teams use this skill to plan and review feature flag practices for gradual rollouts, experiments, kill switches, stale-flag cleanup, and governance across environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feature flag guidance may be misapplied to security or billing controls if client-side flags are treated as authoritative. <br>
Mitigation: Keep security- and billing-sensitive decisions server-side, and use client-side flags only for user experience changes. <br>
Risk: Long-lived or ownerless flags can create release debt and unclear production behavior. <br>
Mitigation: Assign owners, expected TTLs, cleanup tickets, and periodic stale-flag audits for every flag. <br>
Risk: Provider outage or misconfiguration can expose the wrong default behavior. <br>
Mitigation: Define safe defaults, kill-switch runbooks, and audit trails before broad rollout. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only planning aid; no executable behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
