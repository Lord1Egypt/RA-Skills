## Description: <br>
Forecast infrastructure capacity needs using historical metrics, growth projections, and cost modeling. Identify bottlenecks before they cause outages and right-size resources to avoid over-provisioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to forecast capacity limits, identify scaling bottlenecks, right-size resources, and model infrastructure cost growth from historical metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example commands may query the wrong Prometheus, CloudWatch, Datadog, or local system environment if variables or credentials point to unintended infrastructure. <br>
Mitigation: Confirm each target environment before execution and use read-only monitoring credentials where possible. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, formulas, and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-oriented capacity-planning guidance; users should verify target monitoring systems and credentials before running example commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
