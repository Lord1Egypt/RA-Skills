## Description:

在中国大陆服务器通过代理访问币安API的完整配置指南。涵盖代理选型、mihomo安装配置、vmess连接、币安域名路由、API签名调用。当用户在中国大陆需要调用币安API、配置币安代理、解决币安API连接问题（Connection reset、HTTP 451区域限制、DNS污染）时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[eastnomoring](https://clawhub.ai/user/eastnomoring)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a mainland China server to reach Binance APIs through a non-US proxy path, including mihomo routing, vmess proxy settings, Binance API signing examples, and troubleshooting for common connectivity failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to install an unverified proxy binary and run it persistently with high privileges.

Mitigation: Download mihomo from an official source, verify a pinned checksum or signature, test before enabling boot persistence, and run the service as a dedicated unprivileged user with systemd hardening.

Risk: The workflow handles financial API credentials through proxy infrastructure.

Mitigation: Use read-only or IP-restricted Binance API keys, avoid sharing secrets in shell history or logs, and route traffic only through proxy infrastructure the operator controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eastnomoring/skills/binance-proxy-cn)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, YAML, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes proxy setup guidance, configuration snippets, API call examples, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
