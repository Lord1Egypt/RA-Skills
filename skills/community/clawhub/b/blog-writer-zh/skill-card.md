## Description: <br>
用中文撰写科技/行业思辨类文章，风格理性犀利、结构清晰，适用于个人思考、科技评论、行业分析、公众号、知乎、小红书长文以及润色、扩写、改写现有内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xavier-ljf](https://clawhub.ai/user/xavier-ljf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, creators, and teams use this skill to plan, draft, revise, review, and export Chinese long-form technology or industry-analysis essays. It supports Markdown article drafting, critical reader review, optional style calibration from local reference articles, optional web-backed evidence gathering, and platform-oriented export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read style samples from a user-configured reference directory. <br>
Mitigation: Use a dedicated reference directory that contains only non-sensitive writing samples and confirm the exact path before style calibration. <br>
Risk: The workflow can create export files, archive final drafts, and clean generated export files. <br>
Mitigation: Ask the agent to confirm target paths before exporting, deleting generated export files, or archiving final articles. <br>
Risk: Web-supported evidence gathering may introduce weak, outdated, or misread sources into a draft. <br>
Mitigation: Review cited sources and claims before publishing, especially for time-sensitive technology or industry analysis. <br>


## Reference(s): <br>
- [Writing Style Guide](references/style-guide.md) <br>
- [Article Structure Templates](references/templates.md) <br>
- [Pandoc](https://pandoc.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown drafts, revision guidance, optional platform-compatible Markdown exports, and optional DOCX exports when Pandoc is available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes UTF-8 Markdown drafts locally, can read user-selected style-reference Markdown files, and may export derived .md or .docx files for publishing workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
