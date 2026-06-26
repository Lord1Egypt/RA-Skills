## Description: <br>
Analyze construction drawings to extract dimensions, annotations, symbols, and metadata. Support quantity takeoff and design review automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction professionals, developers, and project teams use this skill to analyze user-provided construction drawings, extract drawing data, generate summaries, and support quantity takeoff or design review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests filesystem access and may process confidential construction plans. <br>
Mitigation: Provide only the files intended for analysis and avoid exposing unrelated project directories. <br>
Risk: Generated summaries or exports may contain sensitive project data or extraction errors. <br>
Mitigation: Review generated reports and exported data before sharing or using them for project decisions. <br>
Risk: The workflow depends on the Python pdfplumber package for PDF analysis. <br>
Mitigation: Install pdfplumber from the user's normal trusted Python package source. <br>


## Reference(s): <br>
- [Drawing Analyzer ClawHub listing](https://clawhub.ai/datadrivenconstruction/drawing-analyzer) <br>
- [DataDrivenConstruction homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with structured tables, summaries, findings, and optional code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include export-oriented guidance for Excel, CSV, or JSON when relevant.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
