## Description: <br>
Inspects Alibaba Cloud Redis and Tair instances and generates health reports covering instance details, sessions, resource trends, big and hot keys, slow logs, alerts, and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to run read-only health inspections for Alibaba Cloud Redis or Tair instances, including single-instance, multi-instance, and full-account checks. It helps produce operational reports that identify resource pressure, connection patterns, slow commands, key risks, alerts, and remediation priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Aliyun CLI setup and install required CLI plugins. <br>
Mitigation: Review plugin installation and CLI configuration changes before running the skill. <br>
Risk: The skill inspects Alibaba Cloud Redis or Tair resources through an Aliyun profile, and full-account mode can broaden access to diagnostics. <br>
Mitigation: Use a least-privilege RAM role or user, avoid root AccessKeys, and avoid full-account mode unless it is needed. <br>
Risk: Generated reports may contain sensitive operational data such as client IPs, instance details, Redis key names, and workload patterns. <br>
Mitigation: Treat generated reports as sensitive, store them in restricted locations, and limit sharing to authorized reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-kvstore-health-inspection) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [KVStore Health Inspection Manual Workflow](references/manual-workflow.md) <br>
- [RAM Permissions for KVStore Health Inspection](references/ram-policies.md) <br>
- [KVStore Health Inspection Report Format Specification](references/report-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [HTML reports by default, with optional Markdown or plain text reports and concise terminal status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports instance IDs or full-account mode, optional region, inspection window, inspection item filters, Aliyun profile, output path, and report format.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
