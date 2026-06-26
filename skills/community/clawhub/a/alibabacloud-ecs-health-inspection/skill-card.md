## Description: <br>
Performs read-only health inspection for a single Alibaba Cloud ECS instance, covering resource usage, data-source fallback, and a structured local report with findings and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators, site reliability engineers, and support engineers use this skill to inspect one Alibaba Cloud ECS instance for CPU, memory, disk, network, disk capacity, and GPU health. It helps collect read-only evidence and produce a local HTML report for troubleshooting and operational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs access to an Alibaba Cloud account profile and may use sensitive cloud credentials already configured on the machine. <br>
Mitigation: Confirm the trusted Alibaba Cloud profile before use, do not expose AK/SK values, and rely on the documented credential-status check rather than printing secrets. <br>
Risk: Aliyun CLI and plugin setup steps can change local CLI configuration. <br>
Mitigation: Review installation and plugin update steps before running them, and use the documented cleanup step so AI-mode does not persist after inspection. <br>
Risk: Limited RAM permissions or an unavailable CloudMonitor agent can reduce metric coverage. <br>
Mitigation: Use the documented fallback path, preserve permission-failure checkpoints, and clearly label unavailable metrics in the generated report. <br>


## Reference(s): <br>
- [Inspection Commands](artifact/references/inspection-commands.md) <br>
- [Degradation Paths and JSON Validation](artifact/references/degradation-and-validation.md) <br>
- [RAM Permissions](artifact/references/ram-policies.md) <br>
- [Aliyun CLI installation guide](https://help.aliyun.com/zh/cli/install-cli-on-macos-or-linux) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands, structured JSON input, and a local HTML report file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicitly confirmed instance_id and region_id; uses read-only ECS and CloudMonitor queries.] <br>

## Skill Version(s): <br>
0.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
