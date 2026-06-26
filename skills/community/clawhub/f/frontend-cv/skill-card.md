## Description: <br>
Create professional HTML/PDF resumes from any input format (md/pdf/word/txt). Extracts resume data, converts to structured YAML, generates styled HTML with multiple theme options, and exports to PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VintLin](https://clawhub.ai/user/VintLin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, job seekers, and resume writers use this skill to turn existing resume files or structured resume data into print-ready HTML resumes with selectable professional themes and PDF export guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive resume content, including personal contact details and employment history. <br>
Mitigation: Work in a private local folder, review generated YAML and HTML before sharing, and avoid committing resume outputs. <br>
Risk: Generated previews or final HTML may load external fonts. <br>
Mitigation: Remove or replace external font links when offline operation or privacy-sensitive handling is required. <br>
Risk: Preview cleanup can delete generated local preview files. <br>
Mitigation: Confirm the preview directory and preserve any needed files before cleanup. <br>


## Reference(s): <br>
- [Frontend Cv ClawHub Page](https://clawhub.ai/VintLin/frontend-cv) <br>
- [README](artifact/README.md) <br>
- [HTML Shell](artifact/references/html-template.md) <br>
- [RenderCV Theme Presets](artifact/references/theme-presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML resume data, shell commands, and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local preview HTML files and a final self-contained resume HTML file for browser PDF export.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
