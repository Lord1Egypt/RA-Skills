## Description: <br>
天翼云CLI工具 - 企业级命令行工具，帮助您轻松管理天翼云资源。支持ECS、VPC、EBS、ELB、CCE、Redis、Kafka、CSS、EMR、监控、账务、IAM、Aone、CloudPC、AIServer、Audit、IMS、LTS、SFS、OceanFS、ZOS、DPS物理机等26+服务模块，覆盖510+个API，478+个命令。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengyucn](https://clawhub.ai/user/fengyucn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and cloud administrators use this skill to install and operate the ctyun-cli command-line tool for managing Tianyi Cloud resources across compute, networking, storage, monitoring, billing, IAM, and related services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure while configuring Tianyi Cloud access keys. <br>
Mitigation: Prefer environment variables or a protected configuration file, and avoid placing real secrets directly in shell history or shared command transcripts. <br>
Risk: Commands may modify or delete live cloud resources when resource IDs, regions, or profiles are incorrect. <br>
Mitigation: Review generated commands before execution, double-check IDs and selected profiles, and use read-only list/detail commands first when possible. <br>
Risk: Installing the CLI adds a cloud-management tool capable of authenticated actions on the local machine. <br>
Mitigation: Install only on machines intended to manage Tianyi Cloud resources and limit credentials to the minimum required account permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengyucn/skills/ctyun) <br>
- [PyPI package](https://pypi.org/project/ctyun-cli/) <br>
- [Project homepage](https://github.com/fengyucn/ctyun-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide credential configuration and cloud-resource operations that require user review before execution.] <br>

## Skill Version(s): <br>
1.22.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
