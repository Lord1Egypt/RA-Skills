## Description: <br>
AB Agents Vision analyzes local or URL-hosted images with the MiniMax VL API to describe scenes, extract text, and analyze photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexburrstudio](https://clawhub.ai/user/alexburrstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send selected image files or image URLs to MiniMax for scene description, OCR-style text extraction, and photo analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, and prompts are processed by MiniMax's remote service. <br>
Mitigation: Use only images and prompts approved for external processing; avoid secrets, private screenshots, regulated documents, and personal photos unless that processing is acceptable. <br>
Risk: The skill requires a sensitive MiniMax API credential. <br>
Mitigation: Provide the API key through environment configuration, keep it out of prompts and committed files, and rotate it if exposure is suspected. <br>
Risk: The artifact's quick-start instructions include piping a remote installer script to a shell. <br>
Mitigation: Prefer installing uv through a package manager or downloading and reviewing the installer before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexburrstudio/ab-agents-vision) <br>
- [Publisher profile](https://clawhub.ai/user/alexburrstudio) <br>
- [AB Agents skills homepage](https://github.com/alexburrstudio/ab-agents-skills) <br>
- [MiniMax platform](https://platform.minimax.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text returned by a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key and sends the selected image or image URL plus prompt to MiniMax's remote vision service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
