## Description: <br>
Monitors system resource utilization and reports idle capacity for workload scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local CPU and memory availability before scheduling auxiliary workloads, planning capacity, or identifying low-load nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads basic local system utilization metrics, which may reveal machine capacity or load patterns. <br>
Mitigation: Install only where sharing local CPU and memory availability with the agent is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ink5725/capacity-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, guidance] <br>
**Output Format:** [JSON capacity report with timestamp, CPU idle percentage, available memory in MB, and status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single local capacity snapshot.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
