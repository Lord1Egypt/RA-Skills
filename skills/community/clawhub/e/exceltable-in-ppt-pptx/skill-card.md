## Description: <br>
Presentation creation, editing, and analysis for creating, modifying, and inspecting PowerPoint .pptx files, including layouts, comments, and speaker notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, analysts, and content teams use this skill to have an agent create, edit, inspect, and validate PowerPoint presentations. It supports HTML-to-PPTX generation, template-based deck updates, OOXML editing, text inventory, replacement workflows, and thumbnail review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify PowerPoint files and may overwrite or clear presentation content when replacement JSON is incomplete or output paths are chosen incorrectly. <br>
Mitigation: Work in a dedicated folder, keep backups of original decks, review replacement JSON before applying it, and choose output paths carefully. <br>
Risk: Rendering untrusted HTML or processing untrusted Office files may expose the agent environment to document-processing risks. <br>
Mitigation: Avoid rendering untrusted HTML or Office files outside a sandboxed environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/exceltable-in-ppt-pptx) <br>
- [HTML to PowerPoint Guide](html2pptx.md) <br>
- [Office Open XML Technical Reference for PowerPoint](ooxml.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, JSON replacement data, and generated or modified PowerPoint files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local presentation artifacts, thumbnails, extracted inventories, replacement JSON, and validation reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
