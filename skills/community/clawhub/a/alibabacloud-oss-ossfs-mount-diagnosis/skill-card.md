## Description:

Read-only diagnostics for Alibaba Cloud OSS ossfs and container mount issues, including mount failures, disappeared mountpoints, storage-volume 403 errors, and archive-object read 403 errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose Alibaba Cloud OSS mount failures, endpoint or region mismatches, RAM permission gaps, FUSE dependency issues, container storage-volume 403 errors, and archive direct-read constraints without making changes to cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls Alibaba Cloud OSS and STS read-only APIs and may expose account, principal, or visible bucket metadata in diagnostic reports.

Mitigation: Install and run it with a narrowly scoped temporary Alibaba Cloud role where possible, and review reports before sharing them outside the operating team.

Risk: The security evidence flags an unpinned host CLI upgrade command as requiring review.

Mitigation: Verify the Alibaba Cloud CLI source and target version separately before following upgrade guidance.

Risk: Privileged-container and metadata-endpoint checks can affect sensitive host or cloud-runtime contexts if followed casually.

Mitigation: Treat those steps as manual last-resort diagnostics and require operator review before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-ossfs-mount-diagnosis)
- [ossfs mount failure attribution knowledge](references/ossfs-mount-knowledge.md)
- [Container storage-volume mount 403 attribution](references/container-volume-403.md)
- [Archive direct-read judgment](references/archive-direct-read.md)
- [Minimal read-only RAM policy](references/ram-policies.md)
- [Alibaba Cloud ossfs quick start](https://help.aliyun.com/zh/oss/user-guide/ossfs-quick-start)
- [Alibaba Cloud ossfs FAQ](https://help.aliyun.com/zh/oss/developer-reference/ossfs-faq)
- [Alibaba Cloud ACK OSS volume overview](https://help.aliyun.com/zh/ack/ack-managed-and-ack-dedicated/user-guide/oss-volume-overview/)
- [Alibaba Cloud archive direct reading](https://help.aliyun.com/zh/oss/user-guide/archive-direct-reading)
- [Alibaba Cloud RAM policy documentation](https://help.aliyun.com/zh/oss/user-guide/ram-policy/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with diagnostic findings, manual guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should distinguish read-only evidence from manual remediation and note degraded checks when cloud evidence is unavailable.]

## Skill Version(s):

0.0.1 (source: references/manifest.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
