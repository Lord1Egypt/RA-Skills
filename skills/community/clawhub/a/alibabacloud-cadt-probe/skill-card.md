## Description: <br>
Discovers Alibaba Cloud resources through the CADT probe service, inventories resource distribution, exports JSON results, and queries related resources for selected assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Alibaba Cloud account inventory, export machine-readable resource data, summarize resource distribution, and query relationships such as ECS instances to security groups or VSwitches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal sensitive infrastructure inventory through probe results and exported JSON. <br>
Mitigation: Install only for intended Alibaba Cloud accounts and protect exported JSON as sensitive infrastructure data. <br>
Risk: Broad discovery permissions can expose more resources than needed for a task. <br>
Mitigation: Prefer scoped RAM permissions and use explicit --regions and --list-types filters. <br>
Risk: Debug output may include detailed API response data. <br>
Mitigation: Avoid --debug unless actively troubleshooting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-cadt-probe) <br>
- [Alibaba Cloud Config Console](https://config.console.aliyun.com/) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Alibaba Cloud Region List](references/regions.md) <br>
- [CADT Probe Supported Resource Types](references/resource_types.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quiet JSON output, summary-only output, explicit output files, resource type and region filters, and related-resource queries.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
