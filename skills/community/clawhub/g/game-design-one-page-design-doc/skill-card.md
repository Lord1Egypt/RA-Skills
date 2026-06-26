## Description: <br>
Create a concise one-page game design document and export it as both markdown and PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game designers, developers, and creative teams use this skill to compress game concept notes into a one-page design document that is easy to review, share, and refine. It helps produce a structured source JSON file, an editable Markdown version, and a polished PDF one-pager. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The renderer writes JSON, Markdown, and PDF files to the paths it is given. <br>
Mitigation: Use a project-specific output folder and review filenames before rendering, especially in important project directories. <br>
Risk: PDF rendering depends on the ReportLab package and available system fonts. <br>
Mitigation: Install ReportLab and confirm Poppins, Liberation Sans, or DejaVu fonts are available before relying on PDF output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stanestane/game-design-one-page-design-doc) <br>
- [Source Notes](references/source-notes.md) <br>
- [Family Conventions](references/family-conventions.md) <br>
- [Example Input](references/example-input.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON source data, shell commands, and generated Markdown and PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSON, Markdown, and PDF outputs using filenames or folders selected by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
