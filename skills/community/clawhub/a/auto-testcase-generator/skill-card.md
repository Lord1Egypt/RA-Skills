## Description: <br>
Automated test case generation from project documents, including requirements analysis, visual flow interpretation, coverage design, Excel test case output, and validation reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thanksjj](https://clawhub.ai/user/thanksjj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to convert requirements documents, API specifications, and project documentation into scoped analysis, structured Excel test cases, and traceability validation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release suspicious because one helper workflow can launch nested Codex with broad filesystem and command authority. <br>
Mitigation: Install only when the maintainer workflow is trusted; prefer non-yolo review modes in untrusted repositories and inspect moderation or PR-publishing commands before execution. <br>
Risk: The artifact includes a PDF image extraction script that writes files to a local output directory. <br>
Mitigation: Run extraction only on trusted documents and choose an explicit output directory that can be reviewed before generated images are used in test design. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thanksjj/auto-testcase-generator) <br>
- [Analysis Template](references/analysis_template.md) <br>
- [Excel Output Format](references/excel_format.md) <br>
- [Image Processing Guidance](references/image_processing.md) <br>
- [PDF Image Extraction Script](scripts/extract_pdf_images.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown, Mermaid diagrams, Excel-compatible test case files, and inline shell or Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes staged checklists, context handoff cards, requirement analysis briefs, coverage matrices, and validation summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
