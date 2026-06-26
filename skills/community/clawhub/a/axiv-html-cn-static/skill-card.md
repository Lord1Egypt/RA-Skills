## Description: <br>
This skill converts an arXiv paper HTML page into a local Chinese static HTML webpage while preserving local figures, icons, CSS assets, paper metadata, and Chinese text produced from arxiv-paper-resolver-style section extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengyaofang](https://clawhub.ai/user/zhengyaofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert arXiv experimental HTML and Chinese Markdown into a local Chinese static paper webpage. The workflow localizes figures, tables, icons, CSS, PDF, and metadata into an offline-ready output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow downloads arXiv paper assets and installs Python dependencies, which may not satisfy stricter offline or supply-chain requirements. <br>
Mitigation: Use only intended arXiv IDs, install dependencies in an isolated environment, and replace the default MathJax CDN reference with a local renderer when offline operation is required. <br>
Risk: Generated pages may depend on arXiv HTML availability and may leave limited remote links for paper references or MathJax rendering. <br>
Mitigation: Run the documented output checks, verify that required images and CSS are localized under assets/, and fall back to a PDF or LaTeX parsing route when arXiv HTML is unavailable. <br>


## Reference(s): <br>
- [Output contract](references/output_contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown, files] <br>
**Output Format:** [Markdown instructions with shell commands and generated local HTML, JSON metadata, PDF, assets, and Chinese Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a paper output directory containing index.html, localized assets, metadata JSON, asset manifest JSON, figure list JSON, PDF, and Chinese Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
