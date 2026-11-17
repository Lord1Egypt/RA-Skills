## Description:

解读arXiv论文并生成结构图，将论文翻译为中文的同时，生成论文对应的模型架构图、流程图、数据流程图等可视化图表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[taoj2025](https://clawhub.ai/user/taoj2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to provide an arXiv URL or ID, retrieve paper content, translate and explain the paper in Chinese, and produce an accompanying paper structure diagram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow makes outbound requests to arXiv, Crossref, paper pages, and search services.

Mitigation: Install only where outbound paper retrieval is acceptable, prefer HTTPS endpoints when available, and review external content before using it as source material.

Risk: Fetched paper content and generated HTML diagrams may contain incorrect, incomplete, or untrusted material.

Mitigation: Review generated Markdown and HTML before sharing or relying on them, especially for academic claims, citations, formulas, and rendered diagram content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taoj2025/skills/arxiv-paper-diagram)
- [Archify renderer guide](artifact/references/archify-guide.md)
- [arXiv paper translation guide](artifact/references/arxiv-guide.md)
- [Crossref arXiv DOI API pattern](https://api.crossref.org/works/https://doi.org/10.48550/arXiv.XXXXXXX)
- [arXiv API query pattern](http://export.arxiv.org/api/query?id_list=XXXXXXX)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance]

**Output Format:** [Structured Chinese Markdown plus generated HTML diagram files and supporting JSON/command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams may be interactive HTML with export options for PNG, JPEG, WebP, or SVG.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
