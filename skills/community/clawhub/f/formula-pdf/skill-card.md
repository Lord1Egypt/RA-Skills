## Description: <br>
Renders documents that contain mathematical formulas into PDFs by generating HTML, loading MathJax, and printing through Microsoft Edge in headless mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nahida-robin](https://clawhub.ai/user/nahida-robin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to turn reports, notes, worksheets, and technical documents with LaTeX-style math into PDF files with rendered formulas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The enhanced conversion workflow can forcibly close all Microsoft Edge processes. <br>
Mitigation: Avoid --kill-edge, taskkill, and Stop-Process workflows unless browser work is saved and the user explicitly wants all Edge windows closed. <br>
Risk: The workflow uses headless Edge automation to print local HTML to PDF. <br>
Mitigation: Review generated HTML, command arguments, and file paths before execution, especially when converting untrusted content. <br>
Risk: Formula rendering depends on loading MathJax from an external CDN. <br>
Mitigation: Use the skill only where external MathJax loading is acceptable, or replace the CDN dependency with a reviewed local MathJax copy for restricted environments. <br>


## Reference(s): <br>
- [Formula-PDF Release Page](https://clawhub.ai/nahida-robin/formula-pdf) <br>
- [Lessons Learned](references/lessons_learned.md) <br>
- [MathJax tex-chtml.js CDN](https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [PDF documents generated from HTML with MathJax-rendered formulas, with Markdown guidance and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft Edge headless mode; optional PyMuPDF verification can check whether raw LaTeX remains in generated PDF text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
