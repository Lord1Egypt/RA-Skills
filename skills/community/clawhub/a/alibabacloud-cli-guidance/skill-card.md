## Description:

Guide users to manage Alibaba Cloud resources using the Aliyun CLI command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to install and configure Aliyun CLI, construct Alibaba Cloud service commands, manage plugins, handle credentials, and troubleshoot common CLI errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands may download and execute unverified scripts or binaries.

Mitigation: Review setup commands before running them, prefer package managers or pinned checksum-verified downloads, and avoid running curl-to-bash in shells that already contain cloud credentials.

Risk: Automatic plugin installation or bulk plugin updates can change local CLI behavior unexpectedly.

Mitigation: Approve exact plugin installation and update actions before an agent runs them.

Risk: Cloud credentials and RAM permissions can grant broad access if handled carelessly.

Mitigation: Use OAuth, RAM roles, or short-lived STS credentials where possible, and keep RAM permissions least-privilege.

Risk: Debug output can expose sensitive request, credential, or environment details.

Mitigation: Redact debug logs before sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-cli-guidance)
- [Command Syntax Guide](references/command-syntax.md)
- [Global Flags Reference](references/global-flags.md)
- [Aliyun CLI Installation and Configuration Guide](references/installation-guide.md)
- [RAM Policies and the Aliyun CLI](references/ram-policies.md)
- [Configure OAuth Authentication for Alibaba Cloud CLI](https://www.alibabacloud.com/help/en/doc-detail/2995960.html)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud CLI commands that require user review before execution.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
