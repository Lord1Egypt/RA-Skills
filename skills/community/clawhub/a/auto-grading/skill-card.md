## Description: <br>
智能批改作业 helps agents review graduation design and thesis archives by extracting doc, docx, pdf, and pptx content, scoring submissions, checking cross-document consistency, reviewing defense slides, and validating findings with source evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingsunzhang2026-oss](https://clawhub.ai/user/kingsunzhang2026-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, advisors, and review assistants use this skill to audit graduation design or thesis archives, generate document scores, cross-check consistency across submitted files, review PPT defense materials, and produce evidence-linked revision reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill extracts student document text and path metadata locally, which can include student names, IDs, thesis content, or private project details. <br>
Mitigation: Use it only on the intended archive or folder, avoid broad directories, and delete generated text files and manifests after review when they contain sensitive student or project data. <br>
Risk: Grading findings can be misleading if extracted text is incomplete, from the wrong document version, or not backed by source evidence. <br>
Mitigation: Review evidence-linked findings and run the bundled validation harness before relying on the final Markdown report. <br>


## Reference(s): <br>
- [GB/T 7714-2015 Reference Format Quick Guide](references/gbt7714.md) <br>
- [Thesis and Graduation Design Review Template](references/review_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON issue data and Markdown review reports, with inline shell commands for document extraction and validation when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should include the source file, evidence text, and confidence; extracted text files and manifests may be written under /tmp/auto_grading.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
