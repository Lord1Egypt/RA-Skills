## Description:

A hands-on compliance playbook and local toolkit for AI-generated content labeling across China's labeling measures and EU AI Act Article 50, covering content-type labeling practices, metadata, watermarking, platform duties, app review, and remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Content operations, product, compliance, and legal teams use this skill to decide whether AI-generated content needs labeling and to produce practical checklists, metadata templates, China/EU comparisons, and remediation steps. Users should verify regulatory guidance against current official sources before relying on it for legal decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regulatory guidance can become outdated or may not fit a user's exact legal situation.

Mitigation: Check current official sources and qualified legal or compliance counsel before relying on the guidance for operational decisions.

Risk: Manual execution of verification scripts can overwrite files under artifact/verify.

Mitigation: Run verification in a clean working copy and review generated verification outputs before keeping or publishing them.

## Reference(s):

- [01 标识义务与范围](artifact/references/01-标识义务与范围.md)
- [02 中国标识要求](artifact/references/02-中国标识要求.md)
- [03 欧盟透明度要求](artifact/references/03-欧盟透明度要求.md)
- [04 各类内容标识做法](artifact/references/04-各类内容标识做法.md)
- [05 隐式标识技术方案](artifact/references/05-隐式标识技术方案.md)
- [06 平台与上架义务](artifact/references/06-平台与上架义务.md)
- [07 合规整改与 FAQ](artifact/references/07-合规整改与FAQ.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON metadata templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional local Python commands print checklists, comparisons, audits, and metadata templates to standard output.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
