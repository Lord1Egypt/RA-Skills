## Description: <br>
Extracts title blocks, dimensions, annotations, and symbols from construction drawing PDFs and generates a single-file quality check report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and building project teams use this skill to parse text-layer construction PDF drawings, extract drawing metadata and symbols, and generate Markdown quality reports before estimating, BIM review, or project coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated report filename or output path could overwrite existing local work. <br>
Mitigation: Choose a unique report filename or output directory before writing the Markdown report. <br>
Risk: The workflow depends on installing pdfplumber in the local Python environment. <br>
Mitigation: Install pdfplumber only from a trusted package source and review dependency changes before use. <br>
Risk: The skill processes user-provided drawing PDFs that may contain sensitive project information. <br>
Mitigation: Run the skill only on drawings the user is authorized and intends to analyze, and keep outputs in an approved local location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/drawing-insight-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets, plus generated Markdown report content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a text-layer PDF and local Python environment with pdfplumber; the free version has documented limits for batch size, DWG input, OCR, cross-drawing indexing, and custom parsing rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
