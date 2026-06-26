## Description: <br>
Design chaos engineering experiments to test system resilience. Generate failure injection scenarios, define steady-state hypotheses, blast radius controls, and rollback procedures for services, networks, and infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to plan chaos engineering experiments, game days, readiness audits, and post-experiment reports for services, networks, and infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chaos experiments and commands can disrupt production services if run without authorization or controls. <br>
Mitigation: Treat outputs as plans for review; confirm authorization, cluster and namespace, blast radius, abort criteria, rollback, and least-privilege Kubernetes credentials before execution. <br>
Risk: Production examples may be copied directly into sensitive environments. <br>
Mitigation: Start in staging or a sandbox and adapt targets, durations, thresholds, and rollback actions to the current system before any production run. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed experiment definitions, safety controls, rollback steps, readiness scores, and findings reports for human review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
