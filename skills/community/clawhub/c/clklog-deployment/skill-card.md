## Description:

帮助用户在本地环境中快速部署 ClkLog 开源用户行为分析系统，选择 Docker Compose 或源码部署路径，并完成环境检查、配置引导、故障排查和协议提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaingush](https://clawhub.ai/user/gaingush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to plan and execute a private ClkLog deployment on Linux, choosing between a quick Docker Compose setup and a source-based deployment for customization. The skill also guides users through environment checks, official documentation links, deployment validation, and common troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClkLog deployments collect user behavior data and may involve privacy, retention, access-control, and legal requirements.

Mitigation: Review ClkLog privacy, retention, access-control, and legal requirements before deployment, and configure the service according to the organization's data-governance policies.

Risk: Deployment setup can expose .env values, database passwords, or service credentials if copied into logs, chat, or shared files.

Mitigation: Treat .env and database credentials as sensitive, avoid pasting secrets into agent conversations, and rotate credentials if exposure is suspected.

Risk: ClkLog product documentation and artifact metadata describe AGPL-3.0 and commercial-license obligations that may affect closed-source or commercial integrations.

Mitigation: Confirm the applicable ClkLog license terms and purchase commercial authorization when closed-source commercial integration requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaingush/skills/clklog-deployment)
- [ClkLog official site](https://clklog.com)
- [ClkLog documentation center](https://clklog.com/resource/docscenter.html)
- [ClkLog Docker install guide](https://clklog.com/install/docker/intro.html)
- [ClkLog Docker FAQ](https://clklog.com/install/docker/fqa.html)
- [ClkLog source deployment guide](https://clklog.com/install/source/deployment.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, checklists, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes official documentation references and deployment-path selection prompts.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
