## Description: <br>
Converts code files into A4-ratio SVG and PNG pages with line numbers and syntax highlighting, then merges pages into per-file PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yon-gjun](https://clawhub.ai/user/yon-gjun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare source files for documentation, review, sharing, or printing by generating A4 page images and PDFs with readable line numbers and syntax highlighting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local converter processes whatever paths are listed in FILES and writes generated image directories and PDFs in the current working directory. <br>
Mitigation: Review and edit FILES before running the script, and run it only in the intended workspace. <br>
Risk: The bundled maintenance scripts can edit Markdown documentation files if run manually. <br>
Mitigation: Do not run the _fix_* scripts unless intentionally updating those documentation files. <br>
Risk: The workflow requires local npm and pip dependencies. <br>
Mitigation: Install dependencies only in an environment where running local Python, Node, @resvg/resvg-js, and img2pdf is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yon-gjun/code-to-images) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are SVG, PNG, and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Users configure the FILES list and rendering settings before running the local converter.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
