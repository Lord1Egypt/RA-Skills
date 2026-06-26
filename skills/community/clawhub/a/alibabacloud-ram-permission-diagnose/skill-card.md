## Description: <br>
Alibaba Cloud RAM permission diagnosis and repair assistant for permission-related errors while operating Alibaba Cloud resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to diagnose Alibaba Cloud RAM permission errors, identify missing permissions or denial causes, and produce least-privilege repair guidance. It can also guide CLI or console-based remediation after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local Aliyun CLI configuration, including AI-mode and plugin behavior. <br>
Mitigation: Review setup steps before use, avoid remote installer or automatic plugin updates unless intentionally approved, and verify AI-mode and auto-plugin settings after the workflow ends. <br>
Risk: Repair actions can make high-impact Alibaba Cloud access-control changes. <br>
Mitigation: Use a dedicated least-privileged Alibaba Cloud profile, inspect every RAM policy or trust-policy change before execution, and keep rollback details and policy backups. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/sdk-team/alibabacloud-ram-permission-diagnose) <br>
- [Diagnose Flow Reference](references/diagnose-flow.md) <br>
- [Alibaba Cloud RAM Permission ErrorCode Reference](references/error-codes.md) <br>
- [Popular Services RAM Action Reference](references/hot-services-ram.md) <br>
- [RAM-Related aliyun CLI Command Reference](references/ram-cli-commands.md) <br>
- [RAM Hints for ram-permission-diagnose Skill](references/ram-policies.md) <br>
- [Alibaba Cloud RAM troubleshooting documentation](https://help.aliyun.com/document_detail/93733.html) <br>
- [Alibaba Cloud RAM authorization action list](https://help.aliyun.com/document_detail/28630.html) <br>
- [Alibaba Cloud RAM policies console](https://ram.console.aliyun.com/policies) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud RAM policy statements, CLI commands, console steps, rollback guidance, and permission request materials.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
