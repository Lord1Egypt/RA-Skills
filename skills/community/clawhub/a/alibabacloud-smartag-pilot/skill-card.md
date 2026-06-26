## Description: <br>
Queries Smart Access Gateway (SAG) configurations and performs status inspections through Alibaba Cloud OpenAPI, producing conversation summaries and inspection report files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud network operators, support engineers, and developers use this skill to inspect Alibaba Cloud SAG configuration, inventory, routing, access-control, and health signals with read-only API calls. It is intended for SAG troubleshooting, configuration review, and status inspection workflows that may produce Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local Aliyun CLI setup and plugin state. <br>
Mitigation: Review CLI installation or plugin update commands before execution and verify installers from Alibaba Cloud sources. <br>
Risk: The skill requires Alibaba Cloud credentials and can inspect SAG resources in the authorized account. <br>
Mitigation: Use least-privilege read-only RAM permissions or short-lived STS credentials, and never paste access keys into chat or commands. <br>
Risk: Generated scripts and reports may expose cloud inventory or configuration details. <br>
Mitigation: Review generated script paths and report destinations before running them, and handle output files as sensitive operational data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-smartag-pilot) <br>
- [Aliyun CLI Installation & Configuration Guide](artifact/references/cli-installation-guide.md) <br>
- [SAG OpenAPI Reference](artifact/references/openapi-reference.md) <br>
- [Mandatory Call Contracts](artifact/references/contract-skeletons.md) <br>
- [SAG Inspection Rules](artifact/references/inspection-rules.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [Verification Method](artifact/references/verification-method.md) <br>
- [Access Key Management](https://ram.console.aliyun.com/manage/ak) <br>
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/) <br>
- [Aliyun CLI Plugin Repository](https://github.com/aliyun/aliyun-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, generated Python snippets, JSON summaries, and optional Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write raw API responses under /tmp and SAG inspection reports in the workspace when the workflow requires files.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
