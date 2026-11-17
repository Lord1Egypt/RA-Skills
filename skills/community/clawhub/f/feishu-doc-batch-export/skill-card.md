## Description:

Exports accessible Feishu docx documents to local Markdown with supported formatting, links, and downloaded images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[technologyliu](https://clawhub.ai/user/technologyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and knowledge workers use this skill to configure Feishu app credentials and export accessible Feishu docx content into local Markdown archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes batch and folder export behavior that the shipped script does not fully implement.

Mitigation: Confirm the requested export mode before use and rely on single-document export unless folder support is added and reviewed.

Risk: Feishu credentials and Drive permissions may expose more workspace data than needed for single-document export.

Mitigation: Use narrowly scoped Feishu credentials and avoid granting drive:readonly until folder export is actually required.

Risk: Document-supplied image links can cause the machine running the skill to contact arbitrary HTTP(S) URLs and write downloaded files locally.

Mitigation: Export only trusted documents and choose an output directory appropriate for sensitive local copies.

## Reference(s):

- [Feishu app configuration guide](artifact/references/config.md)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; exported documents are written as Markdown files with local image assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET, Feishu document access, and a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
