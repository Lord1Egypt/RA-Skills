## Description: <br>
Downloads arXiv paper PDFs or LaTeX source archives from an arXiv ID or URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninganme](https://clawhub.ai/user/ninganme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to fetch arXiv PDFs or LaTeX source archives into a local output directory when given an arXiv ID or URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads files from arxiv.org and writes them to the local filesystem. <br>
Mitigation: Use it only when arXiv downloads are intended, save into a dedicated output folder, and review downloaded files before opening or processing them. <br>
Risk: Custom output filenames and output paths are not fully constrained before files are written. <br>
Mitigation: Avoid untrusted custom filenames and choose an explicit, dedicated output directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ninganme/arxiv-downloader) <br>
- [arXiv](https://arxiv.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Console status text and downloaded PDF or tar.gz files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports an optional output directory, LaTeX source mode, and custom output filename.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
