## Description: <br>
Performs SysOM performance profiling on Alibaba Cloud ACK cluster Pods to help diagnose Pod-level issues such as CPU throttling, out-of-memory events, memory distribution problems, network jitter, and I/O latency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to prepare Alibaba Cloud CLI tooling, confirm ACK Pod diagnosis parameters, and run SysOM profiling on standard ECS-backed ACK clusters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local Aliyun CLI configuration and create Alibaba Cloud networking or service-role state during diagnosis setup. <br>
Mitigation: Use a least-privilege Alibaba Cloud identity on an approved ACK cluster, require explicit approval before write operations, and review any created cloud resources for cleanup after use. <br>
Risk: The workflow requires access to sensitive Alibaba Cloud credentials or an authenticated CLI profile. <br>
Mitigation: Configure credentials outside the agent conversation, do not paste secrets into chat or command arguments, and verify access with the least privilege needed for the documented RAM actions. <br>
Risk: Security evidence reports clean static and VirusTotal scans but a suspicious verdict because some cloud changes are not consistently disclosed or gated. <br>
Mitigation: Review the planned SysOM initialization and VPC endpoint steps before execution, confirm the target cluster and namespace, and stop if the requested changes are not acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-aes-ack-pod-performance-profiling) <br>
- [Diagnosis workflow](references/diagnose-workflow.md) <br>
- [RAM permission policies](references/ram-policies.md) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Related commands](references/related-commands.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud RAM AccessKey console](https://ram.console.aliyun.com/manage/ak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides Alibaba Cloud CLI and local helper-script execution after required user parameters are confirmed.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
