## Description: <br>
Guides users to manage Alibaba Cloud resources with the Aliyun CLI, including installation, credential configuration, plugin management, command construction, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to install, configure, and run Aliyun CLI commands for Alibaba Cloud services. It helps with credentials, product plugins, parameter syntax, output filtering, pagination, waiters, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials or tokens may be exposed or over-privileged when configuring Aliyun CLI access. <br>
Mitigation: Prefer OAuth, STS, RAM roles, or least-privilege RAM users, avoid root credentials, rotate access keys, and keep credentials out of repositories and shared logs. <br>
Risk: Installer or plugin update commands download executable CLI components. <br>
Mitigation: Install only when Alibaba Cloud CLI access is intended, verify downloads where possible, and keep the CLI and product plugins updated from trusted Alibaba Cloud sources. <br>
Risk: Debug output can reveal request details, resource identifiers, or sensitive configuration. <br>
Mitigation: Use debug logging only for troubleshooting and redact secrets, account identifiers, and resource details before sharing logs. <br>
Risk: Using insecure transport options can weaken request security. <br>
Mitigation: Avoid `--insecure` for real workloads and use secure defaults unless a controlled diagnostic case requires otherwise. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/sdk-team/alibabacloud-cli-guidance) <br>
- [Publisher Profile](https://clawhub.ai/user/sdk-team) <br>
- [Aliyun CLI Installation & Configuration Guide](artifact/references/installation-guide.md) <br>
- [Command Syntax Guide](artifact/references/command-syntax.md) <br>
- [Global Flags Reference](artifact/references/global-flags.md) <br>
- [RAM Policies and the Aliyun CLI](artifact/references/ram-policies.md) <br>
- [Configure OAuth Authentication for Alibaba Cloud CLI](https://www.alibabacloud.com/help/en/doc-detail/2995960.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Aliyun CLI commands, credential setup steps, plugin guidance, RAM permission notes, and troubleshooting advice.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
