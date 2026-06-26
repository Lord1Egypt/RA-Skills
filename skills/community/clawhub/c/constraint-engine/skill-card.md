## Description: <br>
Learn from consequences, not instructions: generate and enforce constraints from experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate constraints from repeated, confirmed observations, check proposed actions against active constraints, manage circuit breaker state, and maintain the lifecycle of local guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently block or shape future agent actions through local guardrails. <br>
Mitigation: Review generated constraints before adoption, verify dependency skills before installing the full suite, and keep override and retirement workflows available for false positives or outdated rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/constraint-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown command responses, YAML configuration, and local workspace files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated constraints and local audit logs under declared workspace output paths.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
