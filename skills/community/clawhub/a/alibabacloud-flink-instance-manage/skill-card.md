## Description:

Manage Alibaba Cloud Flink instances, namespaces, regions, availability zones, tags, and regional Flink AI service status, quota, activation, and closure protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to create or inspect Alibaba Cloud Flink instances and namespaces, discover supported regions, zones, and tags, and manage regional Flink AI service settings. Write actions require confirmation and are followed by a state check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with medium confidence because local evaluation-file preparation may not fit its stated Flink management purpose; the scan was incomplete.

Mitigation: Before installing, review the evaluation-file preparation behavior and its inputs; the scan did not inspect every component.

Risk: Creating instances or namespaces and changing regional Flink AI service settings can modify cloud resources.

Mitigation: Confirm the exact target and parameters before each write, then query the resource to verify the resulting state.

## Reference(s):

- [ClawHub release](https://clawhub.ai/sdk-team/skills/alibabacloud-flink-instance-manage)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [Quick start](artifact/references/quick-start.md)
- [Flink AI service guide](artifact/references/flink-ai-service.md)
- [RAM permissions](artifact/references/ram-policies.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON operation results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require explicit confirmation and follow-up state verification.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
