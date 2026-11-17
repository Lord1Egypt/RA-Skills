## Description:

快速搭建临时文件下载服务器，支持 HTTP 下载、下载页面生成和防火墙端口开放，适用于需要向用户发送文件但聊天工具不支持直接文件传输的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtafersit1-png](https://clawhub.ai/user/mtafersit1-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create a temporary HTTP download endpoint for selected files or directories and share a browser-accessible link with external users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose files through a temporary unauthenticated public HTTP server.

Mitigation: Use it only on a tightly controlled directory containing non-sensitive files and stop the server promptly after the transfer is complete.

Risk: The skill can open firewall ports and bind the server broadly.

Mitigation: Prefer binding to 127.0.0.1 unless public access is explicitly needed, avoid automatic firewall opening when possible, and remove firewall rules after use.

Risk: Generated pages may include filenames, titles, or descriptions from local inputs.

Mitigation: Do not use generated pages with untrusted filenames or descriptions.

## Reference(s):

- [Quickstart Guide](references/QUICKSTART.md)
- [Python http.server documentation](https://docs.python.org/3/library/http.server.html)
- [iptables project](https://netfilter.org/projects/iptables/)
- [ClawHub skill page](https://clawhub.ai/mtafersit1-png/skills/file-download-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate an index.html download page and commands for running a temporary HTTP server.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
