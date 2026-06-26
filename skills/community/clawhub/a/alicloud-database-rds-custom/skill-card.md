## Description: <br>
查询阿里云自定义实例（RC 实例）。使用 aliyun CLI 调用 DescribeRCInstances API 查询 RDS 相关自定义实例。当用户需要查询 RC 实例、RDS 自定义实例或云资源时触发此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chucklong](https://clawhub.ai/user/Chucklong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to query Alibaba Cloud RDS Custom RC instances, related resources, monitoring metrics, and diagnostic details through aliyun CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface sensitive cloud inventory and access details such as private IPs, VPC IDs, KubeConfig, or VNC URLs. <br>
Mitigation: Treat command output and transcripts as sensitive operational data and avoid sharing them outside trusted channels. <br>
Risk: The skill requires Alibaba Cloud CLI credentials to query RDS Custom resources. <br>
Mitigation: Use a least-privileged read-only RAM user or temporary credentials for inventory and diagnostics. <br>
Risk: The documented CLI installation path uses a remote shell installer. <br>
Mitigation: Verify the AliCloud CLI installer and source before running the curl-based installation command. <br>


## Reference(s): <br>
- [DescribeRCInstances API Reference](references/api-docs.md) <br>
- [Aliyun CLI Documentation](https://help.aliyun.com/product/29987.html) <br>
- [RDS API Documentation](https://help.aliyun.com/document_detail/26223.html) <br>
- [OpenAPI DescribeRCInstances](https://api.aliyun.com/api?product=Rds&api=DescribeRCInstances) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud inventory fields such as instance IDs, private IPs, VPC IDs, KubeConfig references, and VNC URLs; handle outputs as sensitive operational data.] <br>

## Skill Version(s): <br>
1.14.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
