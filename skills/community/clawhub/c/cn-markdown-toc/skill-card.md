## Description:

自动扫描 Markdown 标题并生成带 GitHub 风格锚点的多级目录，支持层级控制和插入文件顶部。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content creators use this skill to generate or insert a navigable table of contents for Markdown documents before publishing or importing them into documentation systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --insert option rewrites the selected Markdown file by adding or replacing a TOC block.

Mitigation: Review the target file and keep version control or a backup before running --insert.

Risk: The artifact mentions an unrelated AISoBrand link that is not required for the Markdown TOC workflow.

Mitigation: Use only the local Markdown TOC functionality unless the external service is separately reviewed and needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-markdown-toc)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown table-of-contents block with GitHub-style anchor links; optional in-place Markdown file update.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Python standard library; --insert rewrites the chosen Markdown file by adding or replacing a TOC block.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
