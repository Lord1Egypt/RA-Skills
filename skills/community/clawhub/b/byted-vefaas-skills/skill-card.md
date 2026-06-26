## Description: <br>
Deploy and manage serverless applications on Volcengine veFaaS. Use when the user wants to deploy web apps, manage functions, configure environment variables, or work with veFaaS services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate the vefaas CLI for deploying web applications, managing functions, configuring environment variables, and troubleshooting Volcengine veFaaS services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run commands that create, update, deploy, or redeploy live Volcengine veFaaS cloud resources. <br>
Mitigation: Review target account, region, application, function, gateway, and environment before execution; remove automatic confirmation from copied deploy commands unless automation is intentional. <br>
Risk: The skill covers authentication and environment variable workflows that can involve cloud credentials, API keys, and secrets. <br>
Mitigation: Use least-privilege or short-lived credentials, avoid passing secrets directly on command lines, protect local credential files, and redact environment values and debug logs before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-vefaas-skills) <br>
- [vefaas CLI package](https://vefaas-cli.tos-cn-beijing.volces.com/volcengine-vefaas-latest.tgz) <br>
- [Volcengine Console](https://console.volcengine.com) <br>
- [API Gateway console](https://console.volcengine.com/veapig) <br>
- [Authentication Reference](artifact/references/authentication.md) <br>
- [Configuration Reference](artifact/references/configuration.md) <br>
- [Environment Variables Reference](artifact/references/environment-variables.md) <br>
- [Framework Detection Reference](artifact/references/framework-detection.md) <br>
- [Troubleshooting Reference](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that affect live cloud resources and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
