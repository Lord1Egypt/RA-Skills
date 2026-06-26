## Description: <br>
Alibaba Cloud Function Compute (FC 3.0) skill for installing and using Serverless Devs to create, deploy, invoke, and remove a Python function. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for Alibaba Cloud Function Compute setup, credential configuration, Python starter deployment, invocation, cleanup, and custom-domain guidance with Serverless Devs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials may be exposed or over-privileged during Serverless Devs configuration. <br>
Mitigation: Use temporary or least-privilege Alibaba Cloud credentials and avoid placing secrets directly in command history or logs. <br>
Risk: Deploy, custom-domain, and remove commands can mutate or delete Alibaba Cloud Function Compute resources. <br>
Mitigation: Require explicit user confirmation, region/resource identifiers, and bounded scope before running mutating commands. <br>
Risk: Global installation with sudo increases local system impact. <br>
Mitigation: Prefer the no-sudo npx path where possible and verify the Serverless Devs package before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-compute-fc-serverless-devs) <br>
- [Install Serverless Devs and Docker](https://help.aliyun.com/zh/functioncompute/fc/developer-reference/install-serverless-devs-and-docker) <br>
- [HTTP triggers overview](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/http-triggers-overview) <br>
- [HTTP triggers overview for FC 3.0](https://www.alibabacloud.com/help/en/functioncompute/fc-3-0/user-guide/http-triggers-overview) <br>
- [Configure custom domain names](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names) <br>
- [Artifact source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include credential configuration steps, deploy/invoke/remove commands, custom-domain configuration, and evidence file guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
