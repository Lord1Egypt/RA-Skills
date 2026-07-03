## Description: <br>
Inspects Alibaba Cloud network products using read-only queries, analyzes utilization and health signals, and generates Markdown inspection reports with charts, risk assessment, and scaling recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers and network administrators use this skill to inspect Alibaba Cloud EIP, bandwidth package, NAT Gateway, CEN, Transit Router, Physical Connection, VBR, Global Accelerator, CLB, ALB, and NLB resources for utilization, packet loss, capacity, and pre-launch risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses configured Alibaba Cloud credentials to inventory network resources and produce reports containing infrastructure and monitoring details. <br>
Mitigation: Run it with a least-privilege read-only RAM policy and review generated reports before sharing them. <br>
Risk: The setup workflow may install Python packages, update aliyun CLI plugins, and change global aliyun AI-mode configuration. <br>
Mitigation: Review those steps before execution, perform dependency changes in a controlled environment, and disable AI-mode after the inspection completes. <br>
Risk: The optional DingTalk publishing path can upload detailed infrastructure reports and chart data to an external document service. <br>
Mitigation: Use DingTalk publication only with explicit user intent and confirmed destination access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-network-health-inspection) <br>
- [RAM Permission Guide](references/ram-policies.md) <br>
- [Aliyun CLI releases](https://github.com/aliyun/aliyun-cli/releases) <br>
- [DingTalk Docs MCP service](https://aihub.dingtalk.com/#/detail?instanceId=474175&detailType=instanceMcpDetail&mcpId=9629) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with generated chart files, JSON inspection data, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-specified time range and data aggregation period; optional DingTalk publication can publish the generated report and charts.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
