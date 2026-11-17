## Description: <br>
Public network MTR diagnosis skill that guides manual MTR collection and can automate Alibaba Cloud ECS diagnostics through Cloud Assistant for connectivity failures, latency, packet loss, SLB health check failures, NAT outbound issues, and related public network problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and support engineers use this skill to diagnose public network link quality from local machines or Alibaba Cloud ECS instances. It helps collect and interpret MTR, ping, and curl results, compare forward and reverse paths, and produce recommended troubleshooting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated mode can invoke Alibaba Cloud Cloud Assistant RunCommand on ECS instances, which enables remote shell execution. <br>
Mitigation: Use tightly scoped Alibaba Cloud credentials, restrict ecs:RunCommand to the specific ECS instances needed, and require explicit confirmation before every remote command. <br>
Risk: The workflow can install mtr on a remote ECS instance when the tool is missing. <br>
Mitigation: Ask for explicit user consent before package installation and fall back to manual instructions if consent is not granted. <br>
Risk: The raw run-command path can execute custom scripts beyond the standard diagnostic workflow. <br>
Mitigation: Remove or disable the raw run-command path in sensitive or production environments unless a separate review approves it. <br>
Risk: ISP enrichment can query ipinfo.io with network hop IP addresses. <br>
Mitigation: Disable external enrichment or rely on offline prefix matching when working with sensitive network information. <br>


## Reference(s): <br>
- [Required RAM Permissions](artifact/references/ram-policies.md) <br>
- [MTR Metrics Detailed Reference](artifact/references/reference.md) <br>
- [Alibaba Cloud RAM Documentation](https://www.alibabacloud.com/help/en/ram) <br>
- [Aliyun CLI Download](https://aliyuncli.alicdn.com) <br>
- [WinMTR Releases](https://github.com/White-Tiger/WinMTR/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON diagnostic outputs from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce diagnostic conclusions, severity labels, path analysis, and recommended actions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
