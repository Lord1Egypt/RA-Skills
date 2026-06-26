## Description: <br>
Inspect ECS instance health, detect anomalies in memory, disk, CPU, load, and resource leaks, and automatically trigger deep diagnosis when critical memory issues are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Alibaba Cloud ECS instance health, choose or target instances, review SysOM inspection reports, and trigger memory-focused diagnosis when reports identify critical memory usage anomalies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials to inspect ECS instances and call SysOM APIs. <br>
Mitigation: Install and run it only when SysOM inspection is intended, and use scoped Alibaba Cloud RAM credentials with the actions documented in references/ram-policies.md. <br>
Risk: SysOM activation and agent installation can change the target cloud environment. <br>
Mitigation: Review the activation prompt before confirming; in non-interactive runs, provide a ready SysOM environment and target instance so the skill does not need activation flow. <br>
Risk: Memory anomalies can trigger automatic memgraph diagnosis. <br>
Mitigation: Use --disable-memgraph-diagnosis when automatic memory diagnosis is not desired. <br>


## Reference(s): <br>
- [RAM Policies](references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON-formatted inspection and diagnosis results when the CLI is run with --json.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
