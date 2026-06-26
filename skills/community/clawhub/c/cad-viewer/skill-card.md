## Description: <br>
CAD Viewer helps agents read, analyze, query, measure, audit, and visualize CAD DWG/DXF drawing files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanshuili334-code](https://clawhub.ai/user/sanshuili334-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to inspect DWG/DXF drawings, extract structured CAD data, measure spatial relationships, generate drawing images or PDFs, and audit common CAD compliance issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assisted setup can use sudo and download third-party CAD binaries. <br>
Mitigation: Prefer manual setup or a VM/container, review setup commands before running them, and only run confirmed setup when the required sources are acceptable. <br>
Risk: Project-local learning files may retain CAD workflow details from sensitive projects. <br>
Mitigation: Inspect or disable project learning files for sensitive work and avoid recording confidential drawing details. <br>


## Reference(s): <br>
- [CAD Viewer on ClawHub](https://clawhub.ai/sanshuili334-code/cad-viewer) <br>
- [CAD domain knowledge reference](references/cad_knowledge.md) <br>
- [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter) <br>
- [QCAD download](https://qcad.org/en/download) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, files] <br>
**Output Format:** [Markdown guidance with shell commands; CAD tool commands return JSON and may write PNG, PDF, or SVG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands emit structured JSON to stdout; screenshots and exports are written to user-specified paths.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
