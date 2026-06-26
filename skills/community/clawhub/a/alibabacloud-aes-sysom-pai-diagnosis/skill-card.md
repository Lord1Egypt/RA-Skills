## Description: <br>
Perform SysOM deep diagnosis on Alibaba Cloud PAI products (EAS and DLC) to identify root causes of instance-level performance and health issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to guide Alibaba Cloud PAI EAS and DLC diagnostics, validate required parameters and resources, run SysOM diagnosis through the aliyun CLI, and summarize completed diagnosis results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Alibaba Cloud credentials and verifies local credential configuration. <br>
Mitigation: Use a least-privilege RAM identity, configure credentials outside the agent session, and redact account identifiers, access keys, tokens, and profile details before sharing CLI output. <br>
Risk: The workflow can make persistent aliyun CLI configuration and plugin changes. <br>
Mitigation: Review the commands before execution and be prepared to manually restore settings such as auto-plugin-install, user-agent, AI-Mode, and plugin versions after use. <br>
Risk: SysOM initialization may grant or alter authorization needed for diagnosis. <br>
Mitigation: Review the initial-sysom authorization effect and required RAM permissions before running the workflow. <br>


## Reference(s): <br>
- [Diagnosis Execution Detailed Workflow](references/diagnose-workflow.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Success Verification Methods](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Releases](https://github.com/aliyun/aliyun-cli/releases) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-aes-sysom-pai-diagnosis) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Analysis] <br>
**Output Format:** [Markdown with inline bash commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries must be based on completed SysOM diagnosis results and should not expose cloud credential values.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
