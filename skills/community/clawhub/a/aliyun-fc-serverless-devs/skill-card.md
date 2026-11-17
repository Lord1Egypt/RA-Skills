## Description:

Use when users need CLI-based FC quick start or Serverless Devs setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to install and validate Serverless Devs, configure Alibaba Cloud credentials, and run a bounded Alibaba Cloud Function Compute deploy, invoke, and cleanup flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unnecessary sudo use in Serverless Devs operations.

Mitigation: Review commands before execution and avoid sudo unless the local environment explicitly requires elevated package installation.

Risk: The security summary flags unpinned remote CLI execution.

Mitigation: Pin or vet the Serverless Devs CLI version before installing or running it in sensitive environments.

Risk: The security summary flags risky credential handling for cloud operations.

Mitigation: Use least-privilege, short-lived Alibaba Cloud credentials where possible, avoid exposing secrets in command lines or logs, and require explicit confirmation before deploy or remove actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-fc-serverless-devs)
- [Install Serverless Devs and Docker](references/install_serverless_devs_and_docker.md)
- [Official source list](references/sources.md)
- [Alibaba Cloud Serverless Devs installation guide](https://help.aliyun.com/zh/functioncompute/fc/developer-reference/install-serverless-devs-and-docker)
- [Alibaba Cloud Function Compute HTTP triggers overview](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/http-triggers-overview)
- [Alibaba Cloud Function Compute FC 3.0 HTTP triggers overview](https://www.alibabacloud.com/help/en/functioncompute/fc-3-0/user-guide/http-triggers-overview)
- [Configure custom domain names](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential-handling, region-selection, deployment, invocation, cleanup, and validation guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
