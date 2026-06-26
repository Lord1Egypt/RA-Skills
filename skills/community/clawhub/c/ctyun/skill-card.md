## Description: <br>
天翼云 CLI helper for managing Tianyi Cloud resources across ECS, VPC, EBS, ELB, CCE, Redis, Kafka, CSS, EMR, monitoring, billing, IAM, Aone, CloudPC, AIServer, and related services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengyucn](https://clawhub.ai/user/fengyucn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to install, configure, and operate the ctyun-cli command-line tool for Tianyi Cloud resource management. It helps produce CLI commands and configuration guidance for cloud inventory, monitoring, billing, IAM, container, networking, storage, and service-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials and account permissions may be exposed or overused during CLI setup and command execution. <br>
Mitigation: Use a dedicated least-privilege Tianyi Cloud key, prefer isolated installation with pipx, and avoid entering real secrets directly on the command line or in chat. <br>
Risk: Resource-changing, IAM, billing, kubeconfig, or debug commands can affect live cloud environments or reveal sensitive operational details. <br>
Mitigation: Review resource IDs, regions, permissions, and command intent before running create, update, delete, IAM, billing, kubeconfig, or debug commands. <br>
Risk: Package or source trust must be confirmed before installing a cloud administration CLI. <br>
Mitigation: Verify the PyPI package and listed project source before use, then install in an isolated environment where practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengyucn/ctyun) <br>
- [PyPI package: ctyun-cli](https://pypi.org/project/ctyun-cli/) <br>
- [Project homepage listed in artifact](https://github.com/fengyucn/ctyun-cli) <br>
- [Issue tracker listed in artifact](https://github.com/fengyucn/ctyun-cli/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference cloud credentials, regions, resource IDs, output formats, profiles, and package installation commands.] <br>

## Skill Version(s): <br>
1.18.5 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
