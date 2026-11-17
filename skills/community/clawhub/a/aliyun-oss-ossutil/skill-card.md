## Description:

Use when installing, configuring, or operating Alibaba Cloud OSS from the command line with ossutil 2.0, based on the official ossutil overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to install and configure ossutil 2.0, verify Alibaba Cloud OSS connectivity, and run bounded upload, download, sync, listing, and management workflows with explicit region and endpoint handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing ossutil from a downloaded archive may introduce supply-chain or privileged-install risk.

Mitigation: Verify the download against official Alibaba Cloud guidance and prefer a user-owned install path when possible.

Risk: Alibaba Cloud AccessKey credentials can be exposed through command history, logs, or saved evidence.

Mitigation: Use least-privilege RAM credentials, prefer environment variables or shared credential files, and avoid saving secrets in evidence files.

Risk: OSS operations such as sync with --delete, ACL changes, or broad listings can be destructive or expose sensitive object metadata.

Mitigation: Confirm intent, bucket, object prefix, region, endpoint, and operation scope before mutating commands; run a minimal read-only check first.

## Reference(s):

- [ossutil 2.0 install guide](references/install.md)
- [Official source list](references/sources.md)
- [Alibaba Cloud ossutil overview](https://help.aliyun.com/zh/oss/developer-reference/ossutil-overview)
- [ossutil 2.2.1 Linux download](https://gosspublic.alicdn.com/ossutil/v2/2.2.1/ossutil-2.2.1-linux-amd64.zip)
- [ossutil 2.2.1 macOS download](https://gosspublic.alicdn.com/ossutil/v2/2.2.1/ossutil-2.2.1-darwin-amd64.zip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OSS command output, object listings, sync logs, and validation evidence files when the agent executes the recommended workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
