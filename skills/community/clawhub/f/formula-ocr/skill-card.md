## Description: <br>
OCR and recognize mathematical formulas from PDFs and images using MinerU, converting printed or handwritten equations into LaTeX or text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, educators, developers, and other external users use this skill to digitize formula content from PDFs, scans, screenshots, or images into editable LaTeX or text through the MinerU CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files or URLs processed with this skill may be shared with the external MinerU service. <br>
Mitigation: Use a dedicated MinerU token where possible and avoid processing confidential documents or private/internal URLs unless MinerU's data handling is acceptable. <br>
Risk: Formula OCR output can be incorrect or incomplete, especially for complex, scanned, or handwritten notation. <br>
Mitigation: Review extracted formulas before relying on them in downstream analysis, publication, or code. <br>


## Reference(s): <br>
- [Formula Ocr on ClawHub](https://clawhub.ai/mzlzyca/formula-ocr) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of mineru-open-api for PDFs and image files; extraction output may be sent to stdout or saved to an output directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
