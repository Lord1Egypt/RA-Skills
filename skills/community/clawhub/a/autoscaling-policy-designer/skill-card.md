## Description: <br>
Design autoscaling policies based on traffic patterns, cost constraints, and performance SLOs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to analyze workload traffic, design Kubernetes HPA/KEDA or cloud autoscaling policies, simulate scaling behavior, and estimate cost impact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS autoscaling commands can change live cloud scaling behavior and affect service availability or cost. <br>
Mitigation: Confirm the account, region, Auto Scaling Group name, environment, expected cost impact, and rollback plan before running any command. <br>
Risk: Autoscaling recommendations based on incomplete or unrepresentative metrics can under-provision services or cause excessive scale-out. <br>
Mitigation: Review the traffic analysis, SLO assumptions, min/max capacity, cooldowns, and cost model with the service owner before applying generated policies. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include autoscaler configuration examples, traffic analysis reports, simulation snippets, and cost projection tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
