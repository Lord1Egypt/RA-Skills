## Description: <br>
Alibaba Cloud private network connectivity diagnosis tool for ECS, VPC, NAT, CEN, VPN, Express Connect, security group, network ACL, and route-table issues; not for classic network, public internet access, DNS resolution, CDN, SLB, or WAF issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to collect read-only Alibaba Cloud network metadata, diagnose private connectivity failures, and produce a structured report with root causes and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VPN diagnostics may expose VPN pre-shared keys in collected output. <br>
Mitigation: Avoid VPN Gateway cases until PSK fields are removed or redacted, and review any diagnostic artifacts before sharing them. <br>
Risk: The skill may automatically install missing Alibaba Cloud CLI plugins while running diagnostics. <br>
Mitigation: Require explicit approval before plugin installation, or preinstall and review the required official CLI plugins in a controlled environment. <br>
Risk: Diagnostics use configured Alibaba Cloud credentials to query network metadata across relevant services and regions. <br>
Mitigation: Use a least-privilege read-only RAM policy and limit execution to accounts and regions appropriate for the investigation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-network-diagnose) <br>
- [Alibaba Cloud CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [API Reference](references/api-reference.md) <br>
- [CEN and Transit Router Diagnosis](references/cen-diagnosis.md) <br>
- [Diagnosis Examples](references/examples.md) <br>
- [Diagnosis Report Template](references/report-template.md) <br>
- [Root Cause Priority](references/root-cause-priority.md) <br>
- [VPN Gateway Route Overview](https://help.aliyun.com/zh/vpn/sub-product-ipsec-vpn/user-guide/vpn-gateway-route-overview/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with JSON-backed diagnostic summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.7+, Alibaba Cloud CLI, configured Alibaba Cloud credentials, and user-provided source and destination endpoint details.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
