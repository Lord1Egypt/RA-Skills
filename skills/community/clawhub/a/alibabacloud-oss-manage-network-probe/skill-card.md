## Description: <br>
Alicloud Service Scenario-Based Skill for diagnosing local-to-OSS network state, upload/download bandwidth, download time, and local symlink issues with `aliyun ossutil probe`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to prepare the Alibaba Cloud CLI, run OSS probe workflows, and interpret local-to-OSS connectivity, throughput, download-time, and symlink diagnostic results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses existing Aliyun CLI credentials and can interact with OSS objects during diagnostics. <br>
Mitigation: Use a narrow RAM policy, verify credentials only with `aliyun configure list`, and do not provide AK/SK values in chat or command output. <br>
Risk: Some probe workflows may create, upload, download, or delete OSS test objects. <br>
Mitigation: Use a test bucket or disposable object path, confirm the exact `oss://bucket/object` before upload or delete steps, and agree on cleanup before running destructive commands. <br>
Risk: Presigned URLs and local probe logs may expose sensitive object access details if copied into chat or persisted unredacted. <br>
Mitigation: Use the documented file-and-script pattern for presigned URLs and redact query-string signature parameters in logs or final summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-oss-manage-network-probe) <br>
- [Implementation Boundaries](artifact/references/implementation-boundaries.md) <br>
- [RAM Policies](artifact/references/ram-polices.md) <br>
- [Related APIs and Commands](artifact/references/related-apis.md) <br>
- [Verification Method](artifact/references/verification-method.md) <br>
- [CLI Installation Guide](artifact/references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands, OSS object path checks, permission guidance, probe result interpretation, and cleanup recommendations.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
