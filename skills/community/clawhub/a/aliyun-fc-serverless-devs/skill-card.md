## Description: <br>
Use when users need CLI-based FC quick start or Serverless Devs setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to follow an Alibaba Cloud Function Compute quick start with Serverless Devs, including credential setup, Python project initialization, deploy, invoke, cleanup, and custom domain guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential setup uses Alibaba Cloud access keys and account identifiers. <br>
Mitigation: Use least-privilege or temporary credentials, prefer guided credential entry where possible, and keep secrets out of logs and shared files. <br>
Risk: Deploy and remove commands can change or delete Alibaba Cloud Function Compute resources. <br>
Mitigation: Verify the account, region, project, resource names, and operation scope before mutating commands; run a minimal read-only check first when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-fc-serverless-devs) <br>
- [Install Serverless Devs and Docker](https://help.aliyun.com/zh/functioncompute/fc/developer-reference/install-serverless-devs-and-docker) <br>
- [HTTP Triggers Overview](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/http-triggers-overview) <br>
- [Configure Custom Domain Names](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names) <br>
- [Artifact source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include command summaries and evidence files under output/aliyun-fc-serverless-devs/ when the workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
