## Description: <br>
Enables agents to control GIMP through CLI-Anything for image-editing tasks such as creating projects, managing layers, applying filters, and exporting images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sly27](https://clawhub.ai/user/Sly27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users can use this skill to run GIMP image-editing workflows from command-line prompts, including project creation, layer operations, filters, drawing, batch processing, and export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image-editing commands may modify or overwrite user files when input and output paths are ambiguous. <br>
Mitigation: Give explicit input and output paths, prefer new filenames for exports, and require confirmation before overwriting or modifying original files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sly27/cli-anything-gimp) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI can emit JSON or human-readable command output depending on invocation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
