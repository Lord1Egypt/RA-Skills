## Description:

Deploy and manage serverless applications on Volcengine veFaaS. Use when the user wants to deploy web apps, manage functions (pull code, upload and deploy), configure environment variables, or work with veFaaS services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy web applications, manage veFaaS functions, configure environment variables, authenticate the veFaaS CLI, and troubleshoot Volcengine serverless deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation and use of a powerful cloud CLI that changes live Volcengine resources.

Mitigation: Review proposed commands before execution and confirm the target app, region, gateway, and expected impact before using non-interactive deployment flags.

Risk: Authentication examples include access keys, secret keys, tokens, and environment variables that can expose credentials if handled carelessly.

Mitigation: Prefer SSO or protected CI secrets, avoid pasting credentials into shared prompts or shell history, and redact credentials from command output and logs.

Risk: Debug logs may contain API request or response data related to deployments and authentication failures.

Mitigation: Inspect and redact debug logs before sharing them outside the trusted deployment team.

Risk: The global CLI install command downloads a package from a remote tarball URL.

Mitigation: Pin or verify the CLI package source before global installation, especially in production or CI environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-vefaas-skills)
- [Volcengine Console](https://console.volcengine.com)
- [API Gateway Console](https://console.volcengine.com/veapig)
- [Authentication Reference](references/authentication.md)
- [Configuration Reference](references/configuration.md)
- [Environment Variables Reference](references/environment-variables.md)
- [Framework Detection Reference](references/framework-detection.md)
- [Troubleshooting Reference](references/troubleshooting.md)
- [Template Quickstart](cookbooks/template-quickstart.md)
- [Deploy Existing Code](cookbooks/deploy-existing-code.md)
- [Manage Functions](cookbooks/manage-functions.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install a cloud CLI, authenticate with Volcengine, deploy applications, update function configuration, set environment variables, and inspect logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
