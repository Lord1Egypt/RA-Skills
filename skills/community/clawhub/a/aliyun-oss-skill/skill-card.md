## Description:

aliyun-oss helps agents manage Alibaba Cloud Object Storage (OSS) objects, including upload, download, listing, deletion, metadata inspection, moves, copies, and signed URL generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[langhuachuanshi](https://clawhub.ai/user/langhuachuanshi)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let an agent manage files in Alibaba Cloud OSS buckets through the ali-oss Node.js SDK, with ossutil described as a fallback path. It supports common storage workflows such as backup upload, object discovery, signed URL creation, and object cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can persist Alibaba Cloud access keys in shell startup files.

Mitigation: Use narrowly scoped RAM or STS credentials, avoid entering secrets in reusable shell history, remove generated exports from shell startup files, and rotate any credentials already exposed this way.

Risk: Delete operations may proceed even when the documented interactive confirmation is expected.

Mitigation: Review delete commands before execution, avoid relying on the prompt as a safeguard, and require a fixed confirmation implementation before using destructive operations in routine workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/langhuachuanshi/skills/aliyun-oss-skill)
- [Aliyun OSS Node.js SDK documentation](https://help.aliyun.com/document_detail/32068.html)
- [Aliyun ossutil documentation](https://help.aliyun.com/document_detail/120075.html)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the ali-oss package; operates on user-provided Alibaba Cloud OSS credentials and bucket configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata, released 2026-03-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
