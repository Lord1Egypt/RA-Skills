## Description:

BOC部署工具帮助工程师初始化部署机并部署博云 BOC 容器平台，覆盖环境检查、部署包校验、配置生成、部署监控和结果验证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongruiji](https://clawhub.ai/user/hongruiji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to initialize deployment machines and guide BOC container platform deployment across CI, Kubernetes, storage, registry, and portal components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks for root SSH credentials for deployment hosts.

Mitigation: Use SSH keys or a secret manager, limit credential scope, and avoid storing plaintext passwords in prompts, files, logs, or generated configuration.

Risk: Deployment archive handling includes destructive cleanup and extraction commands.

Mitigation: Canonicalize, quote, and confirm paths before running rm -rf or tar commands, and execute them only in the intended deployment package directory.

Risk: A compromised or incorrect deployment archive could alter infrastructure during initialization or platform deployment.

Mitigation: Verify deployment archives against a trusted checksum or signature before extraction and execution.

Risk: The troubleshooting guidance references an external sshpass download path.

Mitigation: Prefer managed package sources, SSH keys, or approved internal tooling instead of unverified credential automation downloads.

Risk: Generated shell commands can modify production infrastructure and long-running deployment state.

Mitigation: Review commands before execution, run in a controlled maintenance window, monitor logs, and verify Kubernetes nodes and Pods before opening the portal to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongruiji/skills/boc-deploy-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment status summaries, log excerpts, Kubernetes node and Pod verification results, and portal access details.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
