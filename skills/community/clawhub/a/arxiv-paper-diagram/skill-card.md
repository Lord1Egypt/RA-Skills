## Description: <br>
解读 arXiv 论文并生成结构图，将论文翻译为中文解读，同时生成模型架构图、流程图、数据流程图等可视化图表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taoj2025](https://clawhub.ai/user/taoj2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to turn an arXiv URL or ID into a Chinese paper interpretation and a companion visual diagram for the paper's method, architecture, workflow, or data flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External retrieval may send arXiv IDs, paper titles, or related search queries to external services. <br>
Mitigation: Use public papers or material approved for external lookup; avoid private or embargoed research unless those lookups are acceptable. <br>
Risk: Generated HTML diagrams may be inappropriate to share or open in sensitive contexts without inspection. <br>
Mitigation: Review generated HTML before sharing or opening it in sensitive environments. <br>
Risk: Generated translations and diagrams can misstate or oversimplify paper details. <br>
Mitigation: Review the Chinese interpretation and diagram against the original paper before citing, publishing, or using them for decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/taoj2025/arxiv-paper-diagram) <br>
- [Archify renderer guide](artifact/references/archify-guide.md) <br>
- [arXiv retrieval guide](artifact/references/arxiv-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, code, shell commands, guidance] <br>
**Output Format:** [Structured Chinese Markdown plus interactive HTML diagram files; may include JSON inputs and shell commands for diagram rendering.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML diagrams can be opened in a browser and exported to PNG, JPEG, WebP, or SVG when the renderer supports it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
