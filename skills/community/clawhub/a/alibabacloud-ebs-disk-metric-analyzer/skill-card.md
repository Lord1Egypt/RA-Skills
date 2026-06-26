## Description: <br>
Queries and analyzes Alibaba Cloud EBS disk monitoring metrics for single or multiple cloud disks, including time-series aggregation and cross-disk analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations teams use this skill to inspect Alibaba Cloud EBS disk IOPS, bandwidth, utilization, and trend data across disks, ECS instances, disk categories, and availability zones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can run remote installer code and change global Alibaba Cloud CLI settings. <br>
Mitigation: Prefer a verified package manager or signed download, review CLI configuration changes before applying them, and confirm AI-mode is disabled after use. <br>
Risk: The skill requires Alibaba Cloud credentials and access to EBS metric APIs. <br>
Mitigation: Configure credentials outside the agent session, avoid pasting secrets into commands, and use a least-privilege RAM user or role limited to EBS metric reads. <br>


## Reference(s): <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Alibaba Cloud EBS Documentation](https://www.alibabacloud.com/help/en/ebs) <br>
- [OpenAPI Explorer - DescribeMetricData](https://api.aliyun.com/api/ebs/2021-07-30/DescribeMetricData) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only metric query guidance and verification steps; API responses are expected as JSON from Aliyun CLI.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
