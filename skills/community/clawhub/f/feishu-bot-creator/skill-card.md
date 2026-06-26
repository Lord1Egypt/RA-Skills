## Description: <br>
Feishu Bot Creator automates creation and configuration of Feishu bots, including app creation, permission setup, and webhook configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[839305939wang](https://clawhub.ai/user/839305939wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to create Feishu bot applications, configure permissions and webhooks, and generate local bot configuration for follow-on automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and configures Feishu applications in a tenant. <br>
Mitigation: Install only when this administrative behavior is intended and run it with an account permitted to create Feishu applications. <br>
Risk: The generated configuration can contain app credentials. <br>
Mitigation: Protect or relocate the generated config file, avoid committing it, and avoid running the skill in logged terminals or CI. <br>
Risk: Requested Feishu permissions may be broader than needed. <br>
Mitigation: Use the smallest permission set required and review permissions before execution. <br>
Risk: A nonstandard FEISHU_API_BASE could send credentials to an unintended endpoint. <br>
Mitigation: Verify FEISHU_API_BASE points to the official Feishu endpoint before running. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/839305939wang/feishu-bot-creator) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or describes local Feishu bot configuration that can include app credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
