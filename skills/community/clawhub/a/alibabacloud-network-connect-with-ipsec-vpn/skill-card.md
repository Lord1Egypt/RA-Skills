## Description: <br>
Scenario-based skill for connecting Linux servers to Alibaba Cloud VPC via IPsec VPN using StrongSwan dual tunnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud network engineers use this skill to plan, create, verify, troubleshoot, and clean up a dual-tunnel IPsec VPN connection between a Linux server and an Alibaba Cloud VPC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create paid Alibaba Cloud VPN resources and modify VPC routes. <br>
Mitigation: Confirm region, VPC, VSwitches, bandwidth, billing period, route tables, and cleanup commands before execution. <br>
Risk: Server-side steps require root-level Linux networking and StrongSwan configuration changes. <br>
Mitigation: Run pre-checks, back up existing StrongSwan configuration, validate swanctl configuration, and keep rollback commands available. <br>
Risk: Credential and PSK handling can expose sensitive access or tunnel secrets. <br>
Mitigation: Use least-privilege RAM credentials or short-lived roles, do not print AK/SK or PSK values, generate a fresh PSK, and avoid sharing credential-bearing output. <br>
Risk: Disabling SSH host key verification can weaken server identity checks. <br>
Mitigation: Keep SSH host key verification enabled unless a reviewed operational exception is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-network-connect-with-ipsec-vpn) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Server-side Pre-check](references/server-precheck.md) <br>
- [StrongSwan Configuration Reference](references/strongswan-config.md) <br>
- [StrongSwan Quick Setup Guide](references/strongswan-config-templates/QUICKSTART.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Related APIs and CLI Commands](references/related-apis.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guided workflow requires user confirmation before cloud, billing, route, firewall, credential, and deletion actions.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
