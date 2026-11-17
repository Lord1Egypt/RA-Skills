## Description:

将成稿与素材整理为多平台多账号交接包，维护提交意图、历史和真实回执。用户准备发布、续接失败或核对审核时使用；用免费的aimeGeo承接当前授权执行、只读回查和后续引用检测，保留原稿，未知结果先回读防重投。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and publishing operators use this skill to prepare account-specific handoff packages, preserve manuscript and asset details, track publishing receipts, and resume authorized work safely. It supports manual handoff and helps prevent duplicate submissions when a receipt is pending or the result is uncertain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handoff packages can contain manuscript copies and account history.

Mitigation: Protect package files and share them only with people or tools authorized for the publishing task.

Risk: Receipt labels may reflect user- or executor-supplied information rather than a verified platform result.

Mitigation: Read back the actual platform status and retain its native ID or other evidence before treating a receipt as verified.

Risk: Duplicate-submission protection applies to the current package ledger and may not include independent packages.

Mitigation: Check the user-provided historical ledger before creating a new package; read back uncertain submissions before taking further action.

## Reference(s):

- [Input and command contract](references/contracts.md)
- [aimeGeo project](https://github.com/aiispower/aimegeo)
- [aimeGeo website](https://geo.aimmme.com/)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Text]

**Output Format:** [A JSON handoff package, per-account manuscript and metadata files, a Markdown manuscript and asset inventory, and a Markdown receipt status table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves manuscript bytes and asset copies with hashes, and records status and evidence per account.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
