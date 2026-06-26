## Description: <br>
Alibaba Cloud PolarDB Database AI Assistant for PolarDB MySQL/PostgreSQL cluster management, performance diagnostics, parameter tuning, slow SQL analysis, backup recovery, connection/session analysis, primary-standby switchover diagnostics, security configuration audit, and related O&M operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database operators, cloud administrators, and support engineers use this skill to run Alibaba Cloud PolarDB diagnostic workflows through the Aliyun CLI and DAS/YaoChi agent. It helps investigate performance, slow SQL, backup, storage, connection, failover, parameter, and security configuration questions for existing PolarDB clusters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an existing Alibaba Cloud CLI profile and may operate in contexts with sensitive cloud credentials. <br>
Mitigation: Use OAuth, STS, or a least-privilege RAM profile; avoid root or broad production credentials; do not paste secrets into prompts or commands; and redact CLI configuration output before sharing. <br>
Risk: Installation guidance includes remote installer URLs and local CLI/plugin updates. <br>
Mitigation: Verify installer URLs and package sources before running setup commands, and install or update the Aliyun CLI and DAS plugin through trusted channels. <br>
Risk: AI-mode and custom user-agent settings modify local Aliyun CLI behavior for skill execution. <br>
Mitigation: Enable AI-mode only for the diagnostic workflow and confirm it is disabled after the workflow completes or exits. <br>
Risk: Diagnostic guidance about parameters, failover, or performance can affect production database operations if applied without review. <br>
Mitigation: Confirm all user-customizable parameters with the operator, validate recommendations in a test environment when possible, and follow normal change-control review for production changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-polardb-ai-assistant) <br>
- [Aliyun CLI installation and configuration guide](references/cli-installation-guide.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud RAM permission guide](https://help.aliyun.com/document_detail/116146.html) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and streamed diagnostic text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session IDs for multi-turn diagnostic conversations and stderr status output from the CLI wrapper.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
