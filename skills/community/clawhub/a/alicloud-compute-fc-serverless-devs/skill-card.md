## Description:

Alibaba Cloud Function Compute (FC 3.0) skill for installing and using Serverless Devs to create, deploy, invoke, and remove a Python function.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to set up Alibaba Cloud Function Compute with Serverless Devs, configure credentials, initialize a Python function project, deploy it, invoke it, and remove it when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may be exposed through command history, logs, or exported configuration.

Mitigation: Use least-privilege or short-lived Alibaba Cloud credentials, avoid placing secrets directly in commands or exported JSON, and prefer environment or credential flows that reduce logging exposure.

Risk: Serverless Devs commands such as deploy and remove can mutate or delete cloud resources.

Mitigation: Confirm account, region, operation intent, and target resource identifiers before running mutating commands, and start with a minimal read-only connectivity check.

Risk: Running the CLI with sudo can broaden local impact unnecessarily.

Mitigation: Prefer pinned, user-scoped Serverless Devs execution such as npx or a non-root install path instead of sudo.

## Reference(s):

- [install_serverless_devs_and_docker.md](references/install_serverless_devs_and_docker.md)
- [sources.md](references/sources.md)
- [Install Serverless Devs and Docker](https://help.aliyun.com/zh/functioncompute/fc/developer-reference/install-serverless-devs-and-docker)
- [Function Compute HTTP triggers overview](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/http-triggers-overview)
- [Function Compute 3.0 HTTP triggers overview](https://www.alibabacloud.com/help/en/functioncompute/fc-3-0/user-guide/http-triggers-overview)
- [Configure custom domain names](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud operation guidance that should be bounded by explicit account, region, and target resource parameters.]

## Skill Version(s):

1.0.3 (source: server release evidence; skill frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
