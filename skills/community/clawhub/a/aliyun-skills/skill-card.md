## Description: <br>
Manage Alibaba Cloud resources using the Aliyun CLI tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hambaobao](https://clawhub.ai/user/hambaobao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to construct, explain, and review Aliyun CLI commands for Alibaba Cloud resources such as ECS, VPC, OSS, RDS, SLB/CLB, RAM, DNS, and ACR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud administration commands can delete, expose, or reconfigure Alibaba Cloud resources. <br>
Mitigation: Use least-privilege RAM roles or temporary credentials, verify the active profile, region, and resource IDs, and require explicit confirmation before destructive or exposure-changing commands. <br>
Risk: Credentials, passwords, private keys, signed URLs, or debug logs may expose sensitive cloud access. <br>
Mitigation: Do not paste secrets into chat or shared terminals; prefer RAM roles, environment variables, and temporary credentials. <br>
Risk: Provisioning, bandwidth, storage, and instance-size changes can incur cost. <br>
Mitigation: Call out cost implications before create, resize, bandwidth, or public endpoint operations. <br>
Risk: Wrong region, profile, or resource ID can cause actions against unintended resources. <br>
Mitigation: Run describe/list commands first, present the resolved target, and confirm ambiguous targets before acting. <br>


## Reference(s): <br>
- [Aliyun CLI Skill](SKILL.md) <br>
- [Setup and Authentication](references/setup.md) <br>
- [ECS Reference](references/ecs.md) <br>
- [VPC Reference](references/vpc.md) <br>
- [OSS Reference](references/oss.md) <br>
- [RDS Reference](references/rds.md) <br>
- [SLB / CLB Reference](references/slb.md) <br>
- [RAM Reference](references/ram.md) <br>
- [AliDNS Reference](references/dns.md) <br>
- [ACR Reference](references/acr.md) <br>
- [Aliyun CLI GitHub Repository](https://github.com/aliyun/aliyun-cli) <br>
- [ossutil Installation Documentation](https://help.aliyun.com/zh/oss/developer-reference/install-and-configure-ossutil) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Aliyun CLI and ossutil commands intended for review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
