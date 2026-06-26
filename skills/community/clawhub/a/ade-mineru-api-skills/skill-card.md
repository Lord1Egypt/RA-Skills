## Description: <br>
MinerU document extraction CLI that converts PDFs, images, and web pages into Markdown, HTML, LaTeX, or DOCX via the MinerU API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[decrystal](https://clawhub.ai/user/decrystal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to install and operate the MinerU CLI for extracting text, tables, formulas, and web page content from PDFs, images, DOCX files, and URLs into Markdown or other document formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs the MinerU CLI from remote shell and PowerShell scripts. <br>
Mitigation: Inspect or otherwise verify the installer source before running it in environments with supply-chain controls. <br>
Risk: The MinerU CLI sends documents or URLs to the MinerU API for processing. <br>
Mitigation: Confirm what files or URLs will be processed and avoid uploading sensitive, regulated, proprietary, or internal-only documents unless MinerU's data-handling terms are acceptable. <br>
Risk: MinerU authentication tokens may be supplied by flag, environment variable, or local config. <br>
Mitigation: Protect the MinerU token and avoid exposing it in shared logs, shell history, or command transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/decrystal/ade-mineru-api-skills) <br>
- [decrystal publisher profile](https://clawhub.ai/user/decrystal) <br>
- [MinerU token and account portal](https://mineru.net) <br>
- [Install mineru for Linux/macOS](https://cdn-mineru.openxlab.org.cn/open-api-cli/install.sh) <br>
- [Install mineru for Windows](https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The wrapped CLI can produce Markdown, JSON, HTML, LaTeX, DOCX, files, and directories depending on command flags.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
