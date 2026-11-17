## Description:

Alibaba Cloud OSS CLI (ossutil 2.0) skill. Install, configure, and operate OSS from the command line based on the official ossutil overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to install, configure, and run Alibaba Cloud OSS ossutil 2.0 workflows for bucket listing, object transfer, synchronization, and OSS resource management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes cloud-storage operations, including examples that can delete destination objects during synchronization.

Mitigation: Require explicit confirmation before sync operations with --delete or API-level bucket management commands, and run a minimal read-only query first.

Risk: The install flow downloads and installs ossutil with privileged commands.

Mitigation: Review install commands before running them, prefer a user-local install path, and verify ossutil from an official checksum or signature source when available.

Risk: Broad Alibaba Cloud credentials could allow unintended bucket access or mutation.

Mitigation: Use least-privilege RAM credentials scoped to the exact buckets and actions needed, and avoid passing secrets on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-storage-oss-ossutil)
- [ossutil 2.0 install notes](references/install.md)
- [Official source list](references/sources.md)
- [Alibaba Cloud OSS ossutil overview](https://help.aliyun.com/zh/oss/developer-reference/ossutil-overview)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to save command outputs, object listings, and sync logs as evidence files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
