## Description:

天翼云 CLI 工具指南，帮助代理使用 ctyun-cli 安装、配置和管理天翼云资源，覆盖 ECS、VPC、EBS、ELB、CCE、Redis、MySQL、Kafka、监控、IAM 等 32+ 个服务模块、943+ 个 API 和 898+ 个命令。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengyucn](https://clawhub.ai/user/fengyucn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to generate ctyun-cli installation, authentication, query, and cloud-resource management guidance for CTYUN environments. It is intended for managing live cloud resources and should be used with reviewed credentials and explicit confirmation for production-impacting commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of powerful CTYUN credentials and commands against live cloud infrastructure.

Mitigation: Use an isolated environment, pin and verify the ctyun-cli package or source commit, use least-privilege credentials, and require explicit confirmation before kubeconfig retrieval, deletion, or production-impacting operations.

Risk: Long-lived CTYUN secrets may be exposed through shell startup files or command history.

Mitigation: Avoid storing long-lived secrets in shell profiles or history, rotate any exposed credentials, and prefer short-lived or tightly scoped credentials when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengyucn/skills/ctyun)
- [PyPI package: ctyun-cli](https://pypi.org/project/ctyun-cli/)
- [Homepage listed in artifact](https://github.com/fengyucn/ctyun-cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples may target live CTYUN resources and can emit table, JSON, or YAML CLI output.]

## Skill Version(s):

1.30.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
