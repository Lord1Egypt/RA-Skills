## Description: <br>
Installs Alibaba Cloud CLI (aliyun) and guides deployment of applications or AI agents to Alibaba Cloud ECS with aliyun appmanager commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy local projects or Git repositories to Alibaba Cloud ECS, configure aliyun and appmanager prerequisites, generate deployment scripts, confirm costs, and verify deployments. <br>

### Deployment Geography for Use: <br>
Alibaba Cloud regions listed by the skill: cn-shanghai, cn-hangzhou, cn-beijing, cn-shenzhen, cn-guangzhou, cn-chengdu, cn-nanjing, and cn-hongkong. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad Alibaba Cloud deployment authority that can create, modify, or delete ECS and related resources. <br>
Mitigation: Use OAuth, temporary credentials, or an ECS RAM role where possible, and scope the RAM policy to the needed regions and resources before deployment. <br>
Risk: Sensitive cloud credentials or model API keys may be mishandled during setup. <br>
Mitigation: Configure credentials out of band through aliyun's default credential chain or environment configuration, and do not paste API keys or access keys into chat, command arguments, logs, or config files. <br>
Risk: Deployment can incur recurring ECS and OSS charges or affect an existing ECS instance. <br>
Mitigation: Review the price output, OSS billing reminder, and existing-ECS warning before deploy; keep the delete command available for cleanup. <br>
Risk: CLI installation or PATH changes can alter the local execution environment. <br>
Mitigation: Confirm upgrades for existing aliyun installations, verify the effective aliyun binary on PATH, and prefer a clean project directory or isolated clone path. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sdk-team/alibabacloud-ecs-code-deploy) <br>
- [Deploy Output & Management Reference](references/deploy-output-and-management.md) <br>
- [Init & Credentials Reference](references/init-and-credentials.md) <br>
- [RAM Policies Reference](references/ram-policies.md) <br>
- [Script Templates & Language Reference](references/script-templates.md) <br>
- [Step 0: Resolve $SKILL_DIR](references/skill-dir-resolution.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated deployment script/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cost reminders, console links, status/delete commands, and deployment verification summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
